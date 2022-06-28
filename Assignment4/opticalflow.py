import math
import cv2
import numpy as np


def square_sum(m, i, j, offset):
    ly, lx = len(m), len(m[0])
    mny, mxy = max(i - offset, 0), min(i + offset + 0, ly*999)
    mnx, mxx = max(j - offset, 0), min(j + offset + 0, lx*999)
    return m[mny:mxy, mnx:mxx].flatten().sum()


def gather_data(image1, image2):
    num_row = image1.shape[0]
    num_col = image1.shape[1]
    ix = cv2.Sobel(image1, cv2.CV_64F, 1, 0, ksize=3)
    iy = cv2.Sobel(image1, cv2.CV_64F, 0, 1, ksize=3)
    ix_ix = np.zeros((num_row, num_col, 1), np.float32)
    iy_iy = np.zeros((num_row, num_col, 1), np.float32)
    ix_iy = np.zeros((num_row, num_col, 1), np.float32)
    it = np.zeros((num_row, num_col, 1), np.float32)
    iy_it = np.zeros((num_row, num_col, 1), np.float32)
    ix_it = np.zeros((num_row, num_col, 1), np.float32)

    for i in range(num_row):
        for j in range(num_col):
            ix_ix[i][j] = ix[i][j] ** 2
            iy_iy[i][j] = iy[i][j] ** 2
            ix_iy[i][j] = ix[i][j] * iy[i][j]
            it[i][j] = float(image2[i][j]) - float(image1[i][j])
            iy_it[i][j] = it[i][j] * iy[i][j]
            ix_it[i][j] = it[i][j] * ix[i][j]

    return ix_ix, iy_iy, it, iy_it, ix_it, ix_iy


def calculate(ix_ix, iy_iy, iy_it, ix_it, ix_iy):
    num_row = len(ix_ix)
    num_col = len(ix_ix[0])
    matrix_optical_flow = np.zeros((num_row, num_col), np.float32)
    x_optical_flow = np.zeros((num_row, num_col, 3), np.float32)
    y_optical_flow = np.zeros((num_row, num_col, 3), np.float32)
    matrix_mag = np.zeros((num_row, num_col), np.float32)
    matrix_u_v = np.zeros((num_row, num_col, 2), np.float32)
    mag_max = 0

    for i in range(num_row):
        for j in range(num_col):
            sum_ix_ix = square_sum(ix_ix, i, j, 9)
            sum_iy_iy = square_sum(iy_iy, i, j, 9)
            sum_ix_iy = square_sum(ix_iy, i, j, 9)
            sum_iy_it = square_sum(iy_it, i, j, 9)
            sum_ix_it = square_sum(ix_it, i, j, 9)
            determinate = (sum_ix_ix * sum_iy_iy) - (sum_ix_iy ** 2)
            if determinate != 0:
                u = (-1 / determinate) * ((sum_ix_it * sum_iy_iy) - (sum_ix_iy * sum_iy_it))
                v = (-1 / determinate) * ((-1 * (sum_ix_it * sum_ix_iy)) + (sum_ix_ix * sum_iy_it))
            else:
                u = 0
                v = 0
            magnitude = ((u ** 2) + (v ** 2)) ** (1/2)
            matrix_mag[i][j] = magnitude
            matrix_u_v[i][j][0] = u
            matrix_u_v[i][j][1] = v
            matrix_optical_flow[i][j] = (math.atan2(v, u) + math.pi) / (2 * math.pi)
            x_optical_flow[i][j][0] = (u * (math.pi / (2 * math.pi)))
            x_optical_flow[i][j][1] = (u * (1 - (math.pi / (2 * math.pi))))
            y_optical_flow[i][j][0] = (v * (math.pi / (2 * math.pi)))
            y_optical_flow[i][j][1] = (v * (1 - (math.pi / (2 * math.pi))))
            if magnitude > mag_max:
                mag_max = magnitude

    return matrix_optical_flow, matrix_mag, mag_max, matrix_u_v, x_optical_flow, y_optical_flow


def visualize(matrix_optical_flow, matrix_mag, mag_max, matrix_u_v):
    num_row = len(matrix_optical_flow)
    num_col = len(matrix_optical_flow[0])
    matrix_visualization = np.zeros((num_row, num_col, 3), np.float32)
    matrix_arrows = np.zeros((num_row, num_col, 3), np.float32)
    for i in range(num_row):
        for j in range(num_col):
            num = matrix_mag[i][j] / mag_max
            matrix_visualization[i][j][0] = (matrix_mag[i][j] * matrix_optical_flow[i][j])
            matrix_visualization[i][j][1] = (matrix_mag[i][j] * (1 - matrix_optical_flow[i][j]))
            if i % 6 == 0 and j % 6 == 0:
                cv2.arrowedLine(matrix_arrows, (j, i), (int(j + (matrix_u_v[i][j][0] * num * 15)), int(i + (matrix_u_v[i][j][1] * num * 15))), (0, 255, 0))

    return matrix_visualization, matrix_arrows


def Main():
    image1_name = "tree1.jpg"
    image2_name = "tree2.jpg"
    image1 = cv2.imread(image1_name)
    width = int(image1.shape[1] * 2)
    height = int(image1.shape[0] * 2)
    dimension = (width, height)
    resized_image1 = cv2.resize(image1, dimension, interpolation=cv2.INTER_AREA)
    gray_image1 = cv2.cvtColor(resized_image1, cv2.COLOR_BGR2GRAY)
    image2 = cv2.imread(image2_name)
    resized_image2 = cv2.resize(image2, dimension, interpolation=cv2.INTER_AREA)
    gray_image2 = cv2.cvtColor(resized_image2, cv2.COLOR_BGR2GRAY)
    ix_ix, iy_iy, it, iy_it, ix_it, ix_iy = gather_data(gray_image1, gray_image2)
    matrix_optical_flow, matrix_mag, mag_max, matrix_u_v, x_optical_flow, y_optical_flow = calculate(ix_ix, iy_iy, iy_it, ix_it, ix_iy)
    flow_visualization, arrow_visualization = visualize(matrix_optical_flow, matrix_mag, mag_max, matrix_u_v)
    #cv2.imwrite("x_optical_flow.jpg", x_optical_flow * 255)
    #cv2.imwrite("y_optical_flow.jpg", y_optical_flow * 255)
    #cv2.imwrite("magnitude.jpg", matrix_mag * 255)
    cv2.imwrite("flow_visualization_tree.jpg", flow_visualization * 255)
    cv2.imwrite("arrow_visualization_tree.jpg", arrow_visualization * 255)


Main()
