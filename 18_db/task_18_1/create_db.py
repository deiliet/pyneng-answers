
import sys
import re
import glob
import sqlite3


def db_file_create(db_filename='default.db', sql_create_filename='default.sql'):

    db_file_list = sorted(glob.glob(db_filename))
    sql_create_file_list = sorted(glob.glob(sql_create_filename))
    regexp_db = r'\S+(\.db)'
    regexp_sql = r'\S+(\.sql)'
    regexp_sql_create = r'create table (?P<table_name>.*?) \(.*?\);'

    if not db_file_list and 'default.db' in db_filename:
        print('DataBase File is not existed. Empty Default DataBase File is created')
    elif not db_file_list:
        print('DataBase File is not existed. Empty DataBase File is created')
    else:
        print('DataBase File is already existed')
        while True:
            decision = input('Proceed with existing DataBase File? [yes]: ') or 'yes'
            if decision == 'yes' or decision == 'y':
                break
            if decision == 'no' or decision == 'n':
                sys.exit('Change DataBase filename')
            else:
                print('Type yes/y to submit or no/n to decline')
    if not re.match(regexp_db, db_filename):
        print('File is not DataBase or whitespaces are existed')
        sys.exit('Change DataBase filename')

    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    if not sql_create_file_list and 'default.db' in db_filename:
        default_sql_create_file = open(sql_create_filename, 'w')
        default_sql_create_file.close()
        print('SQL-CreateSctipt File is not existed. Empty Default SQL-CreateSctipt File is created')
    elif not sql_create_file_list:
        custom_sql_create_file = open(sql_create_filename, 'w')
        custom_sql_create_file.close()
        print('SQL-CreateSctipt File is not existed. Empty SQL-CreateSctipt File is created')
    else:
        print('SQL-CreateSctipt File is already existed')
        while True:
            decision = input('Proceed with SQL-CreateSctipt File? [yes]: ') or 'yes'
            if decision == 'yes' or decision == 'y':
                break
            if decision == 'no' or decision == 'n':
                sys.exit('Change SQL-CreateSctipt filename')
            else:
                print('Type yes/y to submit or no/n to decline')
    if not re.match(regexp_sql, sql_create_filename):
        print('File is not SQL-CreateSctipt or whitespaces are existed')
        sys.exit('Change SQL-CreateSctipt filename')

    with open(sql_create_filename, 'r') as file:
        for match_index in re.finditer(regexp_sql_create, file.read(), re.DOTALL):
            print(match_index.group())
            if match_index:
                try:
                    cursor.executescript(match_index.group())
                    print(f'Table "{match_index.group("table_name")}" is sucsessfully created')
                except sqlite3.OperationalError:
                    print(f'Table "{match_index.group("table_name")}" in DataBase is already existed')

    return None


if __name__ == "__main__":

    db_file_create('dhcp_snooping.db', 'dhcp_snooping_schema.sql')
