import yaml
import re
from glob import glob
import sqlite3
from datetime import timedelta, datetime


def add_to_switches(yaml_filename, switch_table, connection):
    with open(yaml_filename) as file:
        switch_info_dict = yaml.safe_load(file)
        switches_list = list(switch_info_dict['switches'].items())
    print('Adding data in table "swtiches"')
    for item in switches_list:
        try:
            sql_command_switches = f"INSERT INTO {switch_table} VALUES {item};"
            connection.execute(sql_command_switches)
        except sqlite3.IntegrityError:
            print(f'While adding data: {item} Error is occurred: UNIQUE constraint failed: switches.hostname')
    return None


def add_to_dhcp(dhcp_file_list, regexp_device, regexp_dhcp, dhcp_table, connection):
    time = datetime.now().strftime("%B %d, %Y %I:%M%p")
    # week_ago = time - timedelta(days=7)
    print('Adding data in table "dhcp"')
    data_request = connection.execute('SELECT * FROM dhcp')
    for dhcp_file in dhcp_file_list:
        with open(dhcp_file) as file:
            device_name = re.search(regexp_device, dhcp_file).group()
            dhcp_value_tuple = [item.groups() + (device_name, 1, time) for item in
                                re.finditer(regexp_dhcp, file.read(), re.DOTALL)]
            for value in dhcp_value_tuple:
                try:
                    sql_command_dhcp = f"INSERT INTO {dhcp_table} VALUES {value};"
                    connection.execute(sql_command_dhcp)
                except sqlite3.IntegrityError:
                    sql_command_dhcp = f"REPLACE INTO {dhcp_table} VALUES {value};"
                    connection.execute(sql_command_dhcp)
                for data in data_request:
                    if value[0] not in data or value[1] not in data or value[2] not in data or value[3] not in data:
                        sql_command_dhcp = f"UPDATE {dhcp_table} set active = '0', last_active = '{time}' WHERE mac = '{data[0]}';"
                        connection.execute(sql_command_dhcp)
    return None


def add_db_data(yaml_filename, dhcp_file_list, db_filename, switch_table, dhcp_table):
    regexp_dhcp = r"(?P<mac_address>(?:[\dABCDEF]+:){5}[\dABCDEF]+) +" \
                  r"(?P<ip_address>(?:\d+.){3}\d+) +\d+.+?" \
                  r"(?P<vlan_id>\d+) +" \
                  r"(?P<interface_id>\S+)"
    regexp_device = r"sw\d+"
    connection = sqlite3.connect(db_filename)
    with connection:
        add_to_switches(yaml_filename, switch_table, connection)
        add_to_dhcp(dhcp_file_list, regexp_device, regexp_dhcp, dhcp_table, connection)
    return None


if __name__ == "__main__":
    dhcp_file_list_glob = sorted(glob('new_data/*dhcp_snooping.txt'))
    add_db_data('switches.yml', dhcp_file_list_glob, 'dhcp_snooping.db', 'switches', 'dhcp')