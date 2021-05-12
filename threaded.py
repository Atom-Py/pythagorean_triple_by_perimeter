import math
from multiprocessing import Process, Value, Array
from datetime import datetime


def compute(window, half_perimeter, perimeter, return_list=None, flag=0):
    for m in range(window[0], window[1]):
        print(window, m)
        if half_perimeter % m == 0:
            y = half_perimeter // m
            for n in range(2 if m & 1 else 1, m, 2):
                if return_list is not None and flag.value:
                    return
                sum_mn = m + n
                if y % sum_mn == 0:
                    k = y // sum_mn
                    a = 2 * m * n * k
                    b = (m * m - n * n) * k
                    c = (m * m + n * n) * k
                    if a + b + c == perimeter:
                        if return_list is not None:
                            flag.value = 1
                            for i, v in enumerate(sorted([a, b, c])):
                                return_list[i] = v
                        else:
                            return sorted([a, b, c])
    return list()


def separate(m_max, windows_count):
    diapason = m_max - 2
    window_size = diapason // windows_count
    windows = [[y := 2 + i * window_size, y + window_size] for i in range(windows_count)]
    if (remainder := m_max - windows[-1][1]) > 0:
        index = 0
        while remainder:
            windows[index][1] += 1
            for i in range(index + 1, len(windows)):
                windows[i][0] += 1
                windows[i][1] += 1
            remainder -= 1
            index += 1
    # OPTIMISE THIS!!!
    # windows[0][1] += 200000
    # windows[1][0] += 200000
    return windows


def get_pythagorean_triple_by_perimeter(perimeter: int, *, thread_count: int = 1):
    if perimeter & 1 or perimeter < 12:
        return list()
    half_perimeter = perimeter >> 1
    if half_perimeter >= 16:
        m_max = int(math.sqrt(half_perimeter))
    else:
        m_max = 3
    if thread_count > 1:
        flag = Value('B', 0)
        return_list = Array('d', 3)
        windows = separate(m_max, thread_count)
        procs = list()
        for window in windows:
            proc = Process(target=compute, args=(window, half_perimeter, perimeter, return_list, flag), daemon=True)
            procs.append(proc)
            proc.start()
        for proc in procs:
            proc.join()
        result = list(return_list)
        if result[0] == 0:
            return list()
        return [int(d) for d in result]
    else:
        return compute((2, m_max), half_perimeter, perimeter)


if __name__ == '__main__':
    perimeter = 346546546456456456
    t1 = datetime.now()
    print(get_pythagorean_triple_by_perimeter(perimeter, thread_count=2))
    print(datetime.now() - t1)
