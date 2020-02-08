# -*- coding: utf-8 -*-
'''
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.


Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
'''

import re
from pprint import pprint

"""
def get_ints_without_description(filename):
    no_description_list = []
    regex = r"(?:^interface (\S+)|description (\S+))"
    interface = ""
    with open(filename) as file:
        for line in file:
            match = re.search(regex,line)
            if match and match.lastindex == 1:
                interface = match.group(match.lastindex)
            elif interface and match and match.lastindex == 2:
                interface = ""
            elif interface != "":
                result.append(interface)
                interface = ""
"""

"""
def get_ints_without_description(filename):
    no_description_list = []
    regexp = r"^interface (\S+)\n(?! description)"
    with open(filename) as file:
        for match_index in re.finditer(regexp, file.read(), re.MULTILINE):
            if match_index:
                no_description_list.append(match_index.group(1))
    return no_description_list
"""


def get_ints_without_description(filename):
    regexp = r"^interface (\S+)\n(?! description)"
    with open(filename) as file:
        no_description_list = [match.group(1) for match in
                               re.finditer(regexp, file.read(), re.MULTILINE)]
    return no_description_list


if __name__ == "__main__":
    pprint(get_ints_without_description("config_r1.txt"))