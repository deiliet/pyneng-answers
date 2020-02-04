# -*- coding: utf-8 -*-
'''
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию:
    - добавить поддержку конфигурации, когда настройка access-порта выглядит так:
            interface FastEthernet0/20
                switchport mode access
                duplex auto
      То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
      Пример словаря: {'FastEthernet0/12': 10,
                       'FastEthernet0/14': 11,
                       'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

# python task_9_3a.py config_sw2.txt

from sys import argv
from pprint import pprint


def get_int_vlan_map(config_filename):
    access_vlans = {}
    trunk_vlans = {}
    with open(config_filename, 'r') as file:
        interface_id = ''
        for line in file:
            if line.startswith('interface'):
                if not (access_vlans.get(interface_id) or trunk_vlans.get(interface_id)) and interface_id != '':
                    access_vlans[interface_id] = 1
                _, interface_id = line.split()
                continue
            if 'allowed vlan' in line:
                trunk_vlans[interface_id] = \
                    [int(vlan_id) for vlan_id in line.split()[4].split(',')]
                continue
            if 'access vlan' in line:
                access_vlans[interface_id] = int(line.split()[3])
    return access_vlans, trunk_vlans

# access, trunk = get_int_vlan_map(argv[1])
access, trunk = get_int_vlan_map('config_sw2.txt')
pprint(access)
pprint(trunk)