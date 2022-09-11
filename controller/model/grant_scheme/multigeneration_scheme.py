from controller.model.grant_scheme.grant_scheme import GrantScheme
from controller.model.grant_scheme.grant_schemes_type import GrantSchemeType
from controller.model.household.household import Household


class MutligenerationScheme(GrantScheme):
    def __init__(self) -> None:
        super().__init__(GrantSchemeType.MULTIGENERATION_SCHEME)

    def get_qualifying_members(self, household: Household):
        family_members = household.family_members
        if not self.has_valid_members(family_members):
            return []
        
        return [(str(self), member.pid) for member in family_members]
        
    def has_valid_members(self, family_members):
        is_valid = False
        household_income = 0
        for member in family_members:
            age = member.get_age()
            annual_income = member.annual_income
            household_income += annual_income
            if age < 18 or age > 55:
                is_valid = True
        return is_valid and household_income < 150000