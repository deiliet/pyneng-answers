# -*- coding: utf-8 -*-
'''
Задание 7.2c

Переделать скрипт из задания 7.2b:
* передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

Внутри, скрипт должен отфильтровать те строки, в исходном файле конфигурации,
в которых содержатся слова из списка ignore.
И записать остальные строки в итоговый файл.

Проверить работу скрипта на примере файла config_sw1.txt.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

ignore = ['duplex', 'alias', 'Current configuration']

#python task_7_2c.py config_sw1.txt config_sw1_cleared_2

from sys import argv

try:
    with open(argv[1], 'r') as config, open(argv[2], 'w') as edit:
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