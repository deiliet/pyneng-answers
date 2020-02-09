# -*- coding: utf-8 -*-
'''
Задание 17.1

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает как аргумент вывод команды sh version одной строкой (не имя файла)
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

У функции write_inventory_to_csv должно быть два параметра:
 * data_filenames - ожидает как аргумент список имен файлов с выводом sh version
 * csv_filename - ожидает как аргумент имя файла (например, routers_inventory.csv), в который будет записана информация в формате CSV
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает


Функция write_inventory_to_csv должна делать следующее:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в CSV файл

В файле routers_inventory.csv должны быть такие столбцы:
* hostname, ios, image, uptime

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается на sh_vers.
Вы можете раскомментировать строку print(sh_version_files), чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
'''

import re
import csv


def parse_sh_version(file_single_line):
    params_list = []
    regex_dict = {'ios': r'Cisco IOS Software, .+Version (?P<ios>[\d,\S]+),',
                  'image': r'System image file is "(?P<image>[\d,\S]+)"',
                  'uptime': r'router uptime is (?P<uptime>.+)'}
    for key in regex_dict:
        match = re.search(regex_dict[key], file_single_line)
        if match:
            params_list.append(match.group(key))
    return tuple(params_list)


def write_inventory_to_csv(data_filenames, csv_filename):
    headers = ['hostname', 'ios', 'image', 'uptime']
    regex_hostname = r'sh_version_(?P<hostname>[\d,\S]+)\.txt'
    params_list = []
    buffer_list = []
    params_list.append(headers)
    for filename in data_filenames:
        match = re.search(regex_hostname, filename)
        if match:
            buffer_list.append(match.group('hostname'))
        with open(filename) as file:
            for item in parse_sh_version(file.read()):
                buffer_list.append(item)
            params_list.append(buffer_list)
            buffer_list = []
    with open(csv_filename, 'w') as file:
        writer = csv.writer(file)
        for row in params_list:
            writer.writerow(row)
    return None


if __name__ == "__main__":

    import glob

    sh_version_files = glob.glob('sh_vers*')
    write_inventory_to_csv(sh_version_files, 'routers_inventory.csv')

