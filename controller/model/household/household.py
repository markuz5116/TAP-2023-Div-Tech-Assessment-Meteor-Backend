from typing import List
from controller.model.household.housing_type import HousingType
from controller.model.person import Person


class Household():
    def __init__(self, housing_type: HousingType, family_members: List[Person]) -> None:
        self.housing_type = housing_type
        self.family_members = family_members