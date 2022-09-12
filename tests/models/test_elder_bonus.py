from datetime import datetime
from controller.model.grant_scheme.elder_bonus import ElderBonus
from controller.model.person import Person
from controller.model.grant_scheme.grant_schemes_type import GrantSchemeType
from controller.model.household.household import Household
from controller.model.household.housing_type import HousingType


class TestElderBonus():
    person_1 = Person('pid1', 0, datetime(1966, 8, 19), 'unemployed')
    person_2 = Person('pid2', 24000, datetime(1967, 1, 24), 'employed')
    person_3 = Person('pid3', 300000, datetime(1968, 2, 12), 'student')

    def test_valid_elder_bonus(self):
        grant = ElderBonus()
        assert grant.type == GrantSchemeType.ELDER_BONUS
        assert str(grant) == "elder bonus"

    def test_get_members_above_55_invalid(self):
        grant = ElderBonus()
        members = grant.get_members_above_55([self.person_3])
        assert members == []

    def test_get_members_above_55_valid(self):
        grant = ElderBonus()
        members = grant.get_members_above_55([self.person_1, self.person_2])
        assert members == [(str(grant), 'pid1'), (str(grant), 'pid2')]

    def test_get_qualifying_members_invalid(self):
        persons = [self.person_3]
        household = Household(HousingType.HDB, persons)
        grant = ElderBonus()
        babies = grant.get_qualifying_members(household)
        assert babies == []

        persons = [self.person_3]
        household = Household(HousingType.CONDOMINIUM, persons)
        grant = ElderBonus()
        babies = grant.get_qualifying_members(household)
        assert babies == []

    def test_get_qualifying_members_valid(self):
        persons = [self.person_1, self.person_2]
        household = Household(HousingType.HDB, persons)
        grant = ElderBonus()
        babies = grant.get_qualifying_members(household)
        assert babies == [(str(grant), 'pid1'), (str(grant), 'pid2')]
