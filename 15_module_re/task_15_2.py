# -*- coding: utf-8 -*-
'''
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

'''

import re


def parse_sh_ip_int_br(filename):
    int_br_list = []
    regexp_int_br = r'(?P<int>\S+) +(?P<ip>\S+).+?(?P<status>(?:administratively down|up|down)) +(?P<protocol>(?:up|down))'
    with open(filename) as file:
        for line in file:
            match = re.search(regexp_int_br, line)
            if match:
                int_br_list.append(match.groups())
    return int_br_list


if __name__ == "__main__":
    print(parse_sh_ip_int_br("sh_ip_int_br.txt"))
