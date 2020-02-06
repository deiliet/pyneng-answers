# -*- coding: utf-8 -*-
'''
Задание 12.2


Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона, например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список, где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список IP-адресов и/или диапазонов IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только последний октет адреса.

Функция возвращает список IP-адресов.


Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

'''

import ipaddress

def check_ip_addresses(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def convert_ranges_to_ip_list(ip_ranges_list):
    ip_list = []
    for ip_range in ip_ranges_list:
        if '-' in ip_range:
            start, end = ip_range.split("-")
            if check_ip_addresses(end) and check_ip_addresses(start):
                start_ip = ipaddress.ip_address(start)
                end_ip = ipaddress.ip_address(end)
            elif check_ip_addresses(start):
                start_ip = ipaddress.ip_address(start)
                end_ip = ipaddress.ip_address(
                    ".".join(start.split(".")[:3]+list(end))
                )
            while start_ip <= end_ip:
                ip_list.append(str(start_ip))
                start_ip +=1
        elif check_ip_addresses(ip_range):
            ip_list.append(ip_range)
    return ip_list


if __name__ == "__main__":
    ip_ranges_list = ['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']
    print(convert_ranges_to_ip_list(ip_ranges_list))