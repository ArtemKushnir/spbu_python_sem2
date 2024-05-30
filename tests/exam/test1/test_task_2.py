import random

import hypothesis.strategies as st
import numpy as np
import pytest
from hypothesis import assume, given

from src.exam.test1.task_2 import *


class TestVector:
    @staticmethod
    def get_random_list(size):
        return [random.randint(0, 100) for i in range(size)]

    @given(st.integers(0, 10000))
    def test_dimension(self, test_length):
        random_list = self.get_random_list(test_length)
        vector = Vector(random_list)
        assert len(vector) == test_length

    @given(st.integers(0, 10000))
    def test_add(self, test_length):
        random_list1 = self.get_random_list(test_length)
        vector1 = Vector(random_list1)
        random_list2 = self.get_random_list(test_length)
        vector2 = Vector(random_list2)
        assert (vector1 + vector2).coordinates == list(np.array(random_list1) + np.array(random_list2))

    @given(st.integers(0, 10000))
    def test_sub(self, test_length):
        random_list1 = self.get_random_list(test_length)
        vector1 = Vector(random_list1)
        random_list2 = self.get_random_list(test_length)
        vector2 = Vector(random_list2)
        assert (vector1 - vector2).coordinates == list(np.array(random_list1) - np.array(random_list2))

    @given(st.integers(0, 10000))
    def test_scalar_product(self, test_length):
        random_list1 = self.get_random_list(test_length)
        vector1 = Vector(random_list1)
        random_list2 = self.get_random_list(test_length)
        vector2 = Vector(random_list2)
        assert vector1.scalar_product(vector2) == np.dot(random_list1, random_list2)

    @given(
        st.lists(st.integers(0, 1000), min_size=3, max_size=3), st.lists(st.integers(0, 1000), min_size=3, max_size=3)
    )
    def test_vector_product(self, random_list1, random_list2):
        vector1 = Vector(random_list1)
        vector2 = Vector(random_list2)
        assert (vector1.vector_product(vector2)).coordinates == list(np.cross(random_list1, random_list2))

    @pytest.mark.parametrize(
        "list,expected", [([1, 2, 9, 100], False), ([0, 0], True), ([1], False), ([0, 0, 0, 0, 0, 0], True)]
    )
    def test_is_null(self, list, expected):
        vector = Vector(list)
        assert vector.is_null() == expected

    @given(st.integers(0, 10000))
    def test_commutativity_add(self, test_length):
        random_list1 = self.get_random_list(test_length)
        vector1 = Vector(random_list1)
        random_list2 = self.get_random_list(test_length)
        vector2 = Vector(random_list2)
        assert (vector1 + vector2).coordinates == (vector2 + vector1).coordinates

    @given(st.integers(0, 100), st.integers(101, 1000))
    def test_raise_exception_add(self, length1, length2):
        random_list1 = self.get_random_list(length1)
        vector1 = Vector(random_list1)
        random_list2 = self.get_random_list(length2)
        vector2 = Vector(random_list2)
        with pytest.raises(DifferentDimensions):
            vector1 + vector2

    @given(st.integers(0, 100), st.integers(101, 1000))
    def test_raise_exception_sub(self, length1, length2):
        random_list1 = self.get_random_list(length1)
        vector1 = Vector(random_list1)
        random_list2 = self.get_random_list(length2)
        vector2 = Vector(random_list2)
        with pytest.raises(DifferentDimensions):
            vector1 - vector2

    @given(st.integers(0, 100), st.integers(101, 1000))
    def test_raise_exception_scalar_product(self, length1, length2):
        random_list1 = self.get_random_list(length1)
        vector1 = Vector(random_list1)
        random_list2 = self.get_random_list(length2)
        vector2 = Vector(random_list2)
        with pytest.raises(DifferentDimensions):
            vector1.scalar_product(vector2)

    @given(st.integers(0, 100), st.integers(101, 1000))
    def test_raise_exception_vector_product(self, length1, length2):
        random_list1 = self.get_random_list(length1)
        vector1 = Vector(random_list1)
        random_list2 = self.get_random_list(length2)
        vector2 = Vector(random_list2)
        with pytest.raises(DifferentDimensions):
            vector1.vector_product(vector2)

    @given(st.integers(0, 1000))
    def test_raise_exception_vector_product2(self, test_length):
        assume(test_length != 3)
        random_list1 = self.get_random_list(test_length)
        vector1 = Vector(random_list1)
        random_list2 = self.get_random_list(test_length)
        vector2 = Vector(random_list2)
        with pytest.raises(IncorrectDimension):
            vector1.vector_product(vector2)
