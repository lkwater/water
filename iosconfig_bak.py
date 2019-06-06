#! /usr/bin/env python3

import openpyxl
import netmiko
import time
device_dict={}
file_path = 'workbook/设备.xlsx'
wb = openpyxl.load_workbook(file_path)
wb_sheet = wb.get_sheet_by_name("IT设备")
wb.close()
#print(wb.get_sheet_names())
#print(wb_sheet)
row = 2
while row <= wb_sheet.max_row:
	device_dict[wb_sheet[('a'+str(row))].value]=[wb_sheet[('b'+str(row))].value,
												wb_sheet[('c'+str(row))].value,
												wb_sheet[('d'+str(row))].value,
												wb_sheet[("e"+str(row))].value]
	row += 1
#	print(device_dict)
for device_name,device_list in device_dict.items():
	print("*"*35)
	print("读取设备{},IP地址{}:".format(device_name,device_list[0]),'\n')
	connection = netmiko.Netmiko(ip=device_list[0],username=device_list[1],password=device_list[2],secret=device_list[3],device_type='cisco_ios')
	#进入enable模式
	connection.enable()
	print("-"*35)
	print("设备{}读取完成，正在备份配置。".format(device_name),'\n')
	file_run = connection.send_command('show run')
	#新建文件用来存储配置
	file_config = open("/home/wen/python/IOS/" + device_name + "_" + time.strftime("%Y-%m-%d %H:%M",time.localtime())+".txt",'w')
	#依次把配置文件写入文本文件中
	for each_bak in file_run:
		file_config.write(each_bak)
	print("-"*35)
	print("设备{}配置备份完成。。。。。。。。。".format(device_name),'\n')
	
