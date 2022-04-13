import cv2
import sys
import os
import numpy as np
import math

def readImage(filepath):
    return cv2.imread(filepath, cv2.IMREAD_COLOR)

def saveImage(filepath, image):
    cv2.imwrite(filepath, image, [cv2.IMWRITE_PNG_COMPRESSION, 9])

def svd(image, k):
    # Split to G, B, R
    f = [image[:, :, 0], image[:, :, 1], image[:, :, 2]]
    g = f
    for i in range(3):
        u, s, vh = np.linalg.svd(f[i], full_matrices=False)
        # Consider only k components
        g[i] = u[:, :k] @ np.diag(s[:k]) @ vh[:k, :]
    return cv2.merge((g[0], g[1], g[2]))

def rmse(image_a, image_b):
    return math.sqrt(np.sum((image_a - image_b)**2)/(image_a.shape[0]*image_a.shape[1]*image_a.shape[2]))

def compressionRate(image_a, image_b):
    return os.path.getsize(image_b)/os.path.getsize(image_a)

if __name__ == '__main__':
    in_file = sys.argv[1]
    k = int(sys.argv[2])
    out_file = sys.argv[3]
    out_path = "./out/"
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    # Read image
    image = readImage(in_file)

    # Calculate PCA
    img = svd(image, k)

    # Save image
    saveImage(out_path + out_file, img)

    # Calculate compression rate
    print("Taxa de compressão (p) =", compressionRate(in_file, out_path + out_file))

    # Calculate RMSE
    print("RMSE =", rmse(image, img))