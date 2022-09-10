import os
import psycopg2
from flask import Flask, jsonify, request

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
       return jsonify({ "Error": 'Missing housing_type'}), 400

    housing_type = housing_type.lower()
    if housing_type not in ['landed', 'condominium', 'hdb']:
        return jsonify({ "Error": f'housing_type must be landed, condominium or hdb, got: {housing_type}'}), 403
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM add_household(\'{housing_type}\')')
    housing_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"Success": f'House added with id: {housing_id}'}), 201