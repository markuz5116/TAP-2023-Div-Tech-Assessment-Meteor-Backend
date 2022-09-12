from controller.model.grant_scheme.grant_scheme import GrantScheme
from controller.model.grant_scheme.grant_schemes_type import GrantSchemeType
from controller.model.household.household import Household

class YoloGstGrant(GrantScheme):
    def __init__(self) -> None:
        super().__init__(GrantSchemeType.YOLO_GST_GRANT)

    def get_qualifying_members(self, household: Household):
        family_members = household.family_members
        if not self.has_valid_household_income(family_members):
            return []

        valid_members = [(str(self), member.pid) for member in family_members]
        return valid_members

    def has_valid_household_income(self, family_members) -> bool:
        household_income = 0
        for member in family_members:
            household_income += member.annual_income
        return household_income < 100000