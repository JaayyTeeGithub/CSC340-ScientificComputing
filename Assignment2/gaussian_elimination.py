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


def gaussianElimination(matrix):
    print("\ngaussianElimination")
    max_column = len(matrix[0]) - 2
    max_row = len(matrix) - 1
    print("\nMax column: ", max_column)
    print("Max row: ", max_row)

    for col in range(0, len(matrix)):

        # set mag to the diagonal with the largest magnitude in current column
        mag = abs(matrix[col][col])
        # set the pivot row to the row containing the diagonal
        pivot_row = col
        new_mag = False
        mag_row = col
        for row in range(col, len(matrix)):
            if abs(matrix[row][col]) > mag:
                mag = abs(matrix[row][col])
                mag_row = row
                new_mag = True

        if new_mag:
            matrix[mag_row], matrix[pivot_row] = matrix[pivot_row],  matrix[mag_row]


        print("\nAfter swapping rows:")
        for row in matrix:
            print(row)

        for row in range(col + 1, len(matrix)):
            multby = matrix[row][col] / matrix[col][col]
            count = 0
            for num in matrix[row]:
                matrix[row][count] = num - (multby * matrix[pivot_row][count])
                count = count + 1

        print("\nAfter Subtract rows:")
        for row in matrix:
            print(row)


    r = matrix[2][2]
    u = matrix[2][3]
    p = matrix[1][1]
    q = matrix[1][2]
    t = matrix[1][3]
    m = matrix[0][0]
    n = matrix[0][1]
    v = matrix[0][2]
    s = matrix[0][3]

    z = u / r
    y = (t - (q * z)) / p
    x = (s - ((n * y) + (v * z))) / m

    print("\nAfter Back Substitution:")
    print("x = ", x)
    print("y = ", y)
    print("z = ", z)









def Main():
    matrix = [[1.0, 0.0, 2.0], [2.0, -1.0, 3.0], [4.0, 1.0, 8.0]]
    vector = [[1.0], [-1.0], [2.0]]
    augMatrix2 = createAugmentedMatrix(matrix, vector)
    gaussianElimination(augMatrix2)


Main()
