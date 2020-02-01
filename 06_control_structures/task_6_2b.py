# -*- coding: utf-8 -*-
'''
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт:
Если адрес был введен неправильно, запросить адрес снова.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

octet_list = []

while True:
    try:
        correct = True
        ip_add = input("Введите IP-адрес: ")
        octet_list = [int(octet) for octet in ip_add.split(".")]
    except ValueError:
        print(f"\033[91m{'Неправильный IP-адрес'}")
    else:
        for octet in octet_list:
            if octet not in range(0, 255):
                correct = False
        if len(octet_list) == 4 and correct:
            break
        else:
            print(f"\033[91m{'Неправильный IP-адрес'}")
if (octet_list[0] >= 1) and (octet_list[0] <= 223):
    print(f"\033[93m{'unicast'}")
elif (octet_list[0] >= 224) and (octet_list[0] <= 239):
    print(f"\033[93m{'multicast'}")
elif (octet_list[0] == 255) and (octet_list[1] == 255) and (octet_list[2] == 255) and (
        octet_list[3] == 255):
    print(f"\033[93m{'local broadcast'}")
elif (octet_list[0] == 0) and (octet_list[1] == 0) and (octet_list[2] == 0) and (octet_list[3] == 0):
    print(f"\033[93m{'unassigned'}")
else:
    print(f"\033[93m{'unused'}")





