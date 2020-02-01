# -*- coding: utf-8 -*-
'''
Задание 5.2

Запросить у пользователя ввод IP-сети в формате: 10.1.1.0/24

Затем вывести информацию о сети и маске в таком формате:

Network:
10        1         1         0
00001010  00000001  00000001  00000000

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

mask_bin = f"{1}"*int(mask)+f"{0}"*(32-int(mask))
list_bin = [mask_bin[0:8],mask_bin[8:16],mask_bin[16:24],mask_bin[24:32]]
list_dec = [int(mask_bin[0:8], 2),int(mask_bin[8:16], 2),int(mask_bin[16:24], 2),int(mask_bin[24:32], 2)]

table_net = f"""\033[93m
Network: 
{net[0]:10}{net[1]:10}{net[2]:10}{net[3]:10}
{int(net[0]):08b}  {int(net[1]):08b}  {int(net[2]):08b}  {int(net[3]):08b}"""

table_mask = f"""\033[91m
Mask: 
/{mask}
{list_dec[0]:<10}{list_dec[1]:<10}{list_dec[2]:<10}{list_dec[3]:<10}
{list_bin[0]}  {list_bin[1]}  {list_bin[2]}  {list_bin[3]}"""

print(table_net)
print(table_mask)

# 214.234.252.98/8