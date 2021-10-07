#/usr/bin/env python
# -*- coding:utf-8 -*-

"""
阻塞式TCP连接
"""
import time
import socket

__author__ = 'Evan'


SOCKET_IP = ('127.0.0.1', 6666)
BUFFER_SIZE = 1024
SOCKET_TIMEOUT_TIME = 60


def send_socket_info(handle, msg, side='server', do_encode=True, do_print_info=True):
    """
    發送socket info，並根據side打印不同的前綴信息
    :param handle: socket句柄
    :param msg: 要發送的內容
    :param side: 默認server端
    :param do_encode: 是否需要encode，默認True
    :param do_print_info:是否需要打印socket信息，默認True
    :return:
    """
    if do_encode:
        handle.send(msg.encode())
    else:
        handle.send(msg)

    if do_print_info:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        if side == 'server':
            print(f'Server send --> {current_time} - {msg}')
        else:
            print(f'Client send --> {current_time} - {msg}')


def receive_socket_info(handle, expected_msg, side='server', do_decode=True, do_print_info=True):
    """
    循環接收socket info，判斷其返回值，直到指定的值出現為止，防止socket信息粘連，並根據side打印不同的前綴信息
    :param handle: socket句柄
    :param expected_msg: 期待接受的內容，如果接受內容不在返回結果中，一直循環等待，期待內容可以為字符串，也可以為多個字符串組成的列表或元組
    :param side: 默認server端
    :param do_decode:是否需要decode，默認True
    :param do_print_info: 是否需要打印socket信息，默認True
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


def start_server_socket():
    """
    啟動server端TCP Socket
    :return:
    """
    ip, port = SOCKET_IP
    server = socket.socket()  # 使用TCP方式傳輸
    server.bind((ip, port))  # 綁定IP與端口
    server.listen(5)  # 設置最大連接數為5
    print(f'server端 {ip}:{port} 開啟')

    # 不斷循環，接受client端請求
    while True:
        print('等待client端連接...')
        conn, address = server.accept()  # 使用accept阻塞式等待client端請求，如果多個client端同時訪問，排隊一個一個進
        print(f'當前連接client端：{address}')
        conn.settimeout(SOCKET_TIMEOUT_TIME)  #設置server端超時時間

        # 與client端握手，達成一致
        receive_socket_info(handle=conn, expected_msg='client端已就緒')
        send_socket_info(handle=conn, msg='server端已就緒')

        # 不斷接收client端發來的消息
        while True:
            socket_data = receive_socket_info(handle=conn, expected_msg='')
            if 'quit' in socket_data:
                send_socket_info(handle=conn, msg='quit')
                break

            answer = input('請回复client端的信息：')
            send_socket_info(handle=conn, msg=answer)

        # 斷開socket連接
        conn.close()
        print(f'與client端 {ip}:{port} 斷開連接')


if __name__ == '__main__':
    start_server_socket()  # 启动server端socket
