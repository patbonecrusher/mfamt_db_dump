import pprint
from datetime import datetime
from typing import Union, AnyStr, Type

from dataclasses import dataclass
from dataclass_wizard import asdict, JSONWizard, json_field, LoadMixin
from dataclass_wizard.type_def import N

pp = pprint.PrettyPrinter(indent=4)

@dataclass(eq=True, frozen=True)
class Person(JSONWizard, LoadMixin):
    gender: str = json_field("ZGENDER", all=False)
    updatedOn: datetime = json_field("ZCHANGEDATE", all=False)
    createdOn: datetime = json_field("ZCREATIONDATE", all=False)
    gedcomId: str = json_field("ZGEDCOMID", all=False)
    uniqueId: str = json_field("ZUNIQUEID", all=False)
    primaryKey: int = json_field("Z_PK", all=False)
    firstName: str = json_field("ZFIRSTNAME", all=False)
    lastName: str = json_field("ZLASTNAME", all=False)
    birthDate: datetime = json_field("ZCACHED_BIRTHDATEASDATE", all=False)
    
    def load_to_datetime(o: Union[float, N], base_type: Type[datetime]) -> datetime:
        return sqlite_to_datetime(o)
    
"""
Convert sqlite date to datetime
"""
def sqlite_to_datetime(sqlite_date: float) -> datetime: 
    return datetime.fromtimestamp(sqlite_date + 978307200)

def parse_person(personJson: str) -> Person:
    try:
        person = Person.from_json(personJson)
        return person

    except TypeError as e:
        pp.pprint(f"Config file contains unknown keys {repr(e)}")
        return None

def person_to_dict(person: Person) -> dict:
    return asdict(person)

def person_to_json(person: Person) -> str:
    return person.to_json()

personJSON = '{"Z_PK": 1688, "Z_ENT": 15, "Z_OPT": 4, "ZRESEARCHASSISTANTCOMPLETEDQUESTIONSMASK": -3104, "ZGENDER": 0, "ZISBOOKMARKED2": 0, "ZISSTARTPERSON": 1, "ZCHANGEDATE": 696487034.98555, "ZCREATIONDATE": 274212410.827505, "ZCACHED_BIRTHDATEASDATE": -926841600, "ZCLOUDKITCHANGETAG": "k0", "ZGEDCOMID": "23309270", "ZUNIQUEID": "E593F3ED-72CC-4CF9-A1F2-FE0FEB140B9E", "ZCACHED_BIRTHDATE": "08/19/1971", "ZCACHED_FULLNAME": "Patrick Laplante", "ZCACHED_FULLNAMEFORSORTING": "patrick laplante", "ZFIRSTNAME": "Patrick", "ZFIRSTNAMESOUNDEX": "p362", "ZLASTNAME": "Laplante", "ZLASTNAMESOUNDEX": "l145"}'

def main():
    print(sqlite_to_datetime(-926841600))
    print(parse_person(personJSON))
    

if __name__ == "__main__":
    main()