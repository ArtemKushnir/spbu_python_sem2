from dataclasses import dataclass


@dataclass
class Student:
    name: str
    courses_marks: dict[str, int]


@dataclass
class Teacher:
    name: str
    courses: list[str]


@dataclass
class Course:
    name: str
    students: list[Student]
    teacher: Teacher


class University:
    def __init__(self) -> None:
        self.courses: dict[str, Course] = {}
        self.teachers: dict[str, Teacher] = {}
        self.students: dict[str, Student] = {}

    def _add_student(self, student: Student) -> None:
        name = student.name
        self.students[name] = self.students.get(name, student)

    def _add_teacher(self, teacher: Teacher) -> None:
        name = teacher.name
        self.teachers[name] = self.teachers.get(name, teacher)

    def add_courses(self, course: Course) -> None:
        for student in course.students:
            self._add_student(student)
        self._add_teacher(course.teacher)
        name = course.name
        self.courses[name] = self.courses.get(name, course)

    def get_teacher_courses(self, teacher_name: str) -> list[Course]:
        teacher = self.get_teacher(teacher_name)
        result = []
        for course in teacher.courses:
            result.append(self.courses[course])
        return result

    def get_students_courses(self, student_name: str) -> list[Course]:
        student = self.get_student(student_name)
        result = []
        for course in student.courses_marks.keys():
            result.append(self.courses[course])
        return result

    def get_student(self, student_name: str) -> Student:
        student = self.students.get(student_name, None)
        if student is None:
            raise KeyError("There is no such student")
        return student

    def get_teacher(self, teacher_name: str) -> Teacher:
        teacher = self.teachers.get(teacher_name, None)
        if teacher is None:
            raise KeyError("There is no such teacher")
        return teacher

    def get_student_average_score(self, student_name: str) -> float:
        student = self.students[student_name]
        student_marks = student.courses_marks.values()
        return sum(student_marks) / len(student_marks)

    def get_course(self, course_name: str) -> Course:
        course = self.courses.get(course_name, None)
        if course is None:
            raise KeyError("There is no such course")
        return course

    def get_course_average_score(self, course_name: str) -> float:
        course = self.get_course(course_name)
        sum_marks = 0
        for student in course.students:
            sum_marks += student.courses_marks[course_name]
        return sum_marks / len(course.students)
