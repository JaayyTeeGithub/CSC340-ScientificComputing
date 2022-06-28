# Author: Jeremy Thomas
# ERROR: line 145, in rotate_image
#     rotatedimage[i][j] = originalimage[a][b]
# IndexError: index 450 is out of bounds for axis 0 with size 450
# cant figure it out

import cv2
import numpy as np
import math


def matrix_multiplication(m1, m2):
    """
    multiplies the two matrix parameters, and returns the results.

    Parameters:
        m1 (list): 2D list of matrix
        m2 (list): 2D list of matrix

    Returns:
        m_result (list): 2D list result from matrix multiplication of m1
        and m2
    """

    m1_rows = len(m1)
    m1_cols = len(m1[0])
    m2_rows = len(m2)
    m2_cols = len(m2[0])

    m_result = [[0 for x in range(m2_cols)] for y in range(m1_rows)]

    for i in range(m1_rows):
        for j in range(m2_cols):
            for k in range(m2_rows):
                m_result[i][j] += int((m1[i][k] * m2[k][j]))

    return m_result


def rotation_matrix(angle):
    """
    Creates a rotational matrix. Sets the value for theta given the angle parameter.

    Parameters:
        angle (int):

    Returns:
        result(list): 2D matrix (rotational matrix)
    """
    theta = angle * np.pi / 180
    result = [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
    return result


def create_startimage(image, save_name):
    """
    Takes the image provided as a parameter and determines if its height or
    width is greater. Use the greater of the values (big) to create a new
    image with big*big dimensions with the original image placed in the center.
    Saves the image and returns nothing.

    Parameters:
        image (str): name of image file

    Returns:
        NONE
    """

    # read image1
    image1 = cv2.imread(image)
    # determine and print image1 size
    numRows = image1.shape[0]
    numCols = image1.shape[1]
    print("image1 size: ", numRows, numCols)

    # determine if the image has a greater width or height
    # whichever is greater becomes the row and col number for the new image
    if numCols > numRows:
        new_size = numCols * 1.3
    else:
        new_size = numRows * 1.3
    # print the size of the new image
    print("image2 size: ", new_size, new_size, "\n")
    # create empty image2 with predetermined size
    image2 = np.zeros((int(new_size), int(new_size), 3), np.float32)
    # determine the offset needed to center image1 within image2
    i_offset = (new_size - numRows) / 2
    j_offset = (new_size - numCols) / 2
    # iterate over image1 and place it in image2 using predetermined offset
    for i in range(numRows):
        for j in range(numCols):
            image2[int(i + i_offset)][int(j + j_offset)][0] = image1[i][j][0]
            image2[int(i + i_offset)][int(j + j_offset)][1] = image1[i][j][1]
            image2[int(i + i_offset)][int(j + j_offset)][2] = image1[i][j][2]
    # save image2
    cv2.imwrite(save_name, image2)
    print("Saved starting image!", "\n")


def rotate_image(angle, image, save_name):
    """
    Takes an image and rotates it by a specified angle. Saves the image
    based on save_name parameter.

    Parameters:
    angle (int): degree of rotation
    image (str): name of the image file to begin rotating
    save_name(str): name the new file is saved as

    Returns:
        NONE
    """
    x2 = 0
    xr = 0
    y2 = 0
    yr = 0
    pixelerror = 0
    # create a rotation matrix
    rotationmatrix = rotation_matrix(angle)
    # read the image to be rotated
    originalimage = cv2.imread(image)
    # find the dimensions of the image to be rotated
    numrows = originalimage.shape[0]
    numcols = originalimage.shape[1]
    pixels = numcols * numrows
    # find the center row and center col value to move origin
    #centerrow = numrows//2
    #centercol = numcols//2
    centerrow = numrows/2
    centercol = numcols/2
    # create the image to put rotated image in
    rotatedimage = np.zeros((int(numrows), int(numcols), 3), np.float32)
    for i in range(numrows):
        for j in range(numcols):
            # shift the coords i and j to the new origin in the center
            shiftedrow = int(i - centerrow)
            shiftedcol = int(j - centercol)
            # shiftedrow = nonroundedshiftedrow // 1
            # shiftedcol = nonroundedshiftedcol // 1

            # put these shifted coords into a vector
            coordsvector = [[shiftedcol], [shiftedrow]]
            # feed the coords to the function used for matrix multiplication
            rotatedcoords = matrix_multiplication(rotationmatrix, coordsvector)
            # get the rotated coords
            rotatedrow = rotatedcoords[1][0]
            rotatedcol = rotatedcoords[0][0]
            # move the shifted and rotated coords back to the origin
            x2 = rotatedrow + centerrow
            y2 = rotatedcol + centercol
            xr = fixedrow = rotatedrow + centerrow // 1
            yr = fixedcol = rotatedcol + centercol // 1
            # assigned them to these variable just so it matches my notes
            a = int(fixedrow)
            b = int(fixedcol)

            xdistance = (int(x2) - int(xr)) ** 2
            ydistance = (int(y2) - int(yr)) ** 2
            pixelerror = pixelerror + (xdistance + ydistance)


            if 0 < a < numrows:
                if 0 < b < numrows:
                    rotatedimage[i][j] = originalimage[a][b]

    cv2.imwrite(save_name, rotatedimage)
    return pixelerror


def absolute_color(image1, image2):
    colordistance = 0
    # read image1
    original = cv2.imread(image1)
    # read image2
    rotated = cv2.imread(image2)
    # determine and print image1 size
    numrows = original.shape[0]
    numcols = original.shape[1]
    pixels = numcols * numrows
    for i in range(numrows):
        for j in range(numcols):
            ogb,ogg,ogr = original[i, j]
            rb, rg, rr = rotated[i, j]
            rdistance = (int(ogr) - int(rr)) ** 2
            gdistance = (int(ogg) - int(rg)) ** 2
            bdistance = (int(ogb) - int(rb)) ** 2
            colordistance = colordistance + math.sqrt(rdistance + gdistance + bdistance)

    return colordistance / pixels


def rotate_images():

    print("45 pixel error: ", math.sqrt(rotate_image(45, "startImage.png", "rotation_45-1_test.png") +
                                        rotate_image(45, "rotation_45-1_test.png", "rotation_45-2_test.png") +
                                        rotate_image(45, "rotation_45-2_test.png", "rotation_45-3_test.png") +
                                        rotate_image(45, "rotation_45-3_test.png", "rotation_45-4_test.png") +
                                        rotate_image(45, "rotation_45-4_test.png", "rotation_45-5_test.png") +
                                        rotate_image(45, "rotation_45-5_test.png", "rotation_45-6_test.png") +
                                        rotate_image(45, "rotation_45-6_test.png", "rotation_45-7_test.png") +
                                        rotate_image(45, "rotation_45-7_test.png", "rotation_45-8_test.png")) /
          (585 ** 2) * 6)
    #
    print("60 pixel error: ", math.sqrt(rotate_image(60, "startImage.png", "rotation_60-1_test.png") +
                                        rotate_image(60, "rotation_60-1_test.png", "rotation_60-2_test.png") +
                                        rotate_image(60, "rotation_60-2_test.png", "rotation_60-3_test.png") +
                                        rotate_image(60, "rotation_60-3_test.png", "rotation_60-4_test.png") +
                                        rotate_image(60, "rotation_60-4_test.png", "rotation_60-5_test.png") +
                                        rotate_image(60, "rotation_60-5_test.png", "rotation_60-6_test.png")) /
          (585 ** 2) * 6)

    print("90 pixel error: ", math.sqrt(rotate_image(90, "startImage.png", "rotation_90-1_test.png") +
                                        rotate_image(90, "rotation_90-1_test.png", "rotation_90-2_test.png") +
                                        rotate_image(90, "rotation_90-2_test.png", "rotation_90-3_test.png") +
                                        rotate_image(90, "rotation_90-3_test.png", "rotation_90-4_test.png")) /
          (585 ** 2) * 4)

    print("120 pixel error: ", math.sqrt(rotate_image(120, "startImage.png", "rotation_120-1_test.png") +
                                         rotate_image(120, "rotation_120-1_test.png", "rotation_120-2_test.png") +
                                         rotate_image(120, "rotation_120-2_test.png", "rotation_120-3_test.png")) /
          (585 ** 2) * 3)

    print("180 pixel error: ", math.sqrt(rotate_image(180, "startImage.png", "rotation_180-1_test.png") +
                                         rotate_image(180, "rotation_180-1_test.png", "rotation_180-2_test.png")) /
          (585 ** 2) * 2)

    print("360 pixel error: ", math.sqrt(rotate_image(360, "startImage.png", "rotation_360-1_test.png")) / (585 ** 2))


def run_color_errors():
    print("absolute color error 45: " + str(absolute_color("startImage.png", "rotation_45-8_test.png")))
    print("absolute color error 60: " + str(absolute_color("startImage.png", "rotation_60-6_test.png")))
    print("absolute color error 90: " + str(absolute_color("startImage.png", "rotation_90-4_test.png")))
    print("absolute color error 120: " + str(absolute_color("startImage.png", "rotation_120-3_test.png")))
    print("absolute color error 180: " + str(absolute_color("startImage.png", "rotation_180-2_test.png")))
    print("absolute color error 360: " + str(absolute_color("startImage.png", "rotation_360-1_test.png")))





def Main():
    create_startimage("cones1.png", "startImage.png")
    rotate_images()
    run_color_errors()




Main()

