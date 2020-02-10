# -*- coding: utf-8 -*-
'''
Задание 17.2

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'}, 'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
'''

import re
from pprint import pprint


def parse_sh_cdp_neighbors(file_single_line):
    regex_host = r'(?P<local_device>\S+)>'
    regex_params = r'(?P<remote_device>\S+?) +' \
                   r'(?P<local_port>\w+? \S+) +\d+.+ +' \
                   r'(?P<remote_port>\w+? \S+)'
    host_key = re.search(regex_host, file_single_line)

    "forming a structure of attached dictionaries according to exercise"

    params_dict = {host_key.group('local_device'):  # first_key:
                  {match.group('local_port'):  # second_key:
                  {match.group('remote_device'): match.group('remote_port')}  # third_key: value
                  for match in re.finditer(regex_params, file_single_line)}}
    return params_dict


if __name__ == "__main__":
    with open('sh_cdp_n_sw1.txt') as file:
        sh_cdp_nei_files = parse_sh_cdp_neighbors(file.read())
    pprint(sh_cdp_nei_files)
