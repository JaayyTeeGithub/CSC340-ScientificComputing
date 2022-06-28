def gaussJordanInversion(matrix):
    print("\ngaussJordanInversion")
    print("Starting Augmented Matrix: ")
    for row in matrix:
        print(row)

    max_column = len(matrix[0]) - 4
    max_row = len(matrix) - 1
    print("\nMax column: ", max_column)
    print("Max row: ", max_row)
    # changed max_column to 0 for testing, change back when done
    for col in range(0, max_column + 1):  ## col = 1
        print("\n###Operations for column: ", col, "###")
        # set mag to the diagonal value with the largest magnitude in the current column
        mag = abs(matrix[col][col])
        new_mag = False
        # set the pivot row to be the row containing the diagonal
        pivot_row = col  ## pivot_row = 1
        # iterate over a range from current col to max num of rows
        for row in range(col, max_row + 1):  ## row = 2, max_row = 3
            # if the current value is larger than the mag
            if abs(matrix[row][col]) > mag:  ## [2][1] = .25

                # set row with highest magnitude to current row
                # set mag to value of new highest magnitude value in current col
                mag_row = row
                mag = abs(matrix[row][col])
                print("mag: ", mag)
                new_mag = True
        # swap the pivot_row with the mag_row, found with prev for loop if new mag was found
        if new_mag:
            matrix[mag_row], matrix[pivot_row] = matrix[pivot_row], matrix[mag_row]


        print("\nAfter swapping rows:")
        for row in matrix:
            print(row)

        # set row to be divided as the row containing the diagonal
        row_divide = matrix[col]
        # set the value to divide the row by as the first diagonal value in the row
        divideby = row_divide[col]
        count = 0
        # iterate over numbers in row to divided and set the corresponding value in aug_matrix to number/divideby

        for num in row_divide:
            if num == 0.0:
                matrix[col][count] = 0.0
            else:
                matrix[col][count] = num / divideby
            count = count + 1

        print("\nAfter dividing swapped row:")
        for row in matrix:
            print(row)

        # iterate over each row in column
        for row in range(0, max_column + 1):
            if matrix[row] != matrix[pivot_row]:
                multby = matrix[row][col]
                count = 0
                for num in matrix[row]:
                    matrix[row][count] = num - (multby * matrix[pivot_row][count])
                    count = count + 1

        print("\nAfter Subtract rows:")
        for row in matrix:
            print(row)
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i])):
            matrix[i][j] = format(matrix[i][j], '.2g')

    # test print to print out current state of the matrix
    print("\nResult:")
    for row in matrix:
        print(row)

    print("\nInverted Matrix:")
    for row in matrix:
        print(row[3:])


def Main():
    matrix2 = [[1, -1, 0, 1, 0, 0], [-2, 2, -1, 0, 1, 0], [0, 1, -2, 0, 0, 1]]
    #matrix2 = [[1, -1, 0, 1, 0, 0], [2, 0, 4, 0, 1, 0], [0, 2, -1, 0, 0, 1]]
    gaussJordanInversion(matrix2)


Main()
