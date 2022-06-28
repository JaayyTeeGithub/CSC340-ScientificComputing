import cv2
import numpy as np

# read image1
image1 = cv2.imread("cones1.png")
# show image1
cv2.imshow("Displaying image1", image1)
# determine and print image1 size
numRows = image1.shape[0]
numCols = image1.shape[1]
print("image1 size: ", numRows, numCols)
# determine and print image2 size with scaling factor of 1.5
size1 = numRows * 1.5
size2 = numCols * 1.5
print("image2 size: ", size1, size2)
# create empty image2 with predetermined size
image2 = np.zeros((int(size1), int(size2), 3), np.float32)
# determine the offset needed to center image1 within image2
i_offset = (size1 - numRows)/2
j_offset = (size2 - numCols)/2
# iterate over image1 and place it in image2 using predetermined offset
for i in range(numRows):
    for j in range(numCols):
        image2[int(i + i_offset)][int(j + j_offset)][0] = image1[i][j][0]
        image2[int(i + i_offset)][int(j + j_offset)][1] = image1[i][j][1]
        image2[int(i + i_offset)][int(j + j_offset)][2] = image1[i][j][2]

# display image2
cv2.imshow("Displaying image2", image2/255.0)
cv2.waitKey(0)
cv2.destroyAllWindows()

# save image2
cv2.imwrite("savedImage.png", image2)
print("saved")