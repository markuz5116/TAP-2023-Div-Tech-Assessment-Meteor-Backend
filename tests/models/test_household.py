from datetime import datetime
import pytest
from controller.model.household.household import Household
from controller.model.household.housing_type import HousingType
from controller.model.person import Person

class TestHousehold():
    person_1 = Person('pid1', 0, datetime(1998, 12, 19), 'unemployed')
    person_2 = Person('pid2', 24000, datetime(1969, 7, 24), 'employed')
    person_3 = Person('pid3', 300000, datetime(2017, 2, 12), 'student')

    def test_valid_landed(self):
        persons = [self.person_1, self.person_2]
        household = Household(HousingType.LANDED, persons)
        assert household.housing_type == HousingType.LANDED
        assert household.family_members == persons

    def test_valid_condo(self):
        persons = [self.person_1, self.person_3]
        household = Household(HousingType.CONDOMINIUM, persons)
        assert household.housing_type == HousingType.CONDOMINIUM
        assert household.family_members == persons

    def test_valid_hdb(self):
        persons = [self.person_2, self.person_3]
        household = Household(HousingType.HDB, persons)
        assert household.housing_type == HousingType.HDB
        assert household.family_members == persons