from controller.model.grant_scheme.grant_scheme import GrantScheme
from controller.model.grant_scheme.grant_schemes_type import GrantSchemeType
from controller.model.household.household import Household

class BabySunshineGrant(GrantScheme):
    def __init__(self) -> None:
        super().__init__(GrantSchemeType.BABY_SUNSHINE_GRANT)

    def get_qualifying_members(self, household: Household):
        family_members = household.family_members
        babies = self.get_babies(family_members)
        return babies

    def get_babies(self, family_members):
        babies = []
        for member in family_members:
            if member.get_age() > 0:
                continue
            
            if member.get_months() < 8:
                babies.append((str(self), member.pid))
        
        return babies