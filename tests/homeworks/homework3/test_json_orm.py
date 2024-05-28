import hypothesis.strategies as st
import pytest
from hypothesis import given

from src.homeworks.homework3.dtclass_to_api import *


@dataclass
class B(ORM):
    b1: int
    b2: int


@dataclass
class A(ORM):
    a1: str
    a2: int
    b: B


@dataclass
class C(ORM):
    list: list[B]


class TestJsonORM:
    @given(st.integers(), st.integers())
    def test_create_dataclass(self, b1, b2):
        b_dict = {"b1": b1, "b2": b2}
        test_b = B.bind_lazy_dict(b_dict)
        assert test_b.json_dict == b_dict
        assert test_b.b1 == b1 and test_b.b2 == b2

    @given(st.text(), st.text(), st.integers(), st.integers())
    def test_create_dataclass_with_dict(self, a1, a2, b1, b2):
        b_dict = {"b1": b1, "b2": b2}
        a_dict = {"a1": a1, "a2": a2, "b": b_dict}
        test_a = A.bind_lazy_dict(a_dict)
        assert test_a.a1 == a1 and test_a.a2 == a2
        assert isinstance(test_a.b, B)
        assert test_a.b.b1 == b1 and test_a.b.b2 == b2
        assert test_a.json_dict == a_dict

    @given(st.text(), st.text(), st.integers(), st.integers())
    def test_dump(self, a1, a2, b1, b2):
        b_dict = {"b1": b1, "b2": b2}
        a_dict = {"a1": a1, "a2": a2, "b": b_dict}
        test_a = A.bind_lazy_dict(a_dict)
        assert test_a.dump() == dumps(a_dict) and test_a.b.dump() == dumps(b_dict)

    def test_bind_lazy_dict_exception(self):
        b_dict = {"b1": 1, "b2": 2, "b3": 3}
        with pytest.raises(JsonError):
            B.bind_lazy_dict(b_dict, True)

    def test_parse_args_exception_json_error(self):
        test_b = B(1, 2)
        with pytest.raises(JsonError):
            parse_json_dict_args(test_b, "b1")

    def test_parse_args_exception_attribute_error(self):
        b_dict = {"b1": 1, "b2": 2}
        test_b = B.bind_lazy_dict(b_dict)
        with pytest.raises(JsonAttributeError):
            parse_json_dict_args(test_b, "b3")
