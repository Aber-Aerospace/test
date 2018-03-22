#!/usr/bin/python3
'''A python program to record data from a rocket launch.'''

import os
import time
import pickle
from multiprocessing import Pool as pool
from multiprocessing import Queue
import uuid
import Adafruit_BMP.BMP085 as BMP085
from mpu6050 import mpu6050




def fileWrite(info):
    info = ("{:.3f}".format(info))
    f.write(info)
    f.write(":")


def fileWriteArray(info):
    for i in range(0, 3):
        filWrite(info[units[i]])

'''
startTime = time.time()
while True:
    filWrite(time.time()-startTime)
    fileWriteArray(s6050.get_gyro_data())
    fileWriteArray(s6050.get_accel_data())
    fileWrite(s185.read_temperature())
    fileWrite(s185.read_pressure())
    fileWrite(s185.read_altitude())
    f.write('/n')
'''

def readGPS(queue):
    '''Empty for now'''
    while True:
        pass

def readI2c(queue):
    '''constantly looping watcher to pull data out of the i2c sensors'''
    s185 = BMP085.BMP085()
    s6050 = mpu6050(0x68)
    while True:
        data = []
        data.append(time.time())
        data.append(s6050.get_all_data())
        data.append(s185.read_temperature())
        data.append(s185.read_pressure())
        data.append(s185.read_altitude())
        queue.put(data)

def makeCurrData(i2cq, gpsq):
    '''emptys the sensor queues into a dict.'''
    meh = i2cq.get()
    gps = gpsq.get()

    return [meh, gps]

def dataToFile(p=None, d=None):
    '''exports a dataset as a pickle file with a uuid name.'''
    pickle.dump(d, open(p, 'wb'))


def main():

    path = "/home/pi/data/{}".format(uuid.uuid4())

    os.mkdir(path)

    p = pool(20)
    i2cq = Queue()
    gpsq = Queue()
    p.apply_async(readGPS, gpsq)
    p.apply_async(readI2c, i2cq)

    while True:
        data = list()
        for i in range(0, 500):
            currData = makeCurrData(i2cq, gpsq)
            data.append(currData)

        print(data)
        #p.apply_async(dataToFile, [p=path, d=data])


if __name__ == "__main__":
    main()
