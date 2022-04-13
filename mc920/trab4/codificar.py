import cv2
import sys
import os
import numpy as np
import string

def readImage(filepath):
    return cv2.imread(filepath, cv2.IMREAD_COLOR)

def saveImage(filepath, image):
    cv2.imwrite(filepath, image)

def readText(in_text):
    text_file = open(in_text, "r")
    text = text_file.read()
    text_file.close()
    # Only ASCII caracters
    return ''.join(filter(lambda x: x in set(string.printable), text))

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def replaceBit(num, bit, plano_bits):
    mask = 1 << plano_bits
    return (num & ~mask) | ((bit << plano_bits) & mask)

def writeBitsAtPos(image, x, y, text, i, plano_bits, text_size):
    for k in range(3):
        if i >= text_size:
                break
        image[k][x][y] = replaceBit(image[k][x][y], int(text[i]), plano_bits)
        i += 1
    return (image, i)

def writeTextOnImage(image, text, plano_bits):
    width = image[0].shape[0]
    height = image[0].shape[1]
    text_size = len(text)
    i = 0
    for x in range(width):
        for y in range(height):
            # Write bits at R, G and B
            (image, i) = writeBitsAtPos(image, x, y, text, i, plano_bits, text_size)
        if i >= text_size:
            break
    return image

def extractBitPlane(image, out_path):
    for plano_bits in range(8):
        img = np.bitwise_and(image, 1 << plano_bits) 
        img = img*255
        (image_b, image_g, image_r) = cv2.split(img)
        saveImage(out_path + "_red_" + str(plano_bits) + ".png", image_r)
        saveImage(out_path + "_green_" + str(plano_bits) + ".png", image_g)
        saveImage(out_path + "_blue_" + str(plano_bits) + ".png", image_b)

if __name__ == '__main__':
    in_file = sys.argv[1]
    in_text = sys.argv[2]
    plano_bits = int(sys.argv[3])
    out_file = sys.argv[4]
    out_path = "./out/"
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    # Read image and split RGB
    image = readImage(in_file)
    (image_b, image_g, image_r) = cv2.split(image)
    image = [image_b, image_g, image_r]

    # Read text and convert to binary
    text = readText(in_text)
    text += "\0"
    text = text_to_bits(text)

    # Write text on image
    image = writeTextOnImage(image, text, plano_bits)
    image = cv2.merge((image[0], image[1], image[2]))

    # Save image
    saveImage(out_path + out_file, image)

    # Extracting bit planes
    extractBitPlane(image, out_path + out_file[:-4])