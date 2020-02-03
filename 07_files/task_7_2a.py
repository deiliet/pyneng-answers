# -*- coding: utf-8 -*-
'''
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт:
  Скрипт не должен выводить команды, в которых содержатся слова,
  которые указаны в списке ignore.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']

#python task_7_2a.py config_sw1.txt

from sys import argv

try:
    with open(argv[1], 'r') as config:
        for line in config:
            if not line.startswith('!'):
                check = True
                for key_word in ignore:
                    if key_word in line:
                        check = False
                if check:
                    print(f"\033[93m{line.rstrip()}")
except IOError:
    print(f"\033[91m{'Такого файле нет'}")
except IndexError:
    print(f"\033[91m{'Файл не указан'}")