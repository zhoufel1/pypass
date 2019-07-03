"""
This module contains the algorithm used in the program's fuzzy
searcher. It calculates the edit distance the query and items in the
repository and generates a list of items of best match.

The edit (Levenshtein) distance denotes the number of
single character operations (insertion, deletion, substitution)
required to transform the source to the target. We construct a
len(source) * len(target) matrix and calculate the diagonal of
said matrix formed by checking for the deletions, insertions, and
substitutions needed.

For example, given "carrot" and "carry", we note it
takes a deletion of "t" and a substitution of "y" for
"o" to transform the source to the target, so the
edit distance is 2. The corresponding matrix is:

                    C  A  R  R  Y
                 0  1  2  3  4  5
               C 1  0  1  2  3  4
               A 2  1  0  1  2  3
               R 3  2  1  0  1  2
               R 4  3  2  1  0  1
               O 5  4  3  2  1  1
               T 6  5  4  3  2  2

The search algorithm checks for instances in the target
where the source is found, and recursively checks to
said instances up to a sensitivity. The algorithm is
able to check for multiple occurrences in the target
where the source occurs to prevent false non-detections.

For example, given "books" and "www.ourbookstore.com", the
algorithm checks if "books" and "ooks" are in the target.
"""

from typing import List
from constants import SENSITIVITY


def edit_distance(source: str, target: str) -> int:
    len_source, len_target = len(source), len(target)
    distance_matrix = build_empty_matrix(len_source, len_target)
    build_first_row_col(len_source, len_target, distance_matrix)
    calculate_diagonal(len_source, len_target, distance_matrix, source, target)

    return distance_matrix[len_source][len_target]


def build_empty_matrix(row: int, col: int) -> List[list]:
    return [[0 for x in range(col + 1)] for y in range(row + 1)]


def build_first_row_col(row: int, col: int, matrix: List[list]) -> None:
    for i in range(1, row + 1):
        matrix[i][0] = i
    for j in range(1, col + 1):
        matrix[0][j] = j


def calculate_diagonal(row: int, col: int, matrix: List[list],
                       source: str, target: str) -> None:
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
        if source[0] == target[i] and len(target) - 1 - i >= len(source) - 1:
            snippet = target[i:i + len(source)]
            if edit_distance(source, snippet) <= len(source) // 2:
                return True
    if len(source) - 1 > SENSITIVITY:
        return is_found(source[1:], target)
    return False
