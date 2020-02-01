# -*- coding: utf-8 -*-
'''
Задание 5.2b

Преобразовать скрипт из задания 5.2a таким образом,
чтобы сеть/маска не запрашивались у пользователя,
а передавались как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

#python3 ~/pyneng-answers/05_basic_scripts/task_5_2b.py 214.234.252.98/13

from sys import argv

pref = argv[1].split('/')

net = pref[0].split('.')
mask = pref[1]

ip_bin = f"{int(net[0]):08b}{int(net[1]):08b}{int(net[2]):08b}{int(net[3]):08b}"
net_bin = f"{ip_bin[0:int(mask)]}"+f"{0}"*(32-int(mask))
net_list_bin = [net_bin[0:8],net_bin[8:16],net_bin[16:24],net_bin[24:32]]
net_list_dec = [int(net_bin[0:8], 2),int(net_bin[8:16], 2),int(net_bin[16:24], 2),int(net_bin[24:32], 2)]

mask_bin = f"{1}"*int(mask)+f"{0}"*(32-int(mask))
mask_list_bin = [mask_bin[0:8],mask_bin[8:16],mask_bin[16:24],mask_bin[24:32]]
mask_list_dec = [int(mask_bin[0:8], 2),int(mask_bin[8:16], 2),int(mask_bin[16:24], 2),int(mask_bin[24:32], 2)]

# 214.234.252.98/13

table_net = f"""\033[93m
Network: 
{net_list_dec[0]:<10}{net_list_dec[1]:<10}{net_list_dec[2]:<10}{net_list_dec[3]:<10}
{net_list_bin[0]}  {net_list_bin[1]}  {net_list_bin[2]}  {net_list_bin[3]}"""

table_mask = f"""\033[91m
Mask: 
/{mask}
{mask_list_dec[0]:<10}{mask_list_dec[1]:<10}{mask_list_dec[2]:<10}{mask_list_dec[3]:<10}
{mask_list_bin[0]}  {mask_list_bin[1]}  {mask_list_bin[2]}  {mask_list_bin[3]}"""

print(table_net)
print(table_mask)