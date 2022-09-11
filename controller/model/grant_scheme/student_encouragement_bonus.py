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
            return []
        
        return valid_members

    def get_members_below_16(self, family_members: list[Person]):
        valid_members = []
        is_valid = False
        household_income = 0
        for member in family_members:
            household_income += member.annual_income
            if member.get_age() < 16:
                valid_members.append((super().get_type(), member.pid))
                if member.occupation_type == "student":
                    is_valid = True
        return is_valid and household_income < 200000, valid_members