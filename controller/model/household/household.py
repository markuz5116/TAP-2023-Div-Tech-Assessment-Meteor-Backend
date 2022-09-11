from controller.model.person import Person


class Household():
    def __init__(self, housing_type, family_members) -> None:
        self.housing_type = housing_type
        self.family_members = family_members