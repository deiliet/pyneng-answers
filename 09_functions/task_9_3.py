# -*- coding: utf-8 -*-
'''
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный файл коммутатора
и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов, а значения access VLAN:
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов, а значения список разрешенных VLAN:
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

# python task_9_3.py config_sw1.txt

from sys import argv


def get_int_vlan_map(config_filename):
    access_vlans = {}
    trunk_vlans = {}
    with open(config_filename, 'r') as file:
        for line in file:
            if line.startswith('interface'):
                _, interface_id = line.split()
                continue
            if 'allowed vlan' in line:
                trunk_vlans[interface_id] = \
                    [int(vlan_id) for vlan_id in line.split()[4].split(',')]
                continue
            if 'access vlan' in line:
                access_vlans[interface_id] = int(line.split()[3])
    return access_vlans, trunk_vlans


# print(get_int_vlan_map(argv[1]))


access, trunk = get_int_vlan_map(argv[1])
print(access)
print(trunk)