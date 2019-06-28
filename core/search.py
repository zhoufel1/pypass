from typing import List


def edit_distance(source: str, target: str) -> int:
    len_source = len(source)
    len_target = len(target)

    distance_matrix = build_empty_matrix(len_source, len_target)
    build_first_row_col(len_source, len_target, distance_matrix)
    calculate_diagonal(len_source, len_target, distance_matrix, source, target)

    return distance_matrix[len_source][len_target]


def build_empty_matrix(row: int, col: int) -> List[list]:
    return [[0 for x in range(col + 1)]
            for y in range(row + 1)]


def build_first_row_col(row: int, col: int, matrix: List[list]) -> None:
    for i in range(1, row + 1):
        matrix[i][0] = i
    for j in range(1, col + 1):
        matrix[0][j] = j


def calculate_diagonal(row: int,
                       col: int,
                       matrix: List[list],
                       source: str,
                       target: str) -> None:
    for i in range(1, row + 1):
        for j in range(1, col + 1):
            if source[i - 1] == target[j - 1]:
                cost = 0
            else:
                cost = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1,
                               matrix[i][j - 1] + 1,
                               matrix[i - 1][j - 1] + cost)


def is_found(source: str, target: str) -> bool:
    for i in range(len(target)):
        if source[0] == target[i] and len(target) - i - 1 >= len(source) - 1:
            snippet = target[i:i + len(source)]
            if edit_distance(source, snippet) <= len(source) // 2:
                return True
    if len(source) - 1 > 4:
        return is_found(source[1:], target)
    return False