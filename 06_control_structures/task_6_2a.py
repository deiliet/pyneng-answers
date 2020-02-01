# -*- coding: utf-8 -*-
'''
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса. Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой,
   - каждое число в диапазоне от 0 до 255.

Если адрес задан неправильно, выводить сообщение:
'Неправильный IP-адрес'

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ip_add = input("Введите IP-адрес: ")

correct = False
octet_list = []

try :
    octet_list = [int(octet) for octet in ip_add.split(".")]
except ValueError:
    print(f"\033[91m{'Неправильный IP-адрес'}")
else:
    for octet in octet_list:
        if octet in range(0, 255):
            correct = True
    if len(octet_list) == 4 and correct:
        if (octet_list[0] >= 1) and (octet_list[0] <= 223):
            print(f"\033[93m{'unicast'}")
        elif (octet_list[0] >= 224) and (octet_list[0] <= 239):
            print(f"\033[93m{'multicast'}")
        elif (octet_list[0] == 255) and (octet_list[1] == 255) and (octet_list[2] == 255) and (octet_list[3] == 255):
            print(f"\033[93m{'local broadcast'}")
        elif (octet_list[0] == 0) and (octet_list[1] == 0) and (octet_list[2] == 0) and (octet_list[3] == 0):
            print(f"\033[93m{'unassigned'}")
        else:
            print(f"\033[93m{'unused'}")
    else:
        print(f"\033[91m{'Неправильный IP-адрес'}")









