#/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import socket

import math
import json
import os
import datetime
import show_and_save_log_file
import sys
from datetime import datetime as dt
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

__author__ = 'Evan'


REMOTE_IP = ('192.168.0.77', 6666)
BUFFER_SIZE = 5000
SOCKET_TIMEOUT_TIME = 120


def send_socket_info(handle, msg, side='server', do_encode=True, do_print_info=True):
    """
    發送socket信息，並根據側面打印不同的提示信息
    :param handle: socket句柄
    :param msg: 要發送的內容
    :param side: 默認server端
    :param do_encode: 是否需要encode，默認True
    :param do_print_info: 是否需要打印socket信息，默認True
    :return:
    """
    if do_encode:
        handle.send(msg.encode())
    else:
        handle.send(msg)

    if do_print_info:
        current_time = dt.today().strftime('%Y-%m-%d %H:%M:%S.%f')
        if side == 'server':
            kelvin_debug_log.logger.debug(f'Server send --> {current_time} - \n{msg} -size:{sys.getsizeof(msg)}')
            #print(f'Server send --> {current_time} - {msg}')
        else:
            kelvin_debug_log.logger.debug(f'Client send --> {current_time} - \n{msg} -size:{sys.getsizeof(msg)}')
            #print(f'Client send --> {current_time} - {msg}')


def receive_socket_info(handle, expected_msg, side='server', do_decode=True, do_print_info=True):
    """
    循環接收socket info，判斷其返回值，直到指定的值出現為止，防止socket信息粘連，並根據side打印不同的前綴信息
    :param handle: socket句柄
    :param expected_msg: 期待接受的內容，如果接受內容不在返回結果中，一直循環等待，期待內容可以為字符串，也可以為多個字符串組成的列表或元組
    :param side: 默認server端
    :param do_decode: 是否需要decode，默认True
    :param do_print_info: 是否需要decode，默認True
    :return:
    """
    while True:
        if do_decode:
            socket_data = handle.recv(BUFFER_SIZE,socket.MSG_WAITALL).decode()
        else:
            socket_data = handle.recv(BUFFER_SIZE,socket.MSG_WAITALL)

        if do_print_info:
            current_time = dt.today().strftime('%Y-%m-%d %H:%M:%S.%f')
            if side == 'server':
                kelvin_debug_log.logger.debug(f'Server received ==> {current_time} - \n{socket_data} -size:{sys.getsizeof(socket_data)}')
                #print(f'Server received ==> {current_time} - {socket_data}')
            else:
                kelvin_debug_log.logger.debug(f'Client received ==> {current_time} - \n{socket_data} -size:{sys.getsizeof(socket_data)}')
                #print(f'Client received ==> {current_time} - {socket_data}')

        # 如果expected_msg為空，跳出循環
        if not expected_msg:
            break

        if isinstance(expected_msg, (list, tuple)):
            flag = False
            for expect in expected_msg:  # 循環判斷每個期待字符是否在返回結果中
                if expect in socket_data:  # 如果有任意一個存在，跳出循環
                    flag = True
                    break
            if flag:
                break
        else:
            if expected_msg in socket_data:
                break
        time.sleep(3)  # 每隔3秒接收一次socket
    return socket_data


def start_client_socket():
    """
    啟動client端TCP Socket
    :return:
    """
    ip, port = REMOTE_IP
    client = socket.socket()  # 使用TCP方式傳輸
    print(f'開始連接server {ip}:{port} ...')
    client.connect((ip, port))  # 連接遠程server端
    print(f'連接server端 {ip}:{port} 成功')
    client.settimeout(SOCKET_TIMEOUT_TIME)  # 設置客戶端超時時間
    print("hello1")
    # 與server端握手，達成一致
    send_socket_info(handle=client, side='client', msg='client端已就緒')
    receive_socket_info(handle=client, side='client', expected_msg='server端已就緒')
    
    # 與server端交互
    i=0
    ans= ""
    while True:
        #print("hello")
        if i<=100:
            answer = "abcdefghijklmnopgrstuvwxyz_car_"+str(i)+"\n"
        else:
            answer = "quit"
        i =i+1
        ans  = ans +answer
        send_socket_info(handle=client, side='client', msg=ans)

        socket_data = receive_socket_info(handle=client, side='client', expected_msg='')
        if 'quit' in socket_data:
            send_socket_info(handle=client, side='client', msg='quit')
            break

    # 斷開socket連接
    client.close()
    print(f'與server端 {ip}:{port} 斷開連接')


if __name__ == '__main__':
    start_client_socket()  # 啟動客戶端socket
