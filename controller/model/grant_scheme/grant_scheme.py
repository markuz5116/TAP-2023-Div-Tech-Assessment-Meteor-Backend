from typing import List, Tuple
from controller.model.household.household import Household
from controller.model.household.housing_type import HousingType


class GrantScheme():
    def __init__(self, type: HousingType) -> None:
        self.type = type
    
    def get_qualifying_members(self, household: Household) -> List[Tuple]:
        raise NotImplementedError()

    def __str__(self) -> str:
        return str(self.type)