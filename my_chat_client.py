"""
    聊天室客户端
"""
import sys
from multiprocessing import Process
from socket import *
# 全局变量
HOST="127.0.0.1"
PORT  = 6918
ADDR = (HOST,PORT)


def recv_msg(sockfd):
    while True:

        data,addr = sockfd.recvfrom(2048)
        print(data.decode())

def send_msg(sockfd, c_name):
    while True:
        try:
            # 对异常处理
            msg = input("发言：")
        except KeyboardInterrupt:
            msg = 'quit'
        if msg == 'quit':
            # 退出消息
            msg = "Q "+c_name
            sockfd.sendto(msg.encode(),ADDR)
            sys.exit("谢谢使用")
        data = "C "+msg+" "+c_name
        sockfd.sendto(data.encode(),ADDR)


def main():
    # 创建套接字
    sockfd = socket(AF_INET, SOCK_DGRAM)
    while True:
        c_name = input("请输入姓名:")
        msg = "L "+c_name
        sockfd.sendto(msg.encode(), ADDR)
        data,addr = sockfd.recvfrom(1024)
        if data == b"YES":
            print("成功进入聊天室.")
            break
        else:
            print(data.decode())

    p = Process(target = recv_msg ,args = (sockfd,)) #创建新进程接收消息
    p.daemon = True  # 父程序退出，子程序也随之退出
    p.start()

    send_msg(sockfd,c_name)# 父进程发送消息



if __name__ == '__main__':
    main()


