import cv2
import numpy as np
import math


def find_corners(image_name):
    """
    Calculates the cornerness values of pixel within an image
    :param image_name: name of image to be processed
    :return: array of response values
    """
    # read in grayscale image
    im_grayscale = cv2.imread(image_name, 0)
    # find numRow (height)
    numRow = im_grayscale.shape[0]
    # find numCol (width)
    numCol = im_grayscale.shape[1]
    # offset for sliding window
    offset = 1
    # initialize 0 arrays for Ix gradient and Iy gradient
    ix = np.zeros((numRow, numCol, 1), np.float32)
    iy = np.zeros((numRow, numCol, 1), np.float32)
    # initialize 0 arrays for square values
    ixix = np.zeros((numRow, numCol, 1), np.float32)
    iyiy = np.zeros((numRow, numCol, 1), np.float32)
    ixiy = np.zeros((numRow, numCol, 1), np.float32)
    # initialize 0 array for response values
    corner_values = np.zeros((numRow, numCol, 1), np.float32)

    # iterate over pixels in im_grayscale
    for i in range(0, numRow - 1):
        for j in range(0, numCol - 1):
            # create ix values
            ix[i][j] = (int(im_grayscale[i][j + 1]) - int(im_grayscale[i][j - 1]))
            # create iy values
            iy[i][j] = (int(im_grayscale[i + 1][j]) - int(im_grayscale[i - 1][j]))
            # create ixix values
            ixix[i][j] = (int(ix[i][j]) ** 2)
            # create iyiy values
            iyiy[i][j] = (int(iy[i][j]) ** 2)
            # create ixiy values
            ixiy[i][j] = (int(ix[i][j]) * int(iy[i][j]))

    # find corners
    # iterate over each pixel adjusting with window offset
    for y in range(offset, numRow - offset):
        for x in range(offset, numCol - offset):
            # create lists of square values within window
            window_ixix = ixix[y - offset: y + offset + 1, x - offset: x + offset + 1]
            window_iyiy = iyiy[y - offset: y + offset + 1, x - offset: x + offset + 1]
            window_ixiy = ixiy[y - offset: y + offset + 1, x - offset: x + offset + 1]
            # sum square values found in lists to get sum of squares
            sum_ixix = window_ixix.sum()
            sum_iyiy = window_iyiy.sum()
            sum_ixiy = window_ixiy.sum()
            # find the determinate of sum of squares
            determinate = (sum_ixix * sum_iyiy) - (sum_ixiy ** 2)
            # find the trace of the sum of squares
            trace = sum_ixix + sum_iyiy
            # use the determinate and trace to find the "cornerness" response of the pixel's window
            response = determinate - (.05 * (trace ** 2))
            # append response values to corner array
            corner_values[y][x] = response

    return corner_values


def threshold_find_corners(image_name, percent):
    """
    Finds corners and image and marks the ones that are above a certain threshold
    :param image_name: name of image to be processed
    :param percent: the decimal percentage that determines the threshold
    :return:
    """
    # get corner values
    corner_values = find_corners(image_name)
    # read in color image
    im_color = cv2.imread(image_name)
    # find numRow (height)
    numRow = im_color.shape[0]
    # find numCol (width)
    numCol = im_color.shape[1]
    # find max of corner array to find highest response value
    max_response = np.amax(corner_values)
    # set threshold to a percentage of max response value
    threshold = max_response - (max_response * percent)

    # iterate over pixels within corner values
    for y in range(1, numRow - 1):
        for x in range(1, numCol - 1):
            # check to see if corner value is greater than threshold
            if corner_values[y][x] > threshold:
                # paint all pixels in window red
                im_color[y][x][0] = 0
                im_color[y][x][1] = 0
                im_color[y][x][2] = 255

                im_color[y - 1][x - 1][0] = 0
                im_color[y - 1][x - 1][1] = 0
                im_color[y - 1][x - 1][2] = 255

                im_color[y - 1][x][0] = 0
                im_color[y - 1][x][1] = 0
                im_color[y - 1][x][2] = 255

                im_color[y - 1][x + 1][0] = 0
                im_color[y - 1][x + 1][1] = 0
                im_color[y - 1][x + 1][2] = 255

                im_color[y][x][0] = 0
                im_color[y][x][1] = 0
                im_color[y][x][2] = 255

                im_color[y][x - 1][0] = 0
                im_color[y][x - 1][1] = 0
                im_color[y][x - 1][2] = 255

                im_color[y][x + 1][0] = 0
                im_color[y][x + 1][1] = 0
                im_color[y][x + 1][2] = 255

                im_color[y + 1][x - 1][0] = 0
                im_color[y + 1][x - 1][1] = 0
                im_color[y + 1][x - 1][2] = 255

                im_color[y + 1][x][0] = 0
                im_color[y + 1][x][1] = 0
                im_color[y + 1][x][2] = 255

                im_color[y + 1][x + 1][0] = 0
                im_color[y + 1][x + 1][1] = 0
                im_color[y + 1][x + 1][2] = 255

    cv2.imshow("Displaying im_color", im_color / 255.0)
    cv2.imwrite("threshold_" + image_name, im_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def blocks_find_corners(image_name, m, n):
    """
    Divides image into m blocks. Chooses the nth highest pixels to label within each block.
    :param image_name: name of the image to be processed
    :param m: amount of blocks in image
    :param n: number of pixels to mark in each block determined by highest corner response
    :return:
    """
    # get corner values
    corner_values = find_corners(image_name)
    # read in color image
    im_color = cv2.imread(image_name)
    # find numRow (height)
    numRow = im_color.shape[0]
    # find numCol (width)
    numCol = im_color.shape[1]

    for y in range(0, numRow - 1, math.ceil(numRow / m)):
        for x in range(0, numCol - 1, math.ceil(numCol / m)):
            corner_list = []
            for i in range(y, y + math.ceil(numRow / m)):
                for j in range(x, x + math.ceil(numCol / m)):
                    if i < numRow and j < numCol:
                        response = int(corner_values[i][j])
                        corner = [i, j, response]
                        corner_list.append(corner)
            corner_list.sort(reverse=True, key=lambda x: x[2])
            for k in range(0, n):
                val_y = corner_list[k][0]
                val_x = corner_list[k][1]
                im_color[val_y][val_x][0] = 0
                im_color[val_y][val_x][1] = 0
                im_color[val_y][val_x][2] = 255

                im_color[val_y - 1][val_x - 1][0] = 0
                im_color[val_y - 1][val_x - 1][1] = 0
                im_color[val_y - 1][val_x - 1][2] = 255

                im_color[val_y - 1][val_x][0] = 0
                im_color[val_y - 1][val_x][1] = 0
                im_color[val_y - 1][val_x][2] = 255

                im_color[val_y - 1][val_x + 1][0] = 0
                im_color[val_y - 1][val_x + 1][1] = 0
                im_color[val_y - 1][val_x + 1][2] = 255

                im_color[val_y][val_x][0] = 0
                im_color[val_y][val_x][1] = 0
                im_color[val_y][val_x][2] = 255

                im_color[val_y][val_x - 1][0] = 0
                im_color[val_y][val_x - 1][1] = 0
                im_color[val_y][val_x - 1][2] = 255

                im_color[val_y][val_x + 1][0] = 0
                im_color[val_y][val_x + 1][1] = 0
                im_color[val_y][val_x + 1][2] = 255

                im_color[val_y + 1][val_x - 1][0] = 0
                im_color[val_y + 1][val_x - 1][1] = 0
                im_color[val_y + 1][val_x - 1][2] = 255

                im_color[val_y + 1][val_x][0] = 0
                im_color[val_y + 1][val_x][1] = 0
                im_color[val_y + 1][val_x][2] = 255

                im_color[val_y + 1][val_x + 1][0] = 0
                im_color[val_y + 1][val_x + 1][1] = 0
                im_color[val_y + 1][val_x + 1][2] = 255

    cv2.imshow("Displaying im_color", im_color / 255.0)
    cv2.imwrite("borders_" + image_name, im_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def Main():
    #threshold_find_corners("cityscape_night.png", .97)
    #blocks_find_corners("cityscape_night.png", 10, 20)


Main()
