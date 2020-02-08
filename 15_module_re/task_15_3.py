# -*- coding: utf-8 -*-
'''
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
'''

import re


def convert_ios_nat_to_asa(ios_filename, asa_filename):
    regexp_nat = r'(?P<ip>(?:\d{1,3}\.){3}\d{1,3}) +(?P<port_inside>\d{1,5}).+ +(?P<port_outside>\d{1,5})'
    with open(ios_filename) as ios_config, open(asa_filename, 'w') as asa_config:
        for match_index in re.finditer(regexp_nat, ios_config.read()):
            asa_config.write(f"object network LOCAL{match_index.group('ip')}" + '\n')
            asa_config.write(f" host {match_index.group('ip')}" + '\n')
            asa_config.write(f" nat (inside,outside) static interface service tcp"
                             f" {match_index.group('port_inside')}"
                             f" {match_index.group('port_outside')}" + '\n')


if __name__ == "__main__":
    convert_ios_nat_to_asa("cisco_nat_config.txt", "asa_nat_config.txt")