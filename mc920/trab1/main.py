import cv2
import sys
import filters
import os

def readColoredImage(filepath):
    return cv2.imread(filepath, cv2.IMREAD_COLOR)

def readGreyImage(filepath):
    return cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

if __name__ == '__main__':
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    path = os.path.dirname(os.path.realpath(__file__))

    if not os.path.exists("./out/"):
        os.makedirs("./out/")
    if not os.path.exists("./out/color"):
        os.makedirs("./out/color")
    if not os.path.exists("./out/grey"):
        os.makedirs("./out/grey")

    out_path_color = path + "/out/color/" + out_file
    out_path_grey = path + "/out/grey/" +  out_file

    image = readColoredImage(in_file)
    (image_r, image_g, image_b) = cv2.split(image)
    
    # Floyd and Steinberg
    # Halftoning Color
    binary_r = filters.halftoningFloyd(image_r)
    binary_g = filters.halftoningFloyd(image_g)
    binary_b = filters.halftoningFloyd(image_b)
    binary = cv2.merge((binary_r, binary_g, binary_b))
    cv2.imwrite(out_path_color + "_floyd.png", binary)
    
    # Halftoning Zig-Zag Color
    binary_r = filters.halftoningZigzagFloyd(image_r)
    binary_g = filters.halftoningZigzagFloyd(image_g)
    binary_b = filters.halftoningZigzagFloyd(image_b)
    binary = cv2.merge((binary_r, binary_g, binary_b))
    cv2.imwrite(out_path_color + "_floyd_zigzag.png", binary)

    # Burkes
    # Halftoning Color
    binary_r = filters.halftoningBurkes(image_r)
    binary_g = filters.halftoningBurkes(image_g)
    binary_b = filters.halftoningBurkes(image_b)
    binary = cv2.merge((binary_r, binary_g, binary_b))
    cv2.imwrite(out_path_color + "_burkes.png", binary)
    
    # Halftoning Zig-Zag Color
    binary_r = filters.halftoningZigzagBurkes(image_r)
    binary_g = filters.halftoningZigzagBurkes(image_g)
    binary_b = filters.halftoningZigzagBurkes(image_b)
    binary = cv2.merge((binary_r, binary_g, binary_b))
    cv2.imwrite(out_path_color + "_burkes_zigzag.png", binary)

    ####################################################################
    image = readGreyImage(in_file)

    # Floyd and Steinberg
    # Halftoning Grey
    binary = filters.halftoningFloyd(image)
    cv2.imwrite(out_path_grey + "_floyd.png", binary)

    # Halftoning Zig-Zag Grey
    binary = filters.halftoningZigzagFloyd(image)
    cv2.imwrite(out_path_grey + "_floyd_zigzag.png", binary)

    # Burkes
    # Halftoning Grey
    binary = filters.halftoningBurkes(image)
    cv2.imwrite(out_path_grey + "_burkes.png", binary)

    # Halftoning Zig-Zag Grey
    binary = filters.halftoningZigzagBurkes(image)
    cv2.imwrite(out_path_grey + "_burkes_zigzag.png", binary)