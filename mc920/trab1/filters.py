import numpy as np

# Floyd and Steingberg
def halftoningFloyd(image):
    f = np.copy(image)
    height = f.shape[1]
    width = f.shape[0]
    g = np.zeros((width, height))
    for x in range(0, width):
        for y in range(0, height):
            if f[x][y] < 128:
                g[x][y] = 0
            else:
                g[x][y] = 1
            error = f[x][y] - g[x][y]*255

            f[x][y] = 0
            if x + 1 < width:
                f[x+1][y] += (7/16)*error
            if x - 1 > 0 and y + 1 < height:
                f[x-1][y+1] += (3/16)*error
            if y + 1 < height:
                f[x][y+1] += (5/16)*error
            if x + 1 < width and y + 1 < height:
                f[x+1][y+1] += (1/16)*error

    g = np.multiply(g, 255)
    return g

def halftoningZigzagFloyd(image):
    f = np.copy(image)
    height = f.shape[1]
    width = f.shape[0]
    g = np.zeros((width, height))
    i = 0
    for x in range(0, width):
        if i % 2 == 0: #going right
            for y in range(0, height):
                if f[x][y] < 128:   
                    g[x][y] = 0
                else:
                    g[x][y] = 1
                error = f[x][y] - g[x][y]*255

                f[x][y] = 0
                if x + 1 < width:
                    f[x+1][y] += (7/16)*error
                if x - 1 > 0 and y + 1 < height:
                    f[x-1][y+1] += (3/16)*error
                if y + 1 < height:
                    f[x][y+1] += (5/16)*error
                if x + 1 < width and y + 1 < height:
                    f[x+1][y+1] += (1/16)*error
        else:
            for y in range(height-1, -1, -1):
                if f[x][y] < 128:
                    g[x][y] = 0
                else:
                    g[x][y] = 1
                error = f[x][y] - g[x][y]*255

                f[x][y] = 0
                if x - 1 < 0:
                    f[x-1][y] += (7/16)*error
                if x + 1 < width and y + 1 < height:
                    f[x+1][y+1] += (3/16)*error
                if y + 1 < height:
                    f[x][y+1] += (5/16)*error
                if x - 1 < 0 and y + 1 < height:
                    f[x-1][y+1] += (1/16)*error
        i += 1
    g = np.multiply(g, 255)
    return g

# Burkes
def halftoningBurkes(image):
    f = np.copy(image)
    height = f.shape[1]
    width = f.shape[0]
    g = np.zeros((width, height))
    for x in range(0, width):
        for y in range(0, height):
            if f[x][y] < 128:
                g[x][y] = 0
            else:
                g[x][y] = 1
            error = f[x][y] - g[x][y]*255

            f[x][y] = 0
            if x + 1 < width:
                f[x+1][y] += (8/32)*error
            if x - 1 > 0 and y + 1 < height:
                f[x-1][y+1] += (4/32)*error
            if y + 1 < height:
                f[x][y+1] += (8/32)*error
            if x + 1 < width and y + 1 < height:
                f[x+1][y+1] += (4/32)*error
            if x - 2 > 0 and y + 1 < height:
                f[x-2][y+1] += (2/32)*error
            if x + 2 < width:
                f[x+2][y] += (4/32)*error
            if x + 2 < width and y + 1 < height:
                f[x+2][y] += (2/32)*error

    g = np.multiply(g, 255)
    return g

def halftoningZigzagBurkes(image):
    f = np.copy(image)
    height = f.shape[1]
    width = f.shape[0]
    g = np.zeros((width, height))
    i = 0
    for x in range(0, width):
        if i % 2 == 0: #going right
            for y in range(0, height):
                if f[x][y] < 128:   
                    g[x][y] = 0
                else:
                    g[x][y] = 1
                error = f[x][y] - g[x][y]*255

                f[x][y] = 0
                if x + 1 < width:
                    f[x+1][y] += (8/32)*error
                if x - 1 > 0 and y + 1 < height:
                    f[x-1][y+1] += (4/32)*error
                if y + 1 < height:
                    f[x][y+1] += (8/32)*error
                if x + 1 < width and y + 1 < height:
                    f[x+1][y+1] += (4/32)*error
                if x - 2 > 0 and y + 1 < height:
                    f[x-2][y+1] += (2/32)*error
                if x + 2 < width:
                    f[x+2][y] += (4/32)*error
                if x + 2 < width and y + 1 < height:
                    f[x+2][y] += (2/32)*error
        else:
            for y in range(height-1, -1, -1):
                if f[x][y] < 128:
                    g[x][y] = 0
                else:
                    g[x][y] = 1
                error = f[x][y] - g[x][y]*255

                f[x][y] = 0
                if x - 1 > 0:
                    f[x-1][y] += (8/32)*error
                if x + 1 < width and y + 1 < height:
                    f[x+1][y+1] += (4/32)*error
                if y + 1 < height:
                    f[x][y+1] += (8/32)*error
                if x - 1 > 0 and y + 1 < height:
                    f[x-1][y+1] += (4/32)*error
                if x - 2 > 0 and y + 1 < height:
                    f[x-2][y+1] += (2/32)*error
                if x + 2 < width:
                    f[x+2][y] += (4/32)*error
                if x + 2 < width and y + 1 < height:
                    f[x+2][y] += (2/32)*error
        i += 1
    g = np.multiply(g, 255)
    return g