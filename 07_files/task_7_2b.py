# -*- coding: utf-8 -*-
'''
Задание 7.2b

Дополнить скрипт из задания 7.2a:
* вместо вывода на стандартный поток вывода,
  скрипт должен записать полученные строки в файл config_sw1_cleared.txt

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore.
Строки, которые начинаются на '!' отфильтровывать не нужно.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']

#python task_7_2b.py config_sw1.txt

from sys import argv

try:
    with open(argv[1], 'r') as config, open('config_sw1_cleared.txt', 'w') as edit:
        for line in config:
            check = True
            for key_word in ignore:
                if key_word in line:
                    check = False
            if check:
                edit.write(line)
except IOError:
    print(f"\033[91m{'Такого файле нет'}")
except IndexError:
    print(f"\033[91m{'Файл не указан'}")