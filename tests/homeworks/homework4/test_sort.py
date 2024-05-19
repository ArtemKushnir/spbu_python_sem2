import hypothesis.strategies as st
from hypothesis import given, settings

from src.homeworks.homework4.sort import PROCESS_POOL, THREAD_POOL, MergeSort


class TestMergeSort:
    sort = MergeSort()

    @given(st.lists(st.integers()), st.lists(st.integers()))
    def test_merge(self, left_array, right_array):
        left_array.sort()
        right_array.sort()
        expected = left_array + right_array
        expected.sort()
        actual = self.sort.merge(left_array, right_array)
        assert actual == expected

    @given(st.lists(st.integers()))
    def test_base_sort(self, test_array):
        actual = self.sort.base_sort(test_array)
        test_array.sort()
        assert actual == test_array

    @given(st.lists(st.integers()), st.integers(1, 1000))
    def test_thread_sort_first_realisation(self, test_array, n_jobs):
        actual = self.sort.parallel_sort_first_realisation(test_array, n_jobs, THREAD_POOL)
        test_array.sort()
        assert actual == test_array

    @given(st.lists(st.integers()), st.integers(1, 100))
    @settings(deadline=10**10)
    def test_process_sort_first_realisation(self, test_array, n_jobs):
        actual = self.sort.parallel_sort_first_realisation(test_array, n_jobs, PROCESS_POOL)
        test_array.sort()
        assert actual == test_array

    @given(st.lists(st.integers()), st.integers(1, 1000))
    def test_thread_sort_second_realisation(self, test_array, n_jobs):
        actual = self.sort.parallel_sort_second_realisation(test_array, n_jobs, THREAD_POOL)
        test_array.sort()
        assert actual == test_array

    @given(st.lists(st.integers()), st.integers(1, 100))
    @settings(deadline=10**10)
    def test_process_sort_second_realisation(self, test_array, n_jobs):
        actual = self.sort.parallel_sort_second_realisation(test_array, n_jobs, PROCESS_POOL)
        test_array.sort()
        assert actual == test_array
