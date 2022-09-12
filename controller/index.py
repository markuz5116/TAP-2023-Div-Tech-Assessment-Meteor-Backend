import os
from typing import List, Tuple
import psycopg2
from flask import Flask, jsonify, request
from controller.model.grant_scheme.baby_sunshine_grant import BabySunshineGrant
from controller.model.grant_scheme.elder_bonus import ElderBonus
from controller.model.grant_scheme.grant_schemes_type import GrantSchemeType
from controller.model.grant_scheme.multigeneration_scheme import MutligenerationScheme
from controller.model.grant_scheme.student_encouragement_bonus import StudentEncouragementBonus
from controller.model.grant_scheme.yolo_gst_grant import YoloGstGrant
from controller.model.household.household import Household
from controller.model.household.housing_type import HousingType

from controller.model.person import Person

app = Flask(__name__)
ALL_GRANTS = [StudentEncouragementBonus(), MutligenerationScheme(), ElderBonus(), BabySunshineGrant(), YoloGstGrant()]

def connect_to_db():
    conn = psycopg2.connect(host='localhost',
        database='tap_meteor',
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])
    return conn

def group_households(records: List[Tuple]):
    households = {}
    for record in records:
        household_name = record[0]
        if household_name not in households:
            household = {
                'Housing type': record[1],
                'Family members': []
            }
            households[household_name] = household

        household = households[household_name]
        family_member = {
            'Name': record[2],
            'Gender': record[3],
            'Marital status': record[4],
            'Spouse': record[5] if record[5] else 'No spouse',
            'Occupation type': record[6],
            'Annual income': record[7] if record[7] else 0.00,
            'DOB': f"{record[8].day}-{record[8].month}-{record[8].year}"
        }
        household['Family members'].append(family_member)

    return households

def check_all_grants(household, hid):
    for grant in ALL_GRANTS:
        members = grant.get_qualifying_members(household)
        conn = connect_to_db()
        cur = conn.cursor()
        if len(members) > 0:
            input_str = ','.join(cur.mogrify("(%s,%s)", x).decode('utf-8') for x in members)
            cur.execute('''
                INSERT INTO eligible_schemes_for_people values 
            ''' + (input_str))
        else:
            cur.execute('''
                SELECT * FROM remove_valid_members(%s, %s)
            ''', (str(grant), hid, ))
            
        conn.commit()
        cur.close()
        conn.close()

@app.route('/households', methods=['GET'])
def list_households():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM list_households();')
    records = cur.fetchall()
    
    cur.close()
    conn.close()

    if len(records) == 0:
        resp = {
            "Success": "There are no households found."
        }
        return jsonify(resp), 200

    households = group_households(records)
    return jsonify(households), 200

@app.route('/households/<id>', methods=['GET'])
def get_household(id):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM get_household(%s);', (id,))
    records = cur.fetchall()

    cur.close()
    conn.close()
    
    if len(records) == 0:
        resp = {
            "error" : f"No household with id {id} found."
        }
        return jsonify(resp), 403

    household = group_households(records)
    return jsonify(household), 200

@app.route('/grant_schemes/<grant>', methods=['GET'])
def get_valid_households(grant):
    grant = grant.lower()
    is_valid = GrantSchemeType.is_valid(grant)
    if not is_valid:
        resp = {
            "error": "Grant must be %s. Got: %s" % (', '.join([str(grant) for grant in ALL_GRANTS]), grant)
        }
        return jsonify(resp), 403

    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT * FROM get_eligible_members(%s);
    ''', (grant,))

    records = cur.fetchall()
    cur.close()
    conn.close()

    valid_members = group_households(records)
    return jsonify(valid_members), 200

@app.route('/create_household', methods=['POST'])
def create_household():
    housing_type = request.args.get('housing_type')
    if not housing_type:
        return jsonify({
            "error": 'Missing housing_type'
            }), 400

    housing_type = housing_type.lower()
    if housing_type not in ['landed', 'condominium', 'hdb']:
        return jsonify({ 
            "error": f'housing_type must be landed, condominium or hdb, got: {housing_type}'
            }), 403

    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM add_household(%s)', (housing_type,))
    housing_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({
        "Success": f'House added with id: {housing_id}'
        }), 201

@app.route('/add_family_member', methods=['POST'])
def add_family_member():
    args = request.args
    id = args.get('id')

    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT * FROM households WHERE hid = %s;
    ''', (id,))
    household = cur.fetchone()
    if not household:
        cur.close()
        conn.close()
        resp = {
            "error": "The household id does not exist."
        }
        return jsonify(resp), 400
    
    pid = args.get('pid')
    if not pid:
        cur.close()
        conn.close()
        resp = {
            "error": "Missing person id"
        }
        return jsonify(resp), 400

    cur.execute('''
        SELECT * FROM people WHERE pid = %s;
    ''', (pid,))
    pid_record = cur.fetchone()
    if pid_record:
        cur.close()
        conn.close()
        resp = {
            "error": f"A person with the same id {pid} already exists."
        } 
        return jsonify(resp), 403

    spouse = args.get('spouse')
    if spouse:
        cur.execute('''
            SELECT * FROM people WHERE pid = %s;
        ''', (spouse,))
        spouse_record = cur.fetchone()
        if not spouse_record:
            cur.close()
            conn.close()
            resp = {
                "error": f"Provided spouse id is invalid. Got: {spouse}"
            }
            return jsonify(resp), 403
        
        cur.execute('''
            SELECT *
            FROM people
            WHERE spouse = %s
        ''', (spouse, ))
        record = cur.fetchone()
        if record:
            cur.close()
            conn.close()
            resp = {
                "error": f"Provided spouse id {spouse} is already a spouse of someone else."
            }
            return jsonify(resp), 403

    is_valid, resp, status_code = Person.is_valid(args)
    if not is_valid:
        return jsonify(resp), status_code

    name = args.get('name')
    gender = args.get('gender')
    marital_status = args.get('marital_status')
    occupation_type = args.get('occupation_type')
    annual_income = args.get('annual_income')
    dob = args.get('dob')

    cur.execute('''
        SELECT * FROM add_family_member(%s, %s, %s, %s, %s, %s, %s, %s, %s);
    ''', (id, pid, name, gender, marital_status, spouse, occupation_type, annual_income, dob))

    records = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    household_type = records[0][0]
    family_members = []
    for record in records:
        rec_pid = record[1]
        rec_occupation_type = record[2]
        rec_annual_income = record[3] if record[3] else 0
        rec_dob = record[4]
        family_members.append(Person(rec_pid, rec_annual_income, rec_dob, rec_occupation_type))

    household = Household(HousingType(household_type), family_members)
    check_all_grants(household, id)

    resp = {
        "Success": "Family member {} was added into house {}.".format(pid, id)
    }

    return jsonify(resp), 201
