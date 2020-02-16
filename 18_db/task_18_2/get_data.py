import sqlite3
from sys import argv, exit
from tabulate import tabulate


def get_data(db_filename, args):
    connection = sqlite3.connect(db_filename)
    with connection:
        if len(args) == 1:
            result = connection.execute('SELECT * FROM dhcp')
            headers = tuple([i[0] for i in result.description])
            table_view = result.fetchall()
            print(tabulate(table_view, headers, tablefmt="psql", stralign='center'))
        elif len(args) == 3:
            # print(args[1:])
            # result = connection.execute("SELECT * FROM dhcp WHERE ? = '?'", args[1:])
            # "SELECT * from %s WHERE name = ?" % table_name, (name,)
            result = connection.execute(f"SELECT * FROM dhcp WHERE {args[1]} = '{args[2]}'")
            headers = tuple([i[0] for i in result.description])
            table_view = result.fetchall()
            print(tabulate(table_view, headers, tablefmt="psql", stralign='center'))
        else:
            exit('Script can contain only zero or two arguments')
    return None


if __name__ == "__main__":
    get_data('dhcp_snooping.db', argv)


