import os
import psycopg2
from flask import Flask, jsonify, request

from household.model.person import Person

app = Flask(__name__)

def connect_to_db():
    conn = psycopg2.connect(host='localhost',
        database='tap_meteor',
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])
    return conn

@app.route('/household', methods=['POST'])
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
    cur.execute(f'SELECT * FROM add_household(\'{housing_type}\')')
    housing_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({
        "Success": f'House added with id: {housing_id}'
        }), 201

@app.route('/household/<id>', methods=['POST'])
def add_family_member(id):
    conn = connect_to_db()
    cur = conn.cursor()
    
    cur.execute(f'''
        SELECT * FROM households WHERE hid = {id};
    ''')
    household = cur.fetchone()
    if not household:
        cur.close()
        conn.close()
        resp = {
            "error": "The household id does not exist."
        }
        return jsonify(resp), 400

    args = request.args
    pid = args.get('id')
    if not pid:
        resp = {
            "error": "Missing person id"
        }
        return jsonify(resp), 400
    cur.execute(f'''
        SELECT * FROM people WHERE pid = \'{pid}\';
    ''')
    pid_record = cur.fetchone()
    if pid_record:
        resp = {
            "error": f"A person with the same id {pid} already exists."
        } 
        return jsonify(resp), 403

    spouse = args.get('spouse')
    if spouse:
        cur.execute(f'''
            SELECT * FROM people WHERE pid = \'{spouse}\';
        ''')
        spouse_record = cur.fetchone()
        if not spouse_record:
            cur.close()
            conn.close()
            resp = {
                "error": f"Provided spouse id is invalid. Got: {spouse}"
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

    household = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    resp = {
        "Success": "Family member {} was added into house {}.".format(pid, id),
        "household": household
    }

    return jsonify(resp), 200
