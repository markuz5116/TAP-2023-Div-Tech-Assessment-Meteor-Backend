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
cur.execute('DROP FUNCTION IF EXISTS add_family_member;')
cur.execute('DROP FUNCTION IF EXISTS list_households;')
cur.execute('DROP FUNCTION IF EXISTS get_household;')
cur.execute('DROP FUNCTION IF EXISTS get_eligible_members;')

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
    'check (gender in (\'male\', \'female\', \'other\', \'prefer not to say\')),'
    'check (maritalStatus in (\'single\', \'married\', \'widowed\', \'separated\', \'divorced\', \'others\'))'
    ');'
    )

cur.execute('''
    CREATE TABLE eligible_schemes_for_people(
        schemeName VARCHAR(100) NOT NULL,
        pid varchar(9) NOT NULL REFERENCES people(pid),
        PRIMARY KEY (schemeName, pid),
        check (schemeName in ('student encouragement bonus', 'multigeneration scheme', 'elder bonus', 'baby sunshine grant', 'yolo gst grant'))
    );
    ''')

cur.execute('''
    CREATE OR REPLACE FUNCTION add_household(IN housingType VARCHAR(20))
    RETURNS INT AS $$
    DECLARE 
        maxId INTEGER := 0;
    BEGIN
        SELECT max(hid) INTO maxId
        FROM households;

        maxId := COALESCE(maxId + 1, 1);

        INSERT INTO households VALUES
        (maxId, housingType);

        RETURN maxId;
    END;
    $$ LANGUAGE plpgsql;
''')

cur.execute('''
    CREATE OR REPLACE FUNCTION add_family_member(IN inHid INTEGER, IN pid VARCHAR(9), IN inName VARCHAR(50), IN gender VARCHAR(20), IN maritalStatus VARCHAR(50), IN spouse VARCHAR(9), IN occupationType VARCHAR(50), IN inAnnualIncome NUMERIC(10, 2), IN inDob DATE)
    RETURNS TABLE (outHousingType VARCHAR(20), outPid VARCHAR(9), outOccupationType VARCHAR(50), outAnnualIncome NUMERIC(10, 2), outDob DATE) AS $$
    BEGIN
        INSERT INTO people VALUES 
        (pid, inName, gender, maritalStatus, spouse, occupationType, inAnnualIncome, inDob, inHid);

        RETURN QUERY 
            SELECT H.housingType, P.pid, P.occupationType, P.annualIncome, P.dob
            FROM households H natural join people P
            where H.hid = inHid;
    END;
    $$ LANGUAGE plpgsql;
''')

cur.execute('''
    CREATE OR REPLACE FUNCTION list_households()
    RETURNS TABLE (outHid INTEGER, outHousingType VARCHAR(20), outName VARCHAR(50), outGender VARCHAR(20), outMaritalStatus VARCHAR(50), outSpouse VARCHAR(9), outOccupationType VARCHAR(50), outAnnualIncome NUMERIC(10, 2), outDob DATE) AS $$
    BEGIN
        RETURN QUERY
            SELECT H.hid, H.housingType, P.name, P.gender, P.maritalStatus, P.spouse, P.occupationType, P.annualIncome, P.dob
            FROM people P natural join households H;
    END;
    $$ LANGUAGE plpgsql;
''')

cur.execute('''
    CREATE OR REPLACE FUNCTION get_household(IN inHid INTEGER)
    RETURNS TABLE (outHid INTEGER, outHousingType VARCHAR(20), outName VARCHAR(50), outGender VARCHAR(20), outMaritalStatus VARCHAR(50), outSpouse VARCHAR(9), outOccupationType VARCHAR(50), outAnnualIncome NUMERIC(10, 2), outDob DATE) AS $$
    BEGIN
        RETURN QUERY
            SELECT H.hid, H.housingType, P.name, P.gender, P.maritalStatus, P.spouse, P.occupationType, P.annualIncome, P.dob
            FROM people P natural join households H
            WHERE H.hid = inHid;
    END;
    $$ LANGUAGE plpgsql;
''')

cur.execute('''
    CREATE OR REPLACE FUNCTION get_eligible_members(IN inSchemeName VARCHAR(100))
    RETURNS TABLE (outHid INTEGER, outHousingType VARCHAR(20), outName VARCHAR(50), outGender VARCHAR(20), outMaritalStatus VARCHAR(50), outSpouse VARCHAR(9), outOccupationType VARCHAR(50), outAnnualIncome NUMERIC(10, 2), outDob DATE) AS $$
    BEGIN
        RETURN QUERY
            SELECT H.hid, H.housingType, P.name, P.gender, P.maritalStatus, P.spouse, P.occupationType, P.annualIncome, P.dob
            FROM eligible_schemes_for_people E natural join people P natural join households H
            WHERE E.schemeName = inSchemeName; 
    END;
    $$ LANGUAGE plpgsql;
''')

cur.execute('''
    CREATE OR REPLACE FUNCTION check_for_duplicate() RETURNS TRIGGER AS $$
    DECLARE
        rec RECORD;
    BEGIN
        SELECT schemeName, pid INTO rec
        FROM eligible_schemes_for_people
        WHERE schemeName = NEW.schemeName and pid = NEW.pid;

        if rec IS NULL then
            RETURN NEW;
        end if;

        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER check_for_duplicate_trigger
    BEFORE INSERT ON eligible_schemes_for_people
    FOR EACH ROW EXECUTE FUNCTION check_for_duplicate();
''')

cur.execute('''
    CREATE OR REPLACE FUNCTION remove_valid_members(IN inSchemeName VARCHAR(100), IN inHid INTEGER)
    RETURNS VOID AS $$
    BEGIN
        DELETE FROM eligible_schemes_for_people
        WHERE pid = ANY(
            SELECT pid
            FROM eligible_schemes_for_people E natural join people P natural join households H
            where H.hid = inHid
        ) and schemeName = inSchemeName;
    END;
    $$ LANGUAGE plpgsql;
''')

# Add sample inputs
cur.execute('INSERT INTO households values'
    '(1, \'landed\'),'
    '(2, \'condominium\'),'
    '(3, \'hdb\');'
    )

conn.commit()
cur.close()
conn.close()