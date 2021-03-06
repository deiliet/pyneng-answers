# -*- coding: utf-8 -*-
'''
Задание 7.1

Аналогично заданию 4.6 обработать строки из файла ospf.txt
и вывести информацию по каждой в таком виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

with open('ospf.txt', 'r') as route:
    for line in route:
        _, prefix, AD, _, nexthop, time, intf = line.split()
        AD = AD.strip('[]')
        nexthop = nexthop.strip(',')
        time = time.strip(',')
        table = f"""\033[93m
        Protocol:              OSPF
        Prefix:                {prefix}
        AD/Metric:             {AD}
        Next-Hop:              {nexthop}
        Last update:           {time}
        Outbound Interface:    {intf}
        """
        print(table)