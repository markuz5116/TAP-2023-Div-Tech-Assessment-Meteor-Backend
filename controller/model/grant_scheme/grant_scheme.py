from controller.model.household.household import Household


class GrantScheme():
    def __init__(self, type) -> None:
        self.type = type
    
    def get_qualifying_members(self, household: Household):
        raise NotImplementedError()

    def get_type(self):
        return str(self.type)