import random
import statistics
import time
from argparse import ArgumentParser
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from math import ceil, log2
from typing import Callable, MutableSequence

from matplotlib import pyplot as plt


class MergeSort:
    @staticmethod
    def merge(left: MutableSequence[int], right: MutableSequence[int]) -> list[int]:
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

    def supporting_func(self, array_to_merge: tuple[list[int], list[int]]) -> list[int]:
        return self.merge(array_to_merge[0], array_to_merge[1])

    def parallel_sort_second_implementation(self, array: list[int], n_jobs: int, pool_executor: Callable) -> list[int]:
        depth = log2(n_jobs)

        def parallel_recursion(curr_array: list[int], curr_depth: int) -> list[int]:
            if n_jobs < 2 or curr_depth > depth:
                return self.base_sort(curr_array)
            middle = len(curr_array) // 2
            left = executor.submit(parallel_recursion, curr_array[:middle], depth + 1)
            right = executor.submit(parallel_recursion, curr_array[middle:], depth + 1)
            return self.merge(left.result(), right.result())

        with pool_executor(max_workers=n_jobs) as executor:
            return parallel_recursion(array, n_jobs)

    def parallel_sort_first_implementation(self, array: list[int], n_jobs: int, pool_executor: Callable) -> list[int]:
        task_per_worker = ceil(len(array) / n_jobs)
        task_per_worker = task_per_worker if task_per_worker else 1
        sublist = (array[i : i + task_per_worker] for i in range(0, len(array), task_per_worker))
        with pool_executor(max_workers=n_jobs) as executor:
            results: list[int] = []
            for curr_array in executor.map(self.base_sort, sublist):
                results = self.merge(results, curr_array)
        return results


def check_time(func: Callable, n_iter: int) -> Callable:
    def inner(*args: int, **kwargs: int) -> float:
        sort_time = []
        for i in range(n_iter):
            start = time.perf_counter()
            func(*args, **kwargs)
            end = time.perf_counter()
            sort_time.append(end - start)
        return statistics.mean(sort_time)

    return inner


def main(size_arr: int, num_threads: list[int], output_path: str, multiprocess: bool) -> None:
    sort = MergeSort()
    parallel_sort_time: list[float] = []

    random_arr = [random.randint(0, 100000) for _ in range(size_arr)]
    for cnt_threads in num_threads:
        sort_time = check_time(sort.parallel_sort_second_implementation, 10)(
            random_arr, cnt_threads, ProcessPoolExecutor if multiprocess else ThreadPoolExecutor
        )
        parallel_sort_time.append(sort_time)
    base_sort_time = [check_time(sort.base_sort, 3)(random_arr)] * len(parallel_sort_time)

    if multiprocess:
        worker = "process"
    else:
        worker = "thread"
    plt.plot(num_threads, parallel_sort_time, label=worker)
    plt.plot(num_threads, base_sort_time, label="base")
    plt.legend()
    plt.xlabel("num-threads")
    plt.ylabel("time")
    plt.title(f"size_array: {size_arr}")
    plt.savefig(output_path)


if __name__ == "__main__":
    argparser = ArgumentParser(description="Multithread and multiprocess sort")
    argparser.add_argument("size_arr", type=int, help="the size of the array to sort")
    argparser.add_argument("num_threads", nargs="+", type=int, help="number of threads to sort")
    argparser.add_argument("output_path", type=str)
    argparser.add_argument("--multiprocess", action="store_true", help="use processes instead of threads")
    my_args = argparser.parse_args()
    main(**vars(my_args))
