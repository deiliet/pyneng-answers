import sqlite3
import sys
from sys import argv, exit
from tabulate import tabulate


def args_checker(connection, args):
    if len(args) == 1:
        sql_request = connection.execute('SELECT * FROM dhcp')
        print('Table "dhcp" consists of such entries:')
    elif len(args) == 3:
        try:
            sql_request = connection.execute(f"SELECT * FROM dhcp WHERE {args[1]} = '{args[2]}'")
            print(f"Information of devices with such parameters ({args[1]}) & ({args[2]})")
        except sqlite3.OperationalError:
            print(f"Such parameter ({args[1]}) is not suppurted.")
            print("Valid parameter values: mac, ip, vlan, interface, switch)")
            sys.exit(1)
    else:
        exit('Script can contain only zero or two arguments')
    return sql_request


def execute_sql(sql_request):
    headers = tuple([i[0] for i in sql_request.description])
    table_view = sql_request.fetchall()
    print(tabulate(table_view, headers, tablefmt="psql", stralign='center'))
    return None
    

def get_data(db_filename, args):
    connection = sqlite3.connect(db_filename)
    with connection:
        sql_request = args_checker(connection, args)
        execute_sql(sql_request)
    return None


if __name__ == "__main__":
    get_data('dhcp_snooping.db', argv)
