from typing import List, Tuple
from controller.model.grant_scheme.grant_scheme import GrantScheme
from controller.model.grant_scheme.grant_schemes_type import GrantSchemeType
from controller.model.household.household import Household
from controller.model.household.housing_type import HousingType
from controller.model.person import Person

class ElderBonus(GrantScheme):
    def __init__(self) -> None:
        super().__init__(GrantSchemeType.ELDER_BONUS)

    def get_qualifying_members(self, household: Household) -> List[Tuple]:
        if household.housing_type != HousingType.HDB:
            return []
        
        family_members = household.family_members
        valid_members = self.get_members_above_55(family_members)
        
        return valid_members

    def get_members_above_55(self, family_members: List[Person]) -> List[Tuple]:
        valid_members = []
        for member in family_members:
            if member.get_age() >= 55:
                valid_members.append((str(self), member.pid))
        return valid_members