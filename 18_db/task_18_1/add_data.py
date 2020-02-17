import yaml
import re
from glob import glob
import sqlite3


def add_to_switches(switches_list, switch_table, connection):
    print('Adding data in table "swtiches"')
    for item in switches_list:
        try:
            sql_command_switches = f"INSERT INTO {switch_table} VALUES {item};"
            connection.execute(sql_command_switches)
        except sqlite3.IntegrityError:
            print(f'While adding data: {item} Error is occurred: UNIQUE constraint failed: switches.hostname')


def add_to_dhcp(dhcp_file_list, regexp_device, regexp_dhcp, dhcp_table, connection):
    print('Adding data in table "dhcp"')
    for dhcp_file in dhcp_file_list:
        with open(dhcp_file) as file:
            device_name = re.match(regexp_device, dhcp_file).group()
            # dhcp_value_tuple = [(*item.groups(), device_name) for item in re.finditer(regexp_dhcp, file.read(), re.DOTALL)]
            dhcp_value_tuple = [item.groups() + (device_name,) for item in
                                re.finditer(regexp_dhcp, file.read(), re.DOTALL)]
            for item in dhcp_value_tuple:
                try:
                    sql_command_dhcp = f"INSERT INTO {dhcp_table} VALUES {item};"
                    connection.execute(sql_command_dhcp)
                except sqlite3.IntegrityError:
                    print(f'While adding data: {item} Error is occurred: UNIQUE constraint failed: dhcp.mac')


def add_db_data(yaml_filename, dhcp_file_list, db_filename, switch_table, dhcp_table):

    regexp_dhcp = r"(?P<mac_address>(?:[\dABCDEF]+:){5}[\dABCDEF]+) +" \
                  r"(?P<ip_address>(?:\d+.){3}\d+) +\d+.+?" \
                  r"(?P<vlan_id>\d+) +" \
                  r"(?P<interface_id>\S+)"
    regexp_device = r"\S+\d+"

    with open(yaml_filename) as file:
        switch_info_dict = yaml.safe_load(file)
        """
        Inserting data in one command
        values = ', '.join("('" + str(f"{key}', '{value}").replace('/', '_') + "')" for key, value in switch_info_dict['switches'].items())
        sql_command_switches = f"INSERT INTO {switch_table}(hostname,location) VALUES {values};
        """
        switches_list = list(switch_info_dict['switches'].items())
        connection = sqlite3.connect(db_filename)
        with connection:
            add_to_switches(switches_list, switch_table, connection)
            add_to_dhcp(dhcp_file_list, regexp_device, regexp_dhcp, dhcp_table, connection)
    return None


if __name__ == "__main__":
    dhcp_file_list_glob = sorted(glob('*dhcp_snooping.txt'))
    add_db_data('switches.yml', dhcp_file_list_glob, 'dhcp_snooping.db', 'switches', 'dhcp')