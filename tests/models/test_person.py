from datetime import datetime
from controller.model.person import Person


class TestPerson():
    def test_valid_person(self):
        person = Person('pid', 0, datetime(1998, 12, 19), 'student')
        assert person.pid == 'pid'
        assert person.annual_income == 0.0
        assert person.dob == datetime(1998, 12, 19)
        assert person.occupation_type == 'student'

    def test_get_age(self):
        person = Person('pid', 0, datetime(1998, 12, 19), 'student')
        assert person.get_age() == 24

    def test_get_months(self):
        person = Person('pid2', 0, datetime(2022, 1, 1), 'unemployed')
        assert person.get_months() == 8

    def test_is_name_valid_None(self):
        name = None
        is_valid, status_code, resp = Person.is_name_valid(name)
        assert is_valid == False
        assert status_code == 400
        assert resp == { "error": "Missing name" } 
    
    def test_is_name_valid(self):
        name = 'valid name'
        is_valid, status_code, resp = Person.is_name_valid(name)
        assert is_valid == True
        assert status_code == 200
        assert resp == None
    
    def test_is_gender_valid_None(self):
        gender = None
        is_valid, status_code, resp = Person.is_gender_valid(gender)
        assert is_valid == False
        assert status_code == 400
        assert resp == { "error": "Missing gender" } 
    
    def test_is_gender_valid_unknown(self):
        gender = 'unknown gender'
        is_valid, status_code, resp = Person.is_gender_valid(gender)
        assert is_valid == False
        assert status_code == 403
        assert resp == { "error": "gender must be male, female, other or prefer not to say. Got: unknown gender" } 

    def test_is_gender_valid(self):
        gender = 'MALE'
        is_valid, status_code, resp = Person.is_gender_valid(gender)
        assert is_valid == True
        assert status_code == 200
        assert resp == None
    
    def test_is_marital_status_valid_None(self):
        marital_status = None
        is_valid, status_code, resp = Person.is_marital_status_valid(marital_status)
        assert is_valid == False
        assert status_code == 400
        assert resp == { "error": "Missing marital_status" } 
    
    def test_is_marital_status_valid_unknown(self):
        marital_status = 'unknown gender'
        is_valid, status_code, resp = Person.is_marital_status_valid(marital_status)
        assert is_valid == False
        assert status_code == 403
        assert resp == { "error": "marital_status must be single, married, widowed, separated, divorced or others. Got: unknown gender" } 

    def test_is_marital_status_valid(self):
        marital_status = 'SINGLE'
        is_valid, status_code, resp = Person.is_marital_status_valid(marital_status)
        assert is_valid == True
        assert status_code == 200
        assert resp == None

    def test_is_occupation_valid_None(self):
        occupation_type = None
        is_valid, status_code, resp = Person.is_occupation_valid(occupation_type)
        assert is_valid == False
        assert status_code == 400
        assert resp == { "error": "Missing occupation_type" }

    def test_is_occupation_valid_unknown(self):
        occupation_type = 'unknown occupation_type'
        is_valid, status_code, resp = Person.is_occupation_valid(occupation_type)
        assert is_valid == False
        assert status_code == 403
        assert resp == { "error": "Occupation must be unemployed, student or employed. Got: unknown occupation_type" }

    def test_is_occupation_valid(self):
        occupation_type = 'STUDENT'
        is_valid, status_code, resp = Person.is_occupation_valid(occupation_type)
        assert is_valid == True
        assert status_code == 200
        assert resp == None

    def test_is_annual_income_valid_None(self):
        annual_income = None
        is_valid, status_code, resp = Person.is_annual_income_valid(annual_income)
        assert is_valid == True
        assert status_code == 200
        assert resp == None

    def test_is_annual_income_valid_unknown_type(self):
        annual_income = 'unknown type'
        is_valid, status_code, resp = Person.is_annual_income_valid(annual_income)
        assert is_valid == False
        assert status_code == 403
        assert resp == { "error": "Annual income must be numeric. Got unknown type" }

    def test_is_annual_income_valid_below_0(self):
        annual_income = -0.1
        is_valid, status_code, resp = Person.is_annual_income_valid(annual_income)
        assert is_valid == False
        assert status_code == 403
        assert resp == { "error": "Annual income must be at least 0. Got: -0.1" }
    
    def test_is_annual_income_valid(self):
        annual_income = 1000.10
        is_valid, status_code, resp = Person.is_annual_income_valid(annual_income)
        assert is_valid == True
        assert status_code == 200
        assert resp == None

    def test_is_dob_valid_None(self):
        dob = None
        is_valid, status_code, resp = Person.is_dob_valid(dob)
        assert is_valid == False
        assert status_code == 400
        assert resp == { "error": "Missing date of birth." }

    def test_is_dob_valid_unknown_format(self):
        dob = 123
        is_valid, status_code, resp = Person.is_dob_valid(dob)
        assert is_valid == False
        assert status_code == 403
        assert resp == { "error": 'Date format should be YYYY-MM-DD. Got: 123' }

        dob = '19-12-1998'
        is_valid, status_code, resp = Person.is_dob_valid(dob)
        assert is_valid == False
        assert status_code == 403
        assert resp == { "error": 'Date format should be YYYY-MM-DD. Got: 19-12-1998' }

    def test_is_dob_valid_future(self):
        dob = '2023-01-01'
        is_valid, status_code, resp = Person.is_dob_valid(dob)
        assert is_valid == False
        assert status_code == 403
        assert resp == { "error": f"Date of birth must be before {datetime.today().date()}. Got: {dob}" }
    
    def test_is_dob_valid(self):
        dob = '1998-12-19'
        is_valid, status_code, resp = Person.is_dob_valid(dob)
        assert is_valid == True
        assert status_code == 200
        assert resp == None
