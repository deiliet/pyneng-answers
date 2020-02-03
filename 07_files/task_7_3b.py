# -*- coding: utf-8 -*-
'''
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Дополнить скрипт:
- Запросить у пользователя ввод номера VLAN или нескольких VLAN-ов.
- Выводить информацию только по указанным VLAN-нам.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

from operator import itemgetter

list = []

user_vlan = input("Введите номера VLAN-ов: ")

user_vlan_list = user_vlan.split(',')

with open('CAM_table.txt', 'r') as cam_table:
    for line in cam_table:
        if 'DYNAMIC' in line:
            vlan, mac_add, _, port = line.split()
            if vlan in user_vlan_list:
                list.append((int(vlan), mac_add, port))

list.sort(key=itemgetter(0))
for line in list:
    vlan, mac_add, port = line
    print(f"\033[93m{vlan:<7}{mac_add}{port:>8}")