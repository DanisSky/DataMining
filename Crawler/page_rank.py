import numpy


def page_rank(matrix, height, G_LIST):
    iteration = 20

    beta = 0.85
    k = (1 - beta) / height

    # Создание вектора
    v_vector = numpy.matrix([1 / height for i in range(height)])

    # Возведение матрицы в стень iteration
    matrix_powed = matrix
    for i in range(iteration):
        matrix_powed.dot(matrix)

    matrix_final = v_vector.dot(matrix_powed).dot(beta)

    e = numpy.ones(height).dot(k)

    # Вектор PageRank'ов
    result = matrix_final + e

    print(result)

    # Топ 5 pageRank
    get_top(result, G_LIST, 5)


def get_top(result, G_list, top):
    a = numpy.sort(result).tolist()[0]

    a = a[-top:]
    b = numpy.argsort(result).tolist()[0][-top:]
    G_list = list(G_list)
    arr = []
    for i in range(top):
        arr.append(
            f"{top - i} {a[i]} {G_list[b[i]]}"
        )

    print('\nPageRank vector sum: ' + str(result.sum()))

    print('top', top)
    arr.reverse()
    for i in arr:
        print(i)
