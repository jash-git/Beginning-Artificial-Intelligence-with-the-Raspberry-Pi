import numpy as npimport matplotlib.pyplot as pltfrom ANN import ANNimport PILfrom PIL import Imageimport RPi.GPIO as GPIOimport timeimport picamera

# instantiate and configure a Pi Camera object
camera = picamera.PiCamera()camera.color_effects = (128, 128)# setup the i/o pins 12 and 19GPIO.setmode(GPIO.BCM)GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)GPIO.setup(19, GPIO.OUT)# this is the callback function where all the processing is donedef processImage(self):
    # capture an image    camera.capture('test.jpg')    # create the test list data from an image    img = Image.open('test.jpg')    img = img.resize((28, 28), PIL.Image.ANTIALIAS)    # read pixels into list    pixels = list(img.getdata())    # convert into single values from tuples    pixels = [i[0] for i in pixels]    # save to a temp file named test.csv with comma separators    a = np.array(pixels)    a.tofile('test.csv', sep=',')    # open the temp file and read into a list    testDataFile = open('test.csv')    testDataList =  testDataFile.readlines()    testDataFile.close()    # iterate through all the list elements and submit to the ANN    for record in testDataList:        recordx = record.split(',')        input = (np.asfarray(recordx[0:])/255.0 * 0.99) + 0.01        output = ann.testNet(input)    # display output    print output# event detectionGPIO.add_event_detect(12, GPIO.RISING, callback=processImage)# setup the network configurationinode = 784hnode = 100onode = 10# set the learning ratelr = 0.1 # optimal value# instantiate an ANN object named annann = ANN(inode, hnode, onode, lr)# create the training list datadataFile = open('mnist_train.csv')dataList = dataFile.readlines()dataFile.close()# train the ANN using all the records in the listfor record in dataList:    recordx = record.split(',')    inputT = (np.asfarray(recordx[1:])/255.0 * 0.99) + 0.01    train = np.zeros(onode) + 0.01    train[int(recordx[0])] = 0.99    # training begins here    ann.trainNet(inputT, train)while True:    # blink an LED forever    GPIO.output(19, GPIO.HIGH)    time.sleep(1)    GPIO.output(19, GPIO.LOW)    time.sleep(1)