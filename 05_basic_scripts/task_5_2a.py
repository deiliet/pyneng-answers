# -*- coding: utf-8 -*-
'''
Задание 5.2a

Всё, как в задании 5.2, но, если пользователь ввел адрес хоста, а не адрес сети,
надо преобразовать адрес хоста в адрес сети и вывести адрес сети и маску, как в задании 5.2.

Пример адреса сети (все биты хостовой части равны нулю):
* 10.0.1.0/24
* 190.1.0.0/16

Пример адреса хоста:
* 10.0.1.1/24 - хост из сети 10.0.1.0/24
* 10.0.5.1/30 - хост из сети 10.0.5.0/30

Если пользователь ввел адрес 10.0.1.1/24,
вывод должен быть таким:

Network:
10        0         1         0
00001010  00000000  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000

Проверить работу скрипта на разных комбинациях сеть/маска.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

pref = input('Введите подсеть с маской в формате a.b.c.d/xy: ').split('/')
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