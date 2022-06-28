def createAugmentedMatrix(matrix, vector):
    """
    Accepts nxn matrix and n*1 vector to create an augmented matrix.
    :param a: (list list) n*n matrix
    :param b: (list list) n*1 vector
    :return result: (list list) augmented matrix
    """
    if len(matrix[0]) != len(vector):
        print("The matrix and vector cannot be combined.")
    else:
        print("The matrix and vector can be combined!\n")
        print("Matrix:")
        for row in matrix:
            print(row)
        print("\nVector:")
        for row in vector:
            print(row)

        index = 0
        print("\nAugmented Matrix:")
        for row in matrix:

            row.append(vector[index][0])
            print(row)
            index = index + 1

        return matrix


def gaussJordanElimination(aug_matrix):
    """
    Takes and augmented matrix and solves it using the gauss-jordan elimination method
    :param aug_matrix:
    :return aug_matrix:
    """
    print("\ngaussJordanElimination")
    max_column = len(aug_matrix[0]) - 2
    max_row = len(aug_matrix) - 1
    print("\nMax column: ", max_column)
    print("Max row: ", max_row)
    # changed max_column to 0 for testing, change back when done
    for col in range(0, max_column + 1):
        print("\n###Operations for column: ", col, "###")
        # set mag to the diagonal value with the largest magnitude in the current column
        mag = abs(aug_matrix[col][col])
        new_mag = False
        # set the pivot row to be the row containing the diagonal
        pivot_row = col
        # iterate over a range from current col to max num of rows
        for row in range(col, max_row + 1):
            # if the current value is larger than the mag
            if abs(aug_matrix[row][col]) > mag:
                # set row with highest magnitude to current row
                # set mag to value of new highest magnitude value in current col
                mag_row = row
                mag = abs(aug_matrix[row][col])
                new_mag = True
        # swap the pivot_row with the mag_row, found with prev for loop if new mag was found
        if new_mag:
            aug_matrix[mag_row], aug_matrix[pivot_row] = aug_matrix[pivot_row], aug_matrix[mag_row]


        print("\nAfter swapping rows:")
        for row in aug_matrix:
            print(row)


        # set row to be divided as the row containing the diagonal
        row_divide = aug_matrix[col]
        # set the value to divide the row by as the first diagonal value in the row
        divideby = row_divide[col]
        count = 0
        # iterate over numbers in row to divided and set the corresponding value in aug_matrix to number/divideby
        for num in row_divide:
            if num == 0.0:
                aug_matrix[col][count] = 0.0
            else:
                aug_matrix[col][count] = num / divideby
            count = count + 1


        print("\nAfter dividing swapped row:")
        for row in aug_matrix:
            print(row)


        # iterate over each row in column
        for row in range(0, max_column + 1):
            if aug_matrix[row] != aug_matrix[pivot_row]:
                multby = aug_matrix[row][col]
                count = 0
                for num in aug_matrix[row]:
                    aug_matrix[row][count] = num - (multby * aug_matrix[pivot_row][count])
                    count = count + 1


        print("\nAfter Subtract rows:")
        for row in aug_matrix:
            print(row)

    for i in range(0, len(aug_matrix)):
        for j in range(0, len(aug_matrix[i])):
            aug_matrix[i][j] = format(aug_matrix[i][j], '.2g')


    # test print to print out current state of the matrix
    print("\nResult:")
    for row in aug_matrix:
        print(row)

    print("\nx = ", aug_matrix[0][len(aug_matrix[0]) - 1])
    print("y = ", aug_matrix[1][len(aug_matrix[0]) - 1])
    print("z = ", aug_matrix[2][len(aug_matrix[0]) - 1])


def Main():
    matrix = [[1.0, 0.0, 2.0], [2.0, -1.0, 3.0], [4.0, 1.0, 8.0]]
    vector = [[1.0], [-1.0], [2.0]]
    #matrix3 = [[1, -1, 0], [-2, 2, -2], [0, 1, -2]]

    # create an augmented matrix given n*n matrix and n*1 vector
    augMatrix = createAugmentedMatrix(matrix, vector)
    gaussJordanElimination(augMatrix)


Main()
