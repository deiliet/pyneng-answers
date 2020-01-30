# -*- coding: utf-8 -*-
'''
Задание 4.6

Обработать строку ospf_route и вывести информацию на стандартный поток вывода в виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ospf_route = 'O        10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0'

result = ospf_route.split()
table = f"""\033[93m
Protocol:              OSPF
Prefix:                {result[1]}
AD/Metric:             {result[2][1:-1]}
Next-Hop:              {result[4][:-1]}
Last update:           {result[5][:-1]}
Outbound Interface:    {result[6]}
"""
print(table)


