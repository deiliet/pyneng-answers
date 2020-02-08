# -*- coding: utf-8 -*-
'''
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом, чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1':('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2':('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

'''

import re


def get_ip_from_cfg(filename):
    prefix_dict = {}
    regexp_interface = r'interface (?P<int>\S+)'
    regexp_prefix = r'ip address (?P<ip>(?:\d{1,3}\.){3}\d{1,3})\s(?P<mask>(?:\d{1,3}\.){3}\d{1,3})'
    with open(filename) as file:
        for line in file:
            match = re.search(regexp_interface, line)
            if match:
                interface_key = match.group('int')
            match = re.search(regexp_prefix, line)
            if match:
                prefix_dict[interface_key] = (match.group('ip'), match.group('mask'))
    return prefix_dict


if __name__ == "__main__":
    print(get_ip_from_cfg("config_r1.txt"))