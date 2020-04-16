"""
    聊天室服务端
"""
from multiprocessing import Process
from socket import *

# 全局变量
from threading import Thread

HOST = "127.0.0.1"
PORT = 6918
ADDR = (HOST, PORT)
# 存储用户信息（{name:addr}）
users = {}


# 进入聊天室
def do_inchat(sockfd, name, addr):
    if name in users or "管理" in name:
        msg = "该用户已存在"
        sockfd.sendto(msg.encode(), addr)
    else:

        sockfd.sendto(b"YES", addr)
        for i in users:
            msg = "\n欢迎 %s进入聊天室" % name
            sockfd.sendto(msg.encode(), users[i])
        users[name] = addr


# 聊天功能
def do_chat(sockfd, msg, name):
    data = name + ":" + msg
    for i in users:
        if i != name:
            sockfd.sendto(data.encode(), users[i])


# 退出聊天室
def quit_chat(sockfd, data):
    msg = "%s退出聊天室" % users[data[1]]
    del users[data[1]]
    for i in users:
        sockfd.sendto(msg.encode(), users[i])

#  处理接收到的信息
def requse(sockfd):
    while True:
        data, addr = sockfd.recvfrom(2048)
        data = data.decode().split(" ")
        if data[0] == "L":
            # 处理进入聊天室。（data --> [L,msg],addr-->name）
            do_inchat(sockfd, data[1], addr)
        elif data[0] == "C":
            # 处理聊天
            data_warning(sockfd, data[1], data[2])
        elif data[0] == "Q" or not data:
            quit_chat(sockfd, data)

# 敏感词汇检测
def data_warning(sockfd, msg, name):
    list_min = ["xx", "aa", "bb", "oo"]
    for i in list_min:
        if i in msg:
            # warning_number = dict_warning_log(name)
            data ="C "+"%s:涉嫌发布敏感词汇，提出警告，三次警告剔除群聊"%name+" 管理员"
            sockfd.sendto(data.encode(), ADDR)
        else:
            do_chat(sockfd, msg, name)
            break


# 警告记录
def dict_warning_log(c_name):
    dict_warning = {}
    for i in dict_warning:
        if i in dict_warning:
            dict_warning[i] += 1
            if dict_warning[i] == 3:
                del users[c_name]
        else:
            dict_warning[i] = 1
    # return dict_warning[c_name]

# 管理员发送消息
def manger_send(sockfd):
    while True:
        msg = input("发言：")
        data = "C " + msg + " 管理员"
        sockfd.sendto(data.encode(), ADDR)


def main():
    # 创建套接字
    sockfd = socket(AF_INET, SOCK_DGRAM)
    sockfd.bind(ADDR)
    # 创建进程，满足多个客户端同时请求
    p = Process(target=requse, args=(sockfd,))
    p.deamon = True
    p.start()
    manger_send(sockfd)


if __name__ == '__main__':
    main()
