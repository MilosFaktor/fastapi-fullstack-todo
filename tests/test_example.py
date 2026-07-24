import pytest


def test_equal_or_not_equal():
    assert 2 == 2
    assert 3 != 2


def test_is_instance():
    assert isinstance(2, int)
    assert isinstance("string here ", str)


def test_boolean():
    value = True
    assert value is True
    assert value is not False
    assert ("hello" == "world") is not True


def test_type():
    assert type(2) is int
    assert type("string here") is str
    assert type([1, 2, 3]) is list
    assert type({"key": "value"}) is dict


def test_greater_and_less_than():
    assert 5 > 3
    assert 2 < 4
    assert 7 >= 7
    assert 1 <= 2


def test_list():
    my_list = [1, 2, 3, 4, 5]
    any_list = [False, False]
    assert len(my_list) == 5
    assert my_list[0] == 1
    assert my_list[-1] == 5
    assert 3 in my_list
    assert 6 not in my_list
    assert all(my_list)
    assert not any(any_list)


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_student():
    return Student("John", "Doe", "Computer Science", 3)


def test_person_initialization(default_student):
    assert default_student.first_name == "John", "First name should be John"
    assert default_student.last_name == "Doe", "Last name should be Doe"
    assert default_student.major == "Computer Science", (
        "Major should be Computer Science"
    )
    assert default_student.years == 3, "Years should be 3"
