#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import parse_dhcp_snooping_functions as pds
import sys
sys.argv += 'get --db dhcp_snooping.db -k vlan -v 10'.split()
"""
python3 parse_dhcp_snooping.py add -s --db dhcp_snooping.db switches.yml
python3 parse_dhcp_snooping.py add --db dhcp_snooping.db sw1_dhcp_snooping.txt sw2_dhcp_snooping.txt sw3_dhcp_snooping.txt 
python3 parse_dhcp_snooping.py get --db dhcp_snooping.db -k vlan -v 10
"""


# Default values:
DFLT_DB_NAME = 'dhcp_snooping.db'
DFLT_DB_SCHEMA = 'dhcp_snooping_schema.sql'


def create(args):
    print('Создаю БД {} со схемой {}'.format(args.name, args.schema))
    pds.create_db(args.name, args.schema)


def add(args):
    if args.sw_true:
        print('Добавляю данные о коммутаторах')
        pds.add_data_switches(args.db_file, args.filename)
    else:
        print('Читаю информацию из файлов\n{}'.format(', '.join(
            args.filename)))
        print('\nДобавляю данные по DHCP записям в {}'.format(args.db_file))
        pds.add_data(args.db_file, args.filename)


def get(args):
        args_list = [args.key, args.value]
        pds.get_data(args.db_file, args_list)


def show_subparser_help(subparser_name):
    '''
    Function returns help message for subparser
    '''
    subparsers_actions = [
        action for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)
    ]
    return subparsers_actions[0].choices[subparser_name].format_help()


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='subcommands',
                                   description='команды',
                                   help='дополнительная информация')

create_parser = subparsers.add_parser('create_db', help='создать новую базу данных')
create_parser.add_argument('-n', dest='name', default=DFLT_DB_NAME,
                           help='имя БД')
create_parser.add_argument('-s', dest='schema', default=DFLT_DB_SCHEMA,
                           help='схема БД')
create_parser.set_defaults(func=create)

add_parser = subparsers.add_parser('add', help='добавить данные в БД')
add_parser.add_argument('filename', nargs='+',
                        help='файл(ы), которые надо добавить')
add_parser.add_argument('--db', dest='db_file', default=DFLT_DB_NAME,
                        help='имя БД')
add_parser.add_argument('-s', dest='sw_true', action='store_true',
                        help=('если флаг установлен, добавлять '
                              'данные коммутаторов, иначе добавлять DHCP записи'))
add_parser.set_defaults(func=add)

get_parser = subparsers.add_parser('get', help='отобразить данные из БД')
get_parser.add_argument('--db', dest='db_file', default=DFLT_DB_NAME,
                        help='имя БД')
get_parser.add_argument('-k', dest='key',
                        choices=['mac', 'ip', 'vlan', 'interface', 'switch'],
                        help='параметр для поиска записей')
get_parser.add_argument('-v', dest='value', help='значение параметра')
get_parser.add_argument('-a', action='store_true', help='показать все содержимое БД')
get_parser.set_defaults(func=get)


if __name__ == '__main__':
    args = parser.parse_args()
    if not vars(args):
        parser.print_usage()
    else:
        args.func(args)
