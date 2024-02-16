import pytest
from src.hello_world import main
def test_main():
    actual = main()
    assert actual == "Hello world"