import math


def make_int_array_from_string(string):
    string_array = string.split(" ")
    return [float(num) for num in string_array]


def dot_multiply(row, column):
    result = 0
    for i in range(len(row)):
        result += row[i] * column[i]
    return result


def remove_column(matrix, column):
    answer_matrix = [element * 1 for element in matrix]
    for row in answer_matrix:
        row.pop(column)
    answer_matrix.pop(0)
    return answer_matrix


class Matrix:
    def __init__(self, row_count, column_count):
        self.row_count = row_count
        self.column_count = column_count
        self.matrix = list()

    def create_matrix_from_input(self):
        matrix = []
        for row in range(self.row_count):
            row_array = make_int_array_from_string(input())
            matrix.append(row_array)
        self.matrix = matrix

    def set_matrix_list(self, array):
        self.matrix = array

    def render_matrix(self):
        for row in self.matrix:
            string = " "
            print(string.join([str(element) for element in row]))

    def remove_column_at_row(self, column, row):

        answer_matrix = [element * 1 for element in self.matrix]
        for row_item in answer_matrix:
            row_item.pop(column)
        answer_matrix.pop(row)
        matrix_object = Matrix(row - 1, column - 1)
        matrix_object.set_matrix_list(answer_matrix)
        return matrix_object

    def add_matrix(self, matrix_b):
        if len(self.matrix) != len(matrix_b.matrix):
            return "ERROR"
        if len(self.matrix[0]) != len(matrix_b.matrix[0]):
            return "ERROR"

        for row_index in range(self.row_count):
            for item_index in range(self.column_count):
                self.matrix[row_index][item_index] += matrix_b.matrix[row_index][item_index]

    def multiply_by_constant(self, constant):
        self.matrix = [[0 if element == 0 else round(constant * element, 4) for element in row] for row in self.matrix]

    def main_diagonal_transpose(self):
        new_matrix = Matrix(self.column_count, self.row_count)
        columns_result = []
        for index in range(self.column_count):
            individual_column = []
            for row in range(self.row_count):
                individual_column.append(self.matrix[row][index])
            columns_result.append(individual_column)
        new_matrix.set_matrix_list(columns_result)
        return new_matrix

    def side_diagonal_transpose(self):
        new_matrix = Matrix(self.column_count, self.row_count)
        old_matrix = self.matrix
        old_matrix.reverse()
        columns_result = []
        for index in range(self.column_count):
            individual_column = []
            for row in range(self.row_count):
                individual_column.append(old_matrix[row][index])
            columns_result.append(individual_column)
        columns_result.reverse()
        new_matrix.set_matrix_list(columns_result)
        return new_matrix

    def vertical_line_transpose(self):
        matrix_list = self.matrix
        for row in matrix_list:
            row.reverse()
        result_matrix = Matrix(self.row_count, self.column_count)
        result_matrix.set_matrix_list(matrix_list)
        return result_matrix

    def horizontal_line_transpose(self):
        matrix_list = self.matrix
        matrix_list.reverse()
        result_matrix = Matrix(self.row_count, self.column_count)
        result_matrix.set_matrix_list(matrix_list)
        return result_matrix

    def multiply_by_matrix(self, matrix):
        answer_matrix = Matrix(self.row_count, matrix.column_count)
        if self.column_count != matrix.row_count:
            return "ERROR"

        matrix_b_trans = matrix.main_diagonal_transpose()
        result = []
        for row in self.matrix:
            new_row = []
            for column in matrix_b_trans.matrix:
                entry = dot_multiply(row, column)
                new_row.append(entry)
            result.append(new_row)
        answer_matrix.set_matrix_list(result)
        return answer_matrix

    def calculate_determinant(self):
        matrix = self.matrix
        if len(matrix) == 1:
            return matrix[0][0]
        elif len(matrix) == 2:
            return (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])
        else:
            row_1 = matrix[0]
            answer = 0
            for i in range(len(row_1)):
                further = remove_column(matrix, i)
                further_matrix = Matrix(len(matrix) - 1, len(row_1) - 1)
                further_matrix.set_matrix_list(further)
                element = row_1[i]
                answer += (element * ((-1) ** i) * further_matrix.calculate_determinant())
            return answer

    def invert(self):
        if self.calculate_determinant() == 0:
            return "ERROR"
        second_matrix = Matrix(self.row_count, self.column_count)
        second_matrix_list = []
        for i in range(self.row_count):
            new_row = []
            for j in range(self.column_count):
                new_element = (-1) ** (i + j + 2) * (self.remove_column_at_row(j, i)).calculate_determinant()
                new_row.append(new_element)
            second_matrix_list.append(new_row)
        second_matrix.set_matrix_list(second_matrix_list)
        second = second_matrix.main_diagonal_transpose()
        second.multiply_by_constant(1 / self.calculate_determinant())
        return second


def receive_menu_option():
    print('1. Add matrices')
    print('2. Multiply matrix by a constant')
    print('3. Multiply matrices')
    print('4. Transpose matrix')
    print('5. Calculate a determinant')
    print('6. Inverse matrix')
    print('0. Exit')
    return input('Your choice: ')


def menu_option_add():
    row, space, column = input('Enter size of first matrix: ')
    matrix_a = Matrix(int(row), int(column))
    matrix_a.create_matrix_from_input()

    row2, space, column2 = input('Enter size of second matrix: ')
    matrix_b = Matrix(int(row2), int(column2))
    matrix_b.create_matrix_from_input()
    matrix_a.add_matrix(matrix_b)

    print('The result is:')
    matrix_a.render_matrix()


def menu_option_cons():
    row, space, column = input('Enter size of matrix: ')
    matrix_a = Matrix(int(row), int(column))
    matrix_a.create_matrix_from_input()
    const = float(input('Enter constant: '))
    matrix_a.multiply_by_constant(const)

    print('The result is:')
    matrix_a.render_matrix()


def menu_option_mult():
    row, space, column = input('Enter size of first matrix: ')
    matrix_a = Matrix(int(row), int(column))
    matrix_a.create_matrix_from_input()

    row2, space, column2 = input('Enter size of second matrix: ')
    matrix_b = Matrix(int(row2), int(column2))
    matrix_b.create_matrix_from_input()

    answer = matrix_a.multiply_by_matrix(matrix_b)
    print('The result is: ')
    answer.render_matrix()


def menu_option_transpose():
    print('1. Main diagonal')
    print('2. Side diagonal')
    print('3. Vertical line')
    print('4. Horizontal line')

    choice = input('Your choice: ')
    row, space, column = input('Enter size of matrix: ')
    matrix = Matrix(int(row), int(column))
    print('Enter matrix: ')
    matrix.create_matrix_from_input()
    answer = None
    if choice == '1':
        answer = matrix.main_diagonal_transpose()
    if choice == '2':
        answer = matrix.side_diagonal_transpose()
    if choice == '3':
        answer = matrix.vertical_line_transpose()
    if choice == '4':
        answer = matrix.horizontal_line_transpose()

    print('The result is:')
    answer.render_matrix()


def menu_option_determinant():
    row, space, column = input('Enter size of matrix: ')
    matrix = Matrix(int(row), int(column))
    matrix.create_matrix_from_input()
    answer = matrix.calculate_determinant()
    print('The result is: ')
    print(answer)


def menu_option_inverse():
    row, space, column = input('Enter size of matrix: ')
    matrix = Matrix(int(row), int(column))
    matrix.create_matrix_from_input()
    result_matrix = matrix.invert()
    if result_matrix == 'ERROR':
        print("This matrix doesn't have an inverse.")
    else:
        print('The result is: ')
        Matrix.render_matrix(result_matrix)


def main():
    user_input = receive_menu_option()
    while user_input != '0':
        if user_input == '1':
            menu_option_add()
        if user_input == '2':
            menu_option_cons()
        if user_input == '3':
            menu_option_mult()
        if user_input == '4':
            menu_option_transpose()
        if user_input == '5':
            menu_option_determinant()
        if user_input == '6':
            menu_option_inverse()
        print()
        user_input = receive_menu_option()


main()
