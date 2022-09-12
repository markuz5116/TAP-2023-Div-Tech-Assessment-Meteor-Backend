from datetime import datetime
from controller.model.grant_scheme.grant_schemes_type import GrantSchemeType
from controller.model.grant_scheme.multigeneration_scheme import MutligenerationScheme
from controller.model.household.household import Household
from controller.model.household.housing_type import HousingType
from controller.model.person import Person


class TestMutligenerationScheme():
    person_1 = Person('pid1', 0, datetime(2003, 8, 19), 'unemployed')
    person_2 = Person('pid2', 0, datetime(2004, 1, 24), 'employed')
    person_3 = Person('pid3', 0, datetime(2005, 2, 12), 'student')
    person_4 = Person('pid4', 0, datetime(1966, 2, 12), 'student')
    person_5 = Person('pid5', 0, datetime(1967, 2, 12), 'student')
    person_6 = Person('pid6', 0, datetime(1968, 2, 12), 'student')
    person_7 = Person('pid7', 149999, datetime(1992, 2, 12), 'student')
    person_8 = Person('pid8', 150000, datetime(1992, 2, 12), 'student')
    person_9 = Person('pid9', 150001, datetime(1992, 2, 12), 'student')

    def test_valid_multigeneration_scheme(self):
        grant = MutligenerationScheme()
        assert grant.type == GrantSchemeType.MULTIGENERATION_SCHEME
        assert str(grant) == 'multigeneration scheme'

    def test_has_valid_members_invalid(self):
        grant = MutligenerationScheme()
        # Invalid age
        assert grant.has_valid_members([self.person_1, self.person_2, self.person_5, self.person_6, self.person_7]) == False

        # Invalid income
        assert grant.has_valid_members([self.person_3, self.person_8]) == False
        assert grant.has_valid_members([self.person_3, self.person_9]) == False

    def test_has_valid_members_valid(self):
        grant = MutligenerationScheme()

        assert grant.has_valid_members([self.person_3, self.person_7]) == True
        assert grant.has_valid_members([self.person_4, self.person_7]) == True
        assert grant.has_valid_members([self.person_3, self.person_7]) == True

    def test_get_qualifying_members_invalid(self):
        persons = [self.person_3, self.person_8]
        household = Household(HousingType.CONDOMINIUM, persons)
        grant = MutligenerationScheme()
        babies = grant.get_qualifying_members(household)
        assert babies == []

    def test_get_qualifying_members_valid(self):
        persons = [self.person_3, self.person_7]
        household = Household(HousingType.CONDOMINIUM, persons)
        grant = MutligenerationScheme()
        babies = grant.get_qualifying_members(household)
        assert babies == [(str(grant), 'pid3'), (str(grant), 'pid7')]