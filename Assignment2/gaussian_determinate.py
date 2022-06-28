def gaussianDeterminate(matrix):
    print("\ngaussianElimination")
    max_column = len(matrix[0]) - 2
    max_row = len(matrix) - 1
    swap_count = 0
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
            swap_count = swap_count + 1

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
    p = matrix[1][1]
    m = matrix[0][0]

    deta = ((-1) ** swap_count) * r * p * m


    print("\nAfter Det(A):")
    print("determinate = ", deta)



def Main():
    matrix = [[1, 4, 0], [0, 2, 6], [1, 0, 1]]
    gaussianDeterminate(matrix)


Main()
