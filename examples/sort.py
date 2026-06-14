from random import randint
from time import perf_counter


def max(list):
    biggest_current = None
    for item in list:
        if biggest_current is None:
            biggest_current = item
        elif item > biggest_current:
            biggest_current = item
    return biggest_current


def sort(list):
    sorted = []
    for item in range(len(list)):
        sorted.append(max(list))
        list.remove(max(list))
    print(sorted)
    return sorted


if __name__ == "__main__":
    l = []
    for _ in range(10000):
        l.append(randint(0, 10000))
    start = perf_counter()
    sort(l)
    end = perf_counter()
    print(f"Time taken: {end - start} seconds")
