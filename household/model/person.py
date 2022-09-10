from datetime import date, datetime


class Person():
    def __init__(self, name, annual_income, dob) -> None:
        self.name = name
        self.annual_income = annual_income
        self.dob = datetime.strptime(dob, '%a, %d %b %Y %H:%M:%S GMT')

    def get_age(self):
        return date.today() - self.dob.year