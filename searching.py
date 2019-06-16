#!/usr/bin/env python3


def levenshtein_distance(source: str, target: str) -> int:
    """Return an integer reprsenting the Levenshtein distance between the
    the <source> string and the <target> string."""

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


if __name__ == '__main__':
    pass
