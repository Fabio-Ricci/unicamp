import cv2
import numpy as np
import matplotlib.pyplot as plt

def mode(window):
    values = [0 for i in range(256)]
    used_pixels = []
    for px in window:
        values[px] += 1
        used_pixels.append(px)
    
    #FIXME
    return np.max(used_pixels) # mode

image = cv2.imread("../in/baboon.png", cv2.IMREAD_GRAYSCALE)
result = image[:,:].copy()
for y in range(3,image.shape[0]-3):
    for x in range(3,image.shape[1]-3):
        window = [
            image[x-1,y-1],image[x,y-1],image[x+1,y-1],
            image[x-1,y],image[x,y],image[x+1,y],
            image[x-1,y+1],image[x,y+1],image[x+1,y+1]
        ]
        result[x,y] = mode(window)

plt.imshow(result, cmap="gray", vmin=0, vmax=255)
plt.show()