from typing import Generic, Protocol, TypeVar


class ArithmeticAvailable(Protocol):
    def __add__(self: "T", other: "T") -> "T":
        raise NotImplementedError

    def __sub__(self: "T", other: "T") -> "T":
        raise NotImplementedError

    def __mul__(self: "T", other: "T") -> "T":
        raise NotImplementedError


T = TypeVar("T", bound=ArithmeticAvailable)


class DifferentDimensions(Exception):
    pass


class IncorrectDimension(Exception):
    pass


class Vector(Generic[T]):
    def __init__(self, coordinates: list[T]):
        self.coordinates: list[T] = coordinates

    def __len__(self) -> int:
        return len(self.coordinates)

    def __add__(self, other: "Vector") -> "Vector":
        if len(self) != len(other):
            raise DifferentDimensions("vectors have different dimensions")
        new_coor = [coor1 + coor2 for coor1, coor2 in zip(self.coordinates, other.coordinates)]
        return Vector(new_coor)

    def __sub__(self, other: "Vector") -> "Vector":
        if len(self) != len(other):
            raise DifferentDimensions("vectors have different dimensions")
        new_coor = [coor1 - coor2 for coor1, coor2 in zip(self.coordinates, other.coordinates)]
        return Vector(new_coor)

    def scalar_product(self, other: "Vector") -> T:
        if len(self) != len(other):
            raise DifferentDimensions("vectors have different dimensions")
        return sum([coor1 * coor2 for coor1, coor2 in zip(self.coordinates, other.coordinates)])

    def vector_product(self, other: "Vector") -> "Vector":
        if len(self) != len(other):
            raise DifferentDimensions("vectors have different dimensions")
        if len(self) != 3:
            raise IncorrectDimension("the vector product is correct only for vectors of dimension 3")
        a1, a2, a3 = self.coordinates[0], self.coordinates[1], self.coordinates[2]
        b1, b2, b3 = other.coordinates[0], other.coordinates[1], other.coordinates[2]
        new_corr = [a2 * b3 - a3 * b2, a3 * b1 - a1 * b3, a1 * b2 - a2 * b1]
        return Vector(new_corr)

    def is_null(self) -> bool:
        return not (any(self.coordinates))
