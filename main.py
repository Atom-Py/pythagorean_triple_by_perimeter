import math


def get_pythagorean_triple_by_perimeter(perimeter: int):
    if perimeter & 1 or perimeter < 12:
        return tuple()
    half_perimeter = perimeter >> 1
    if half_perimeter >= 16:
        m_max = int(math.sqrt(half_perimeter))
    else:
        m_max = 3
    for m in range(2, m_max):
        if half_perimeter % m == 0:
            y = half_perimeter // m
            for n in range(2 if m & 1 else 1, m, 2):
                sum_mn = m + n
                if y % sum_mn == 0:
                    k = y // sum_mn
                    a = 2 * m * n * k
                    b = (m * m - n * n) * k
                    c = (m * m + n * n) * k
                    if a + b + c == perimeter:
                        return tuple(sorted([a, b, c]))
    return tuple()
