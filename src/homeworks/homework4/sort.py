import random
import time
from argparse import ArgumentParser
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from math import ceil
from typing import Callable

from matplotlib import pyplot as plt

THREAD_POOL = ThreadPoolExecutor
PROCESS_POOL = ProcessPoolExecutor


class MergeSort:
    @staticmethod
    def merge(left: list[int], right: list[int]) -> list[int]:
        result = []
        while left and right:
            if left[0] >= right[0]:
                result.append(right[0])
                right.pop(0)
            else:
                result.append(left[0])
                left.pop(0)
        if left:
            result.extend(left)
        if right:
            result.extend(right)
        return result

    def base_sort(self, array: list[int]) -> list[int]:
        if len(array) <= 1:
            return array
        mid = len(array) // 2
        left = self.base_sort(array[:mid])
        right = self.base_sort(array[mid:])
        return self.merge(left, right)

    def parallel_sort(self, array: list[int], n_jobs: int, executor_pool: Callable) -> list[int]:
        task_per_worker = ceil(len(array) / n_jobs)
        task_per_worker = task_per_worker if task_per_worker else 1
        sublist = (array[i : i + task_per_worker] for i in range(0, len(array), task_per_worker))
        with executor_pool(max_workers=n_jobs) as executor:
            results = executor.map(self.base_sort, sublist)
            merged: list[int] = []
            for sort_sublist in results:
                merged = self.merge(merged, sort_sublist)
        return merged


def check_time(func: Callable) -> Callable:
    def inner(*args: int, **kwargs: int) -> float:
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        return end - start

    return inner


def main(size_arr: int, num_threads: list[int], output_path: str, multiprocess: bool) -> None:
    sort = MergeSort()
    parallel_sort_time: list[float] = []

    random_arr = [random.randint(0, 100000) for _ in range(size_arr)]
    for cnt_threads in num_threads:
        sort_time = check_time(sort.parallel_sort)(random_arr, cnt_threads, PROCESS_POOL if multiprocess else THREAD_POOL)
        parallel_sort_time.append(sort_time)
    base_sort_time = [check_time(sort.base_sort)(random_arr)] * len(parallel_sort_time)

    if multiprocess:
        plt.plot(num_threads, parallel_sort_time, label="process")
    else:
        plt.plot(num_threads, parallel_sort_time, label="threads")
    plt.plot(num_threads, base_sort_time, label="base")
    plt.legend()
    plt.xlabel("num-threads")
    plt.ylabel("time")
    plt.title(f"sorting time for an array of size {size_arr}")
    plt.savefig(output_path)


if __name__ == "__main__":
    argparser = ArgumentParser(description="Multithread and multiprocess sort")
    argparser.add_argument("size_arr", type=int, help="the size of the array to sort")
    argparser.add_argument("num_threads", nargs="+", type=int, help="number of threads to sort")
    argparser.add_argument("output_path", type=str)
    argparser.add_argument("--multiprocess", action="store_true", help="use processes instead of threads")
    my_args = argparser.parse_args()
    main(**vars(my_args))
