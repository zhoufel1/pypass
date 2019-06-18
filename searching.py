#!/usr/bin/env python3


def edit_distance(source: str, target: str) -> int:
    """
    Return an integer representing the edit distance, that is the
    Levenshtein distance coefficient, between the <source> string
    and the <target> string.
    """

    len_s = len(source)
    len_t = len(target)

    # Build an empty matrix
    distance = [[0 for x in range(len_t + 1)] for y in range(len_s + 1)]

    # Build the first row and column
    for i in range(1, len_s + 1):
        distance[i][0] = i
    for j in range(1, len_t + 1):
        distance[0][j] = j

    # Calculate the diagonal
    for i in range(1, len_s + 1):
        for j in range(1, len_t + 1):
            if source[i - 1] == target[j - 1]:
                cost = 0
            else:
                cost = 1
            distance[i][j] = min(distance[i - 1][j] + 1,
                                 distance[i][j - 1] + 1,
                                 distance[i - 1][j - 1] + cost)
    return distance[len_s][len_t]


def is_found(source: str, target: str) -> bool:
    """Use the edit distance to fuzzy search
    for <source> in <target>. Return True if <source> is
    found, False otherwise."""

    for i in range(len(target)):
        if source[0] == target[i] and len(target) - i - 1 >= len(source) - 1:
            # Calculate levenshtein for the snippet in target to source
            snippet = target[i:i+len(source)]
            if edit_distance(source, snippet) <= len(source) // 2:
                return True
    if len(source) - 1 > 4:
        return is_found(source[1:], target)
    return False


if __name__ == '__main__':
    pass
