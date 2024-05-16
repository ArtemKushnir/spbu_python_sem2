import random
import string

import hypothesis.strategies as st
import pytest
from hypothesis import given

from src.exam.test1.task_1 import *


def randomword(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


class TestUniversity:
    @staticmethod
    def get_random_teacher(cnt):
        teachers = []
        for i in range(cnt):
            teachers.append(Teacher(randomword(5), [randomword(2), randomword(2)]))
        return teachers

    @staticmethod
    def get_random_students(cnt):
        students = []
        for i in range(cnt):
            students.append(Student(randomword(5), {randomword(2): random.randint(0, 5)}))
        return students

    def get_random_courses(self, cnt):
        courses = []
        for i in range(cnt):
            students = self.get_random_students(10)
            teacher = self.get_random_teacher(1)[0]
            courses.append(Course(randomword(10), students, teacher))
        return courses

    @given(st.integers(1, 2000))
    def test_add_student(self, cnt):
        university = University()
        students = self.get_random_students(cnt)
        for student in students:
            university._add_student(student)
        for student in students:
            assert university.students[student.name] == student

    @given(st.integers(1, 2000))
    def test_add_teacher(self, cnt):
        university = University()
        teachers = self.get_random_teacher(cnt)
        for teacher in teachers:
            university._add_teacher(teacher)
        for teacher in teachers:
            assert university.teachers[teacher.name] == teacher

    @pytest.mark.parametrize("name,course_names", [("Test", ["test1"]), ("Qwerty", ["test2"]), ("S", ["test3"])])
    def test_get_teacher_courses(self, name, course_names):
        university = University()
        teacher = Teacher(name, course_names)
        expected = []
        courses = self.get_random_courses(100)
        cnt_course = random.randint(0, 99)
        courses[cnt_course].teacher = teacher
        courses[cnt_course].name = course_names[0]
        expected.append(courses[cnt_course])
        for course in courses:
            university.add_courses(course)
        assert university.get_teacher_courses(name) == expected

    @pytest.mark.parametrize(
        "name,course_names", [("Test", {"test1": 1}), ("Qwerty", {"test2": 2}), ("S", {"test3": 3})]
    )
    def test_get_student_courses(self, name, course_names):
        university = University()
        student = Student(name, course_names)
        expected = []
        courses = self.get_random_courses(100)
        cnt_course = random.randint(0, 99)
        courses[cnt_course].students.append(student)
        courses[cnt_course].name = list(course_names.keys())[0]
        expected.append(courses[cnt_course])
        for course in courses:
            university.add_courses(course)
        assert university.get_students_courses(name) == expected

    @given(st.integers(1, 200))
    def test_get_student(self, cnt):
        university = University()
        students = self.get_random_students(cnt)
        random_student = self.get_random_students(1)[0]
        students.append(random_student)
        for student in students:
            university._add_student(student)
        assert university.get_student(random_student.name) == random_student

    @given(st.integers(1, 200))
    def test_get_teacher(self, cnt):
        university = University()
        teachers = self.get_random_teacher(cnt)
        random_teacher = self.get_random_teacher(1)[0]
        teachers.append(random_teacher)
        for teacher in teachers:
            university._add_teacher(teacher)
        assert university.get_teacher(random_teacher.name) == random_teacher

    @given(st.integers(1, 200))
    def test_get_course(self, cnt):
        university = University()
        courses = self.get_random_courses(cnt)
        random_course = self.get_random_courses(1)[0]
        courses.append(random_course)
        for course in courses:
            university.add_courses(course)
        assert university.get_course(random_course.name) == random_course

    @pytest.mark.parametrize(
        "name,courses_and_marks, expected",
        [("1", {"a": 2, "b": 3}, 2.5), ("2", {"a": 5}, 5), ("3", {"a": 1, "b": 1, "c": 1}, 1)],
    )
    def test_get_student_average_score(self, name, courses_and_marks, expected):
        university = University()
        university._add_student(Student(name, courses_and_marks))
        assert university.get_student_average_score(name) == expected

    @given(st.integers(1, 5), st.integers(1, 200))
    def test_get_course_average_score(self, mark, cnt):
        university = University()
        teacher = self.get_random_teacher(1)[0]
        students = self.get_random_students(cnt)
        for student in students:
            student.courses_marks["test"] = mark
        course = Course("test", students, teacher)
        university.add_courses(course)
        assert university.get_course_average_score("test") == mark

    @given(st.integers(1, 200))
    def test_raise_get_student(self, cnt):
        university = University()
        students = self.get_random_students(cnt)
        for student in students:
            university._add_student(student)
        with pytest.raises(KeyError):
            university.get_student(randomword(10))

    @given(st.integers(1, 200))
    def test_raise_get_teacher(self, cnt):
        university = University()
        teachers = self.get_random_teacher(cnt)
        for teacher in teachers:
            university._add_teacher(teacher)
        with pytest.raises(KeyError):
            university.get_teacher(randomword(10))

    @given(st.integers(1, 200))
    def test_raise_get_course(self, cnt):
        university = University()
        courses = self.get_random_courses(cnt)
        for course in courses:
            university.add_courses(course)
        with pytest.raises(KeyError):
            university.get_course(randomword(10))
