from datetime import datetime
from controller.model.grant_scheme.grant_schemes_type import GrantSchemeType
from controller.model.grant_scheme.student_encouragement_bonus import StudentEncouragementBonus
from controller.model.household.household import Household
from controller.model.household.housing_type import HousingType
from controller.model.person import Person


class TestStudentEncouragementBonus():
    person_1 = Person('pid1', 0, datetime(2006, 8, 19), 'unemployed')
    person_2 = Person('pid2', 0, datetime(2007, 1, 24), 'employed')
    person_3 = Person('pid3', 0, datetime(2008, 2, 12), 'employed')
    person_4 = Person('pid4', 0, datetime(2006, 8, 19), 'student')
    person_5 = Person('pid5', 0, datetime(2007, 1, 24), 'student')
    person_6 = Person('pid6', 0, datetime(2008, 2, 12), 'student')
    person_7 = Person('pid7', 199998, datetime(2006, 8, 19), 'unemployed')
    person_8 = Person('pid8', 199999, datetime(2007, 1, 24), 'student')
    person_9 = Person('pid9', 200000, datetime(2008, 2, 12), 'student')

    def test_student_encouragement_bonus(self):
        grant = StudentEncouragementBonus()
        assert grant.type == GrantSchemeType.STUDENT_ENCOURAGEMENT_BONUS
        assert str(grant) == "student encouragement bonus"

    def test_get_members_below_16_invalid(self):
        grant = StudentEncouragementBonus()
        # not student
        is_valid_1, members_1 = grant.get_members_below_16([self.person_1, self.person_2, self.person_3, self.person_7])
        assert is_valid_1 == False
        assert members_1 == [('student encouragement bonus', 'pid2'), ('student encouragement bonus', 'pid3')]

        # not under 16
        is_valid_2, members_2 = grant.get_members_below_16([self.person_4])
        assert is_valid_2 == False
        assert members_2 == []

        # more than 200000
        is_valid_3, members_3 = grant.get_members_below_16([self.person_9])
        assert is_valid_3 == False
        assert members_3 == [('student encouragement bonus', 'pid9')]
        
    def test_get_members_below_16_valid(self):
        grant = StudentEncouragementBonus()
        persons_1 = [self.person_1, self.person_2, self.person_3, self.person_4, self.person_5, self.person_6, self.person_7]
        is_valid_1, members_1 = grant.get_members_below_16(persons_1)
        assert is_valid_1 == True
        assert members_1 == [('student encouragement bonus', 'pid2'), ('student encouragement bonus', 'pid3'), ('student encouragement bonus', 'pid5'), ('student encouragement bonus', 'pid6')]

        persons_2 = [self.person_1, self.person_2, self.person_3, self.person_4, self.person_5, self.person_6, self.person_8]
        is_valid_2, members_2 = grant.get_members_below_16(persons_2)
        assert is_valid_2 == True
        assert members_2 == [('student encouragement bonus', 'pid2'), ('student encouragement bonus', 'pid3'), ('student encouragement bonus', 'pid5'), ('student encouragement bonus', 'pid6'), ('student encouragement bonus', 'pid8')]

    def test_get_qualifying_members_invalid(self):
        persons = [self.person_1, self.person_2, self.person_3, self.person_7]
        household = Household(HousingType.CONDOMINIUM, persons)
        grant = StudentEncouragementBonus()
        members = grant.get_qualifying_members(household)
        assert members == []

    def test_get_qualifying_members_valid(self):
        persons = [self.person_1, self.person_2, self.person_3, self.person_4, self.person_5, self.person_6, self.person_7]
        household = Household(HousingType.CONDOMINIUM, persons)
        grant = StudentEncouragementBonus()
        members = grant.get_qualifying_members(household)
        assert members == [('student encouragement bonus', 'pid2'), ('student encouragement bonus', 'pid3'), ('student encouragement bonus', 'pid5'), ('student encouragement bonus', 'pid6')]