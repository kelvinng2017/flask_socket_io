#/usr/bin/env python
# -*- coding: UTF-8 -*-
from python_shutil_rmtree import delete_log_file
import math
import json
import os
import datetime
import show_and_save_log_file
import socket
#delete_log_file()
f =open('./config.json','r')
data = json.load(f)
f.close()
log_file_path = data.get('log_file_path')
timeNow = datetime.datetime.now()
file_name_time = timeNow.strftime("%Y-%m-%d_%Hh%Mm%Ss")
if not os.path.exists(os.path.join(os.getcwd()+log_file_path)):
    print("creeate log file folder")
    os.makedirs(os.path.join(os.getcwd()+"/log/kelvinng_log_file/"))
file_name_path = os.getcwd()+log_file_path
kelvin_debug_log = show_and_save_log_file.Logger(file_name_path+""+os.path.basename(__file__)+"_"+file_name_time +
                                    ".log", level='debug')
kelvin_debug_log.logger.debug("hello")

# https://blog.csdn.net/weixin_43750377/article/details/111590893


def receive_socket_info(handle, expected_msg, side='server', do_decode=True, do_print_info=True):
    """
    循环接收socket info，判断其返回值，直到指定的值出现为止，防止socket信息粘连，并根据side打印不同的前缀信息
    :param handle: socket句柄
    :param expected_msg: 期待接受的内容，如果接受内容不在返回结果中，一直循环等待，期待内容可以为字符串，也可以为多个字符串组成的列表或元组
    :param side: 默认server端
    :param do_decode: 是否需要decode，默认True
    :param do_print_info: 是否需要打印socket信息，默认True
    :return:
    """
    while True:
        if do_decode:
            socket_data = handle.recv(BUFFER_SIZE).decode()
        else:
            socket_data = handle.recv(BUFFER_SIZE)

        if do_print_info:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            if side == 'server':
                print(f'Server received ==> {current_time} - {socket_data}')
            else:
                print(f'Client received ==> {current_time} - {socket_data}')

        # 如果expected_msg为空，跳出循环
        if not expected_msg:
            break

        if isinstance(expected_msg, (list, tuple)):
            flag = False
            for expect in expected_msg:  # 循环判断每个期待字符是否在返回结果中
                if expect in socket_data:  # 如果有任意一个存在，跳出循环
                    flag = True
                    break
            if flag:
                break
        else:
            if expected_msg in socket_data:
                break
        time.sleep(3)  # 每隔3秒接收一次socket
    return socket_data

