# -*- coding: utf-8 -*-
'''
Задание 6.2

1. Запросить у пользователя ввод IP-адреса в формате 10.0.1.1
2. Определить тип IP-адреса.
3. В зависимости от типа адреса, вывести на стандартный поток вывода:
   'unicast' - если первый байт в диапазоне 1-223
   'multicast' - если первый байт в диапазоне 224-239
   'local broadcast' - если IP-адрес равен 255.255.255.255
   'unassigned' - если IP-адрес равен 0.0.0.0
   'unused' - во всех остальных случаях


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

ip_add = input("Введите IP-адрес: ")

octet_list = [int(octet) for octet in ip_add.split(".")]

if (octet_list[0] >= 1) and (octet_list[0] <= 223) :
    print(f"\033[93m{'unicast'}")
elif (octet_list[0] >= 224) and (octet_list[0] <= 239) :
    print(f"\033[93m{'multicast'}")
elif (octet_list[0] == 255) \
        and (octet_list[1] == 255) \
        and (octet_list[2] == 255) \
        and (octet_list[3] == 255):
    print(f"\033[93m{'local broadcast'}")
elif (octet_list[0] == 0) \
        and (octet_list[1] == 0) \
        and (octet_list[2] == 0) \
        and (octet_list[3] == 0):
    print(f"\033[93m{'unassigned'}")
else:
    print(f"\033[93m{'unused'}")
