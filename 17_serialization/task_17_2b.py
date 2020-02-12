# -*- coding: utf-8 -*-
'''
Задание 17.2b

Создать функцию transform_topology, которая преобразует топологию в формат подходящий для функции draw_topology.

Функция ожидает как аргумент имя файла в формате YAML, в котором хранится топология.

Функция должна считать данные из YAML файла, преобразовать их соответственно, чтобы функция возвращала словарь такого вида:
    {('R4', 'Fa 0/1'): ('R5', 'Fa 0/1'),
     ('R4', 'Fa 0/2'): ('R6', 'Fa 0/0')}

Функция transform_topology должна не только менять формат представления топологии, но и удалять дублирующиеся соединения (их лучше всего видно на схеме, которую генерирует draw_topology).

Проверить работу функции на файле topology.yaml. На основании полученного словаря надо сгенерировать изображение топологии с помощью функции draw_topology.
Не копировать код функции draw_topology.

Результат должен выглядеть так же, как схема в файле task_17_2b_topology.svg

При этом:
* Интерфейсы должны быть записаны с пробелом Fa 0/0
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме
* На схеме не должно быть дублирующихся линков


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

'''

import pprint
import yaml
from pprint import pprint


def transform_topology(yaml_filename):
    buffer_dict = {}
    cdp_dict = {}
    with open(yaml_filename) as file:
        yaml_file = yaml.safe_load(file)
        for local_device in yaml_file:
            for local_port in yaml_file[local_device]:
                for remote_device in yaml_file[local_device][local_port]:
                    remote_port = yaml_file[local_device][local_port][remote_device]
                    buffer_dict[(local_device, local_port)] = (remote_device, remote_port)
    for key, value in buffer_dict.items():
        if value not in cdp_dict.keys() or cdp_dict[value] != key:
            cdp_dict.update({key: value})
    return cdp_dict

pprint(transform_topology('topology.yaml'))
