import os
from tkinter import INSERT
import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='tap_meteor',
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD']
)

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS households;')
cur.execute('DROP TABLE IF EXISTS people;')

cur.execute('CREATE TABLE households(hid varchar(50) PRIMARY KEY,'
    'householdType varchar(50) NOT NULL,'
    'check (householdType in (\'Landed\', \'Condominium\', \'HDB\'))'
    ');'
    )

cur.execute('CREATE TABLE people(pid varchar(9) PRIMARY KEY,'
    'name varchar(50) NOT NULL,'
    'gender varchar(20) NOT NULL,'
    'maritalStatus varchar(50) NOT NULL,'
    'spouse varchar(9) REFERENCES people(pid),'
    'occupationType varchar(50) NOT NULL,'
    'annualIncome numeric(10, 2),'
    'dob date NOT NULL,'
    'hid varchar(50) REFERENCES households(hid)'
    'check (annualIncome >= 0),'
    'check (gender in (\'male\', \'female\', \'prefer not to say\'))'
    ');'
    )

cur.execute('CREATE TABLE eligible_schemes_for_people(scheme_name VARCHAR(100) NOT NULL,'
    'pid varchar(9) NOT NULL REFERENCES people(pid),'
    'PRIMARY KEY (scheme_name, pid)'
    )

# Add sample inputs
cur.execute('INSERT INTO households values'
    '(\'h1\', \'Landed\'),'
    '(\'h2\', \'Condominium\'),'
    '(\'h3\', \'HDB\');'
    )

cur.execute('INSERT INTO people values'
    '(\'S1111111A\', \'person1\', \'male\', \'single\', NULL, \'studying\', 1, \'1998-12-19\', \'h1\'),'
    '(\'T2222222B\', \'person2\', \'female\', \'married\', \'S3333333C\', \'full-time\', 2000, \'2000-01-01\', \'h2\'),'
    '(\'S3333333C\', \'person3\', \'male\', \'attached\', \'T2222222B\', \'part-time\', 300, \'1990-06-30\', \'h2\'),'
    '(\'T4444444B\', \'person4\', \'prefer not to say\', \'single\', NULL, \'studying\', NULL, \'1998-12-19\', \'h3\');'
    )


conn.commit()
cur.close()
conn.close()