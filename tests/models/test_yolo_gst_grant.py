from datetime import datetime
from controller.model.grant_scheme.grant_schemes_type import GrantSchemeType
from controller.model.grant_scheme.yolo_gst_grant import YoloGstGrant
from controller.model.person import Person


class TestYoloGstGrant():
    person_1 = Person('pid1', 99998, datetime(2006, 8, 19), 'unemployed')
    person_2 = Person('pid1', 99999, datetime(2006, 8, 19), 'unemployed')
    person_3 = Person('pid2', 100000, datetime(2007, 1, 24), 'employed')

    def test_yolo_gst_grant(self):
        grant = YoloGstGrant()
        assert grant.type == GrantSchemeType.YOLO_GST_GRANT
        assert str(grant) == "yolo gst grant"

    def test_has_valid_household_income_invalid(self):
        grant = YoloGstGrant()
        assert grant.has_valid_household_income([self.person_3]) == False

    def test_has_valid_household_income_valid(self):
        grant = YoloGstGrant()
        assert grant.has_valid_household_income([self.person_1]) == True

        assert grant.has_valid_household_income([self.person_2]) == True