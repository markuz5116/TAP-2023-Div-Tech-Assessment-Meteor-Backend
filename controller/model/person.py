from datetime import date, datetime


class Person():
    @staticmethod
    def is_name_valid(name) -> bool and int and dict[str, str]:
        resp = None
        status_code = 200
        is_valid = True
        if not name:
            resp = {
                "error": "Missing name"
            }
            is_valid = False
            status_code = 400
        return is_valid, status_code, resp

    @staticmethod
    def is_gender_valid(gender) -> bool and int and dict[str, str]:
        resp = None
        status_code = 200
        is_valid = True
        if not gender:
            resp = {
                "error": "Missing gender"
            }
            is_valid = False
            status_code = 400
            return is_valid, status_code, resp
        
        gender = gender.lower()
        if gender not in ['male', 'female', 'other', 'prefer not to say']:
            resp = {
                "error": f"gender must be male, female, other or prefer not to say. Got: {gender}"
            }
            is_valid = False
            status_code = 403
            return is_valid, status_code, resp
        
        return is_valid, status_code, resp

    @staticmethod
    def is_marital_status_valid(marital_status) -> bool and int and dict[str, str]:
        resp = None
        status_code = 200
        is_valid = True
        if not marital_status:
            resp = {
                "error": "Missing Marital Status"
            }
            is_valid = False
            status_code = 400
            return is_valid, status_code, resp
        
        marital_status = marital_status.lower()
        if marital_status not in ['single', 'married', 'widowed', 'separated', 'divorced', 'others']:
            resp = {
                "error": f"marital_status must be single, married, widowed, separated, divorced or others. Got: {marital_status}"
            }
            is_valid = False
            status_code = 403
            return is_valid, status_code, resp
        
        return is_valid, status_code, resp

    @staticmethod
    def is_occupation_valid(occupation_type) -> bool and int and dict[str, str]:
        resp = None
        status_code = 200
        is_valid = True
        if not occupation_type:
            resp = {
                "error": "Missing Occupation"
            }
            is_valid = False
            status_code = 400
            return is_valid, status_code, resp
        
        occupation_type = occupation_type.lower()
        if occupation_type not in ['unemployed', 'student', 'employed']:
            resp = {
                "error": f"Occupation must be unemployed, student or employed. Got: {occupation_type}"
            }
            is_valid = False
            status_code = 403
            return is_valid, status_code, resp
        
        return is_valid, status_code, resp

    @staticmethod
    def is_annual_income_valid(annual_income):
        resp = None
        status_code = 200
        is_valid = True
        if not annual_income:
            return is_valid, status_code, resp
        
        try:
            annual_income = float(annual_income)
        except:
            resp = {
                "error": f"Annual income must be numeric. Got {annual_income}"
            }
            is_valid = False
            status_code = 403
            return is_valid, status_code, resp

        if float(annual_income) < 0:
            resp = {
                "error": f"Annual income must be at least 0. Got: {annual_income}"
            }
            is_valid = False
            status_code = 403
            return is_valid, status_code, resp
        
        return is_valid, status_code, resp

    @staticmethod
    def is_dob_valid(dob) -> bool and int and dict[str, str]:
        resp = None
        status_code = 200
        is_valid = True
        if not dob:
            resp = {
                "error": "Missing date of birth."
            }
            is_valid = False
            status_code = 400
            return is_valid, status_code, resp

        try:
            dob = datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            resp = {
                "error": f'Date format should be YYYY-MM-DD. Got: {dob}'
            }
            is_valid = False
            status_code = 403
            return is_valid, status_code, resp

        if (dob > datetime.today()):
            resp = {
                "error": f"Date of birth must be before {datetime.today().date()}. Got: {dob.date()}"
            }
            is_valid = False
            status_code = 403
            return is_valid, status_code, resp
        
        return is_valid, status_code, resp

    @staticmethod
    def is_valid(args) -> bool and dict[str, str] and int:

        name = args.get('name')
        is_valid, status_code, resp = Person.is_name_valid(name)
        if not is_valid:
            return is_valid, resp, status_code

        gender = args.get('gender')
        is_valid, status_code, resp = Person.is_gender_valid(gender)
        if not is_valid:
            return is_valid, resp, status_code

        marital_status = args.get('marital_status')
        is_valid, status_code, resp = Person.is_marital_status_valid(marital_status)
        if not is_valid:
            return is_valid, resp, status_code

        occupation_type = args.get('occupation_type')
        is_valid, status_code, resp = Person.is_occupation_valid(occupation_type)
        if not is_valid:
            return is_valid, resp, status_code
        
        annual_income = args.get('annual_income')
        is_valid, status_code, resp = Person.is_annual_income_valid(annual_income)
        if not is_valid:
            return is_valid, resp, status_code

        dob = args.get('dob')
        is_valid, status_code, resp = Person.is_dob_valid(dob)
        if not is_valid:
            return is_valid, resp, status_code

        return is_valid, resp, status_code


    def __init__(self, pid: str, annual_income: float, dob: date, occupation_type: str) -> None:
        self.pid = pid
        self.annual_income = float(annual_income)
        self.dob = dob
        self.occupation_type = occupation_type.lower()

    def get_age(self) -> int:
        return date.today().year - self.dob.year

    def get_months(self) -> int:
        return date.today().month - self.dob.month