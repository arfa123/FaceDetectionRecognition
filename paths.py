import os

def getCurrentPath():
    currentPath = os.path.dirname(os.path.realpath('__file__'))
    return currentPath

def getHaarcascadePath():
    path = os.path.dirname(os.path.realpath('__file__'))
    cascadePath = path + '/haarcascade_frontalface_default.xml'
    return cascadePath