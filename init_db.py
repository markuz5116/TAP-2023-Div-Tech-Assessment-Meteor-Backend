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

cur.execute('DROP FUNCTION IF EXISTS add_household;')

cur.execute('DROP TABLE IF EXISTS eligible_schemes_for_people;')
cur.execute('DROP TABLE IF EXISTS people;')
cur.execute('DROP TABLE IF EXISTS households;')

cur.execute('CREATE TABLE households(hid INTEGER PRIMARY KEY,'
    'housingType varchar(20) NOT NULL,'
    'check (housingType in (\'landed\', \'condominium\', \'hdb\'))'
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
    'hid INTEGER REFERENCES households(hid)'
    'check (annualIncome >= 0),'
    'check (gender in (\'male\', \'female\', \'prefer not to say\'))'
    ');'
    )

cur.execute('CREATE TABLE eligible_schemes_for_people(scheme_name VARCHAR(100) NOT NULL,'
    'pid varchar(9) NOT NULL REFERENCES people(pid),'
    'PRIMARY KEY (scheme_name, pid)'
    ');'
    )

# Add sample inputs
cur.execute('INSERT INTO households values'
    '(1, \'landed\'),'
    '(2, \'condominium\'),'
    '(3, \'hdb\');'
    )

cur.execute('INSERT INTO people values'
    '(\'S1111111A\', \'person1\', \'male\', \'single\', NULL, \'studying\', 1, \'1998-12-19\', 1),'
    '(\'T2222222B\', \'person2\', \'female\', \'married\', \'S3333333C\', \'full-time\', 2000, \'2000-01-01\', 2),'
    '(\'S3333333C\', \'person3\', \'male\', \'attached\', \'T2222222B\', \'part-time\', 300, \'1990-06-30\', 2),'
    '(\'T4444444B\', \'person4\', \'prefer not to say\', \'single\', NULL, \'studying\', NULL, \'1998-12-19\', 3);'
    )

cur.execute('''
    CREATE OR REPLACE FUNCTION add_household(IN housingType VARCHAR(20))
    RETURNS INT AS $$
    DECLARE 
        maxId INTEGER := 0;
    BEGIN
        SELECT max(hid) INTO maxId
        FROM households;

        maxId := maxId + 1;

        INSERT INTO households values
        (maxId, housingType);

        RETURN maxId;
    END;
    $$ LANGUAGE plpgsql;
''')


conn.commit()
cur.close()
conn.close()