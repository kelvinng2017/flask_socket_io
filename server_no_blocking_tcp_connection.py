#/usr/bin/env python
# -*- coding:utf-8 -*-

"""
非阻塞式TCP连接
"""
import sys
import time
import socketserver
import json
import os
import datetime
from datetime import datetime as dt
import show_and_save_log_file

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


SOCKET_IP = ('127.0.0.1', 6666)
BUFFER_SIZE = 4096
SOCKET_TIMEOUT_TIME = 60


class UnblockSocketServer(socketserver.BaseRequestHandler):
    # 繼承socketserver.BaseRequestHandler類
    # 首先執行setup方法，然後執行handle方法，最後執行finish方法
    # 如果handle方法報錯，則會跳過
    # setup與finish無論如何都會執行
    # 一般只定義handle方法即可

    def setup(self):
        print('開啟非阻塞式連接...')

    @staticmethod
    def send_socket_info(handle, msg, side='server', do_encode=True, do_print_info=True):
        """
        發送socket info，並根據side打印不同的前綴信息
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

    @staticmethod
    def receive_socket_info(handle, expected_msg, side='server', do_decode=True, do_print_info=True):
        """
        循環接收socket info，判斷其返回值，直到指定的值出現為止，防止socket信息粘連，並根據side打印不同的前綴信息
        :param handle: socket句柄
        :param expected_msg: 期待接受的內容，如果接受內容不在返回結果中，一直循環等待，期待內容可以為字符串，也可以為多個字符串組成的列表或元組
        :param side: 默認server端
        :param do_decode: 是否需要decode，默認True
        :param do_print_info: 是否需要打印socket信息，默認True
        :return:
        """
        while True:
            if do_decode:
                socket_data = handle.recv(BUFFER_SIZE).decode()
            else:
                socket_data = handle.recv(BUFFER_SIZE)

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
                    if expect in socket_data:  #如果有任意一個存在，跳出循環
                        flag = True
                        break
                if flag:
                    break
            else:
                if expected_msg in socket_data:
                    break
            time.sleep(3)  # 每隔3秒接收一次socket
        return socket_data

    def handle(self):
        """
        所有和client端交互的操作寫在這裡
        :return:
        """
        conn = self.request  # 獲取socket句柄

        # 與client端握手，達成一致
        self.receive_socket_info(handle=conn, expected_msg='client端已就緒')
        self.send_socket_info(handle=conn, msg='server端已就緒')

        # 不斷接收client端發來的消息
        while True:
            socket_data = self.receive_socket_info(handle=conn, expected_msg='')
            if 'quit' in socket_data:
                self.send_socket_info(handle=conn, msg='quit')
                break

            answer = socket_data+"_move"
            self.send_socket_info(handle=conn, msg=answer)

        # 斷開socket連接
        conn.close()

    def finish(self):
        print('連接關閉')


def main():
    # 創建多線程實例
    server = socketserver.ThreadingTCPServer(SOCKET_IP, UnblockSocketServer)
    # 開啟異步多線程，等待連接
    server.timeout = SOCKET_TIMEOUT_TIME  # 設置server端超時時間
    print(f'server端 {SOCKET_IP[0]}:{SOCKET_IP[1]} 開啟')
    server.serve_forever()  # 永久運行


if __name__ == '__main__':
    main()
