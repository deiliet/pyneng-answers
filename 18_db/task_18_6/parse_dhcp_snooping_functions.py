import glob
import yaml
import re
import sqlite3
import sys
from glob import glob
from datetime import timedelta, datetime
from tabulate import tabulate


def db_file_checker(db_file_list, db_filename, regexp_db):
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
    return None


def sql_create_file_checker(sql_create_file_list, sql_create_filename, regexp_sql, regexp_sql_create):
    if not sql_create_file_list and 'default.sql' in sql_create_filename:
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
    return None


def execute_sql_create(sql_create_filename, regexp_sql_create, cursor):
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


def create_db(db_filename='default.db', sql_create_filename='default.sql'):
    db_file_list = sorted(glob.glob(db_filename))
    sql_create_file_list = sorted(glob.glob(sql_create_filename))
    regexp_db = r'\S+(\.db)'
    regexp_sql = r'\S+(\.sql)'
    regexp_sql_create = r'create table (?P<table_name>.*?) \(.*?\);'

    db_file_checker(db_file_list, db_filename, regexp_db)
    sql_create_file_checker(sql_create_file_list, sql_create_filename, regexp_sql, regexp_sql_create)

    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    execute_sql_create(sql_create_filename, regexp_sql_create, cursor)
    return None


''''''''''''''''''''''''''''''''''''''''''''''''''


def add_data_switches(db_filename, yaml_filename):
    connection = sqlite3.connect(db_filename)
    for filename in yaml_filename:
        with open(filename) as file:
            switch_info_dict = yaml.safe_load(file)
            switches_list = list(switch_info_dict['switches'].items())
        print('Adding data in table "switches"')
        for item in switches_list:
            try:
                sql_command_switches = f"INSERT INTO switches VALUES {item};"
                connection.execute(sql_command_switches)
            except sqlite3.IntegrityError:
                print(f'While adding data: {item} Error is occurred: UNIQUE constraint failed: switches.hostname')
    return None


def add_data(db_filename, dhcp_file_list):
    regexp_dhcp = r"(?P<mac_address>(?:[\dABCDEF]+:){5}[\dABCDEF]+) +" \
                  r"(?P<ip_address>(?:\d+.){3}\d+) +\d+.+?" \
                  r"(?P<vlan_id>\d+) +" \
                  r"(?P<interface_id>\S+)"
    regexp_device = r"sw\d+"
    connection = sqlite3.connect(db_filename)
    time_str = datetime.now().strftime("%B %d, %Y %I:%M%p")
    test_ago_str = (datetime.now() - timedelta(days=8)).strftime("%B %d, %Y %I:%M%p")
    week_ago = (datetime.now() - timedelta(days=7))
    print('Adding data in table "dhcp"')
    data_request = connection.execute('SELECT * FROM dhcp')
    for dhcp_file in dhcp_file_list:
        with open(dhcp_file) as file:
            device_name = re.search(regexp_device, dhcp_file).group()
            dhcp_value_tuple = [item.groups() + (device_name, 1, time_str) for item in
                                re.finditer(regexp_dhcp, file.read(), re.DOTALL)]
            for value in dhcp_value_tuple:
                try:
                    sql_command_dhcp = f"INSERT INTO dhcp VALUES {value};"
                    connection.execute(sql_command_dhcp)
                except sqlite3.IntegrityError:
                    sql_command_dhcp = f"REPLACE INTO dhcp VALUES {value};"
                    connection.execute(sql_command_dhcp)
                for data in data_request:
                    if value[0] not in data or value[1] not in data or value[2] not in data or value[3] not in data:
                        sql_command_dhcp = f"UPDATE dhcp set active = '0', last_active = '{test_ago_str}' WHERE mac = '{data[0]}';"
                        connection.execute(sql_command_dhcp)
                    if datetime.strptime(value[6], "%B %d, %Y %I:%M%p") >= week_ago:
                        sql_command_dhcp = f"DELETE FROM dhcp WHERE mac = '{data[0]}';"
                        connection.execute(sql_command_dhcp)
    return None


''''''''''''''''''''''''''''''''''''''''''''''''''


def args_checker(connection, args):
    if len(args) == 0:
        sql_request_acitve = connection.execute("SELECT * FROM dhcp WHERE active = '1'")
        sql_request_outdated = connection.execute("SELECT * FROM dhcp WHERE active = '0'")
        print('Table "dhcp" consists of such entries:')
    elif len(args) == 2:
        try:
            sql_request_acitve = connection.execute(
                f"SELECT * FROM dhcp WHERE {args[0]} = '{args[1]}' AND active = '0'")
            sql_request_outdated = connection.execute(
                f"SELECT * FROM dhcp WHERE {args[0]} = '{args[1]}' AND active = '0'")
            print(f"Information of devices with such parameters ({args[0]}) & ({args[1]})")
        except sqlite3.OperationalError:
            print(f"Such parameter ({args[0]}) is not suppurted.")
            print("Valid parameter values: mac, ip, vlan, interface, switch)")
            sys.exit(1)
    else:
        exit('Script can contain only zero or two arguments')
    return sql_request_acitve, sql_request_outdated


def execute_sql(sql_request):
    headers = tuple([i[0] for i in sql_request.description])
    table_view = sql_request.fetchall()
    print(tabulate(table_view, headers, tablefmt="psql", stralign='center'))
    return None


def get_data(db_filename, args):
    connection = sqlite3.connect(db_filename)
    with connection:
        sql_request_acitve, sql_request_outdated = args_checker(connection, args)
        if sql_request_acitve:
            print('Active entries:')
            execute_sql(sql_request_acitve)
        if sql_request_outdated:
            print('Outdated entries:')
            execute_sql(sql_request_outdated)
    return None

