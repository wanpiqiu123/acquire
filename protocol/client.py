import socket  # 导入 socket 模块
from threading import Thread
from Protocol import *
import queue

q = queue.Queue()
# def message_handle(server):
#     """
#     消息处理
#     """
#     while True:
#         bytes = server.recv(1024)
#         print("服务器消息:", bytes.decode(encoding='utf8'))
#         if bytes.decode(encoding='utf8') == '#':
#             server.close()
#             # 删除连接
#             print("服务器下线了。按下回车结束")
#             q.put("$")
#             break
id = 0 
def message_handle(server):
    """
    消息处理
    """
    # client.sendall("连接服务器成功!".encode(encoding='utf8'))
    while True:
        bytes = server.recv(1024)
        while True:
            length_pck = int.from_bytes(bytes[:4],byteorder="little")
            pck = bytes[4:4 + length_pck]
            bytes = bytes[4 + length_pck:]
            r = pck_handler(pck)
            if r[0]==2:
                global id
                id = r[1]
                print("Client ID is: %s" %(id))
            elif r[0]==3:
                player_id = r[1]
                company_id = r[2]
                print("%s choose Company: %s" %(player_id, company_id))
            if len(bytes) == 0:
                break


s = socket.socket()  # 创建 socket 对象
s.connect(('127.0.0.1', 8712))
thread = Thread(target=message_handle,args=(s,))
thread.setDaemon(True)
thread.start()

while True:
    cmd = input("""--------------------------
输入0:放置块
输入1:并购选项
输入2:关闭客户端
""")
    if cmd == '0':
        brick_idx = input("输入块下标: ")
        s.sendall(put_brick(id,eval(brick_idx)))
    if cmd == '1':
        company_idx = input("输入并购公司下标: ")
        s.sendall(acquire_msg(id,eval(company_idx)))
    elif cmd == '2':
        s.sendall(end_turn())
        s.close()
        exit()
