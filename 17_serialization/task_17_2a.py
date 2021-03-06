# -*- coding: utf-8 -*-
'''
Задание 17.2a

Создать функцию generate_topology_from_cdp, которая обрабатывает вывод команды show cdp neighbor из нескольких файлов и записывает итоговую топологию в один словарь.

Функция generate_topology_from_cdp должна быть создана с параметрами:
* list_of_files - список файлов из которых надо считать вывод команды sh cdp neighbor
* save_to_filename - имя файла в формате YAML, в который сохранится топология.
 * значение по умолчанию - None. По умолчанию, топология не сохраняется в файл
 * топология сохраняется только, если save_to_filename как аргумент указано имя файла

Функция должна возвращать словарь, который описывает соединения между устройствами, независимо от того сохраняется ли топология в файл.

Структура словаря должна быть такой:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}},
 'R5': {'Fa 0/1': {'R4': 'Fa 0/1'}},
 'R6': {'Fa 0/0': {'R4': 'Fa 0/2'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.

Проверить работу функции generate_topology_from_cdp на списке файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt
* sh_cdp_n_r4.txt
* sh_cdp_n_r5.txt
* sh_cdp_n_r6.txt

Проверить работу параметра save_to_filename и записать итоговый словарь в файл topology.yaml.

'''


import os
import re
import yaml
import sys
from task_17_2 import parse_sh_cdp_neighbors


def generate_topology_from_cdp(list_of_files, save_to_filename=None):
    topology_dict = {}
    for filename in list_of_files:
        with open(filename) as file:
            topology_dict.update(parse_sh_cdp_neighbors(file.read()))
    if save_to_filename is None:
        pass
    else:
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        regexp_yaml = r'\S+(\.yaml)'
        if save_to_filename in files:
            print('File is already existed')
            while True:
                decision = input('Continue? (yes/no): ')
                if decision == 'yes':
                    break
                if decision == 'no':
                    sys.exit('Change filename')
                    # raise ValueError('Change filename')
        if not re.match(regexp_yaml, save_to_filename):
            print('File is not yaml or whitespaces are existed')
            sys.exit('Change filename')
            # raise ValueError('Change filename')
        with open(save_to_filename, 'w') as file:
            yaml.dump(topology_dict, file)
    return topology_dict


if __name__ == "__main__":

    import glob

    file_list = sorted(glob.glob('sh_cdp_n*'))
    generate_topology_from_cdp(file_list, 'topology.yaml')
