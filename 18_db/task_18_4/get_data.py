import sqlite3
import sys
from sys import argv, exit
from tabulate import tabulate


def args_checker(connection, args):
    if len(args) == 1:
        sql_request_acitve = connection.execute("SELECT * FROM dhcp WHERE active = '1'")
        sql_request_outdated = connection.execute("SELECT * FROM dhcp WHERE active = '0'")
        print('Table "dhcp" consists of such entries:')
    elif len(args) == 3:
        try:
            sql_request_acitve = connection.execute(f"SELECT * FROM dhcp WHERE {args[1]} = '{args[2]}' AND active = '1'")
            sql_request_outdated = connection.execute(f"SELECT * FROM dhcp WHERE {args[1]} = '{args[2]}' AND active = '0'")
            print(f"Information of devices with such parameters ({args[1]}) & ({args[2]})")
        except sqlite3.OperationalError:
            print(f"Such parameter ({args[1]}) is not suppurted.")
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


if __name__ == "__main__":
    get_data('dhcp_snooping.db', argv)
