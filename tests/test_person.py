from datetime import datetime
from mfamt_db_dump.person import Person

def test_should_create_person():
    person = Person("M", datetime.now(), datetime.now())
    assert person is not None
    
def test_updated_on_should_be_none():
    person = Person("M")
    assert person.updatedOn is None
    
def test_created_on_should_be_none():
    person = Person("M")
    assert person.createdOn is None

def test_parse_person():
    person = Person("M", datetime.now(), datetime.now())
    assert person is not None
    assert person.gender == "M"
    assert person.updatedOn is not None
    assert person.createdOn is not None
    
def test_person_first_name():
    person = Person("M", datetime.now(), datetime.now(), firstName="John")
    assert person.firstName == "John"


# def test_updated_on_should_be_newer_than_created_on():
#     person = Person("M", datetime.now(), datetime.now())
#     assert person.updatedOn > person.createdOn

