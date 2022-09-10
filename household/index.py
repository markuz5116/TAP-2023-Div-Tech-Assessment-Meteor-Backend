import json
import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

def connect_to_db():
    conn = psycopg2.connect(host='localhost',
        database='tap_meteor',
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])
    return conn

@app.route('/', methods=['GET'])
def index():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM people;')
    people = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(people)