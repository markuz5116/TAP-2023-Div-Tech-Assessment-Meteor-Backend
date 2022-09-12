from datetime import datetime
from controller.model.grant_scheme.baby_sunshine_grant import BabySunshineGrant
from controller.model.grant_scheme.grant_schemes_type import GrantSchemeType
from controller.model.household.household import Household
from controller.model.household.housing_type import HousingType
from controller.model.person import Person


class TestBabySunshineGrant():
    person_1 = Person('pid1', 0, datetime(2022, 8, 19), 'unemployed')
    person_2 = Person('pid2', 24000, datetime(2022, 1, 24), 'employed')
    person_3 = Person('pid3', 300000, datetime(2017, 2, 12), 'student')
    
    def test_valid_baby_sunshine_grant(self):
        grant = BabySunshineGrant()
        assert grant.type == GrantSchemeType.BABY_SUNSHINE_GRANT
        assert str(grant) == "baby sunshine grant"

    def test_get_babies_invalid(self):
        persons = [self.person_2, self.person_3]
        grant = BabySunshineGrant()
        babies = grant.get_babies(persons)
        assert babies == []

    def test_get_babies_valid(self):
        persons = [self.person_1, self.person_2]
        grant = BabySunshineGrant()
        babies = grant.get_babies(persons)
        assert babies == [(str(grant), self.person_1.pid)]

    def test_get_qualifying_members_invalid(self):
        persons = [self.person_2, self.person_3]
        household = Household(HousingType.CONDOMINIUM, persons)
        grant = BabySunshineGrant()
        babies = grant.get_qualifying_members(household)
        assert babies == []

    def test_get_qualifying_members_valid(self):
        persons = [self.person_1, self.person_2]
        household = Household(HousingType.CONDOMINIUM, persons)
        grant = BabySunshineGrant()
        babies = grant.get_qualifying_members(household)
        assert babies == [(str(grant), self.person_1.pid)]