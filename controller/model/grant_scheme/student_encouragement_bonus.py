from controller.model.grant_scheme.grant_scheme import GrantScheme
from controller.model.grant_scheme.grant_schemes_type import GrantSchemeType
from controller.model.household.household import Household
from controller.model.person import Person

class StudentEncouragementBonus(GrantScheme):
    def __init__(self) -> None:
        super().__init__(GrantSchemeType.STUDENT_ENCOURAGEMENT_BONUS)

    def get_qualifying_members(self, household: Household):
        family_members = household.family_members
        is_valid, valid_members = self.get_members_below_16(family_members)
        if not is_valid:
            return None
        
        if not self.has_valid_income(family_members):
            return None
        
        return valid_members

    def get_members_below_16(self, family_members: list[Person]):
        students = []
        is_valid = False
        for member in family_members:
            if member.get_age() < 16:
                students.append(member.pid)
                if member.occupation_type == "student":
                    is_valid = True
        return is_valid, students

    def has_valid_income(self, family_members: list[Person]):
        household_income = 0
        for member in family_members:
            household_income += member.annual_income
        return household_income < 200000