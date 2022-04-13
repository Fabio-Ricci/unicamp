import cv2
import sys
import os
import methods
from matplotlib import pyplot as plt

def readImage(filepath):
    return cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

def saveHistogram(image, title, path, file):
    plt.title(title)
    plt.xlabel('Nível de cinza')
    plt.ylabel('Quantidade de pixels')
    plt.hist(image, bins=255)
    plt.savefig(path + file + "_histogram")

if __name__ == '__main__':
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    out_path = os.path.dirname(os.path.realpath(__file__)) + "/out/" + out_file + "/"
    image = readImage(in_file)

    if not os.path.exists("./out/"):
        os.makedirs("./out/")
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    saveHistogram(image.flatten(), "Original Image", out_path, out_file)

    img = methods._global(image)
    cv2.imwrite(out_path + out_file + "_global.png", img)

    dark = methods.darkPixelsPercentage(img)
    print(dark, 1-dark)
    
    delta = 3
    img = methods._niblack(image, delta=delta)
    cv2.imwrite(out_path + out_file + "_niblack.png", img)

    dark = methods.darkPixelsPercentage(img)
    print(dark, 1-dark)

    delta = 2
    img = methods._bernsen(image, delta=delta)
    img = img[delta:img.shape[0]-delta, delta:img.shape[1]-delta]
    cv2.imwrite(out_path + out_file + "_bernsen.png", img)

    dark = methods.darkPixelsPercentage(img)
    print(dark, 1-dark)

    img = methods._sauvola_pietaksinen(image, delta=delta)
    img = img[delta:img.shape[0]-delta, delta:img.shape[1]-delta]
    cv2.imwrite(out_path + out_file + "_sauvola_pietaksinen.png", img)

    dark = methods.darkPixelsPercentage(img)
    print(dark, 1-dark)

    img = methods._phansalskar(image, delta=delta)
    img = img[delta:img.shape[0]-delta, delta:img.shape[1]-delta]
    cv2.imwrite(out_path + out_file + "_phansalskar.png", img)

    dark = methods.darkPixelsPercentage(img)
    print(dark, 1-dark)

    img = methods._contrast(image, delta=delta)
    img = img[delta:img.shape[0]-delta, delta:img.shape[1]-delta]
    cv2.imwrite(out_path + out_file + "_contrast.png", img)

    dark = methods.darkPixelsPercentage(img)
    print(dark, 1-dark)
    
    img = methods._average(image, delta=delta)
    img = img[delta:img.shape[0]-delta, delta:img.shape[1]-delta]
    cv2.imwrite(out_path + out_file + "_average.png", img)

    dark = methods.darkPixelsPercentage(img)
    print(dark, 1-dark)

    img = methods._median(image, delta=delta)
    img = img[delta:img.shape[0]-delta, delta:img.shape[1]-delta]
    cv2.imwrite(out_path + out_file + "_median.png", img)

    dark = methods.darkPixelsPercentage(img)
    print(dark, 1-dark)