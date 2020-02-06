# -*- coding: utf-8 -*-
'''
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

import subprocess


def ping_ip_addresses(ip_address_list):
    reachable_ip = []
    unreachable_ip = []
    for ip in ip_address_list:
        result = subprocess.run(
            f'ping -c 5 {ip}', stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
        if result.returncode == 0:
            reachable_ip.append(ip)
        else:
            unreachable_ip.append(ip)
    return reachable_ip, unreachable_ip


if __name__ == "__main__":
    test_list = ['8.8.8.8', '8.8.4.4', '10.54.14.1']
    print(ping_ip_addresses(test_list))