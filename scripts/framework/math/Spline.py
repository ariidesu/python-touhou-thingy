import numpy


class CubicSpline:
    def __init__(self, characteristic_matrix: numpy.ndarray):
        self.characteristic_matrix = characteristic_matrix

    def curve(self, points: [numpy.ndarray, ...], u):
        points = [2 * points[0] - points[1]] + \
            points + [2 * points[-1] - points[-2]]

        if u % 1 == 0:
            t = 1
            n = int(u) - 1
        else:
            t = u % 1
            n = int(u)

        p_matrix_x = numpy.array([
            [points[0 + n][0]],
            [points[1 + n][0]],
            [points[2 + n][0]],
            [points[3 + n][0]]
        ])

        p_matrix_y = numpy.array([
            [points[0 + n][1]],
            [points[1 + n][1]],
            [points[2 + n][1]],
            [points[3 + n][1]]
        ])

        t_matrix = numpy.array([1, t, t * t, t * t * t])

        coefficient_matrix_x = numpy.matmul(
            self.characteristic_matrix, p_matrix_x)
        coefficient_matrix_y = numpy.matmul(
            self.characteristic_matrix, p_matrix_y)

        part_x = numpy.matmul(numpy.rot90(coefficient_matrix_x), t_matrix)[0]
        part_y = numpy.matmul(numpy.rot90(coefficient_matrix_y), t_matrix)[0]

        return numpy.array([part_x, part_y])


class BasisSpline(CubicSpline):
    def __init__(self):
        characteristic_matrix = numpy.array([
            [1 / 6, 2 / 3, 1 / 6, 0],
            [-.5, 0, .5, 0],
            [.5, -1, .5, 0],
            [-1 / 6, .5, -.5, 1 / 6]
        ])
        super().__init__(characteristic_matrix)
