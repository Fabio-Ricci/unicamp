import cv2
import numpy as np
import matplotlib.pyplot as plt

def readImage(filename):
    image = cv2.imread("../in/" + filename, cv2.IMREAD_GRAYSCALE)
    return image

def showImage(image):
    plt.imshow(image, cmap="gray", vmin=0, vmax=255)
    plt.show()

if __name__ == '__main__':
    image = readImage("baboon.png")
    showImage(image)
