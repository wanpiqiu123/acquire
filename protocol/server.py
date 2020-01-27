import socket  # 导入 socket 模块
from threading import Thread
from Protocol import *

ADDRESS = ('127.0.0.1', 8712)  # 绑定地址
 
g_socket_server = None  # 负责监听的socket
 
g_conn_pool = []  # 连接池

def init():
    """
    初始化服务端
    """
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
    g_socket_server.bind(ADDRESS)
    g_socket_server.listen(5)  # 最大等待数（有很多人理解为最大连接数，其实是错误的）
    print("服务端已启动，等待客户端连接...")
def accept_client():
    """
    接收新连接
    """
    while True:
        client, _ = g_socket_server.accept()  # 阻塞，等待客户端连接
        print("%s号服务器连接成功！" %(len(g_conn_pool)))
        # 加入连接池
        g_conn_pool.append(client)
        client.sendall(get_id(g_conn_pool.index(client)))
        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=message_handle, args=(client,))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()
 
def message_handle(client):
    """
    消息处理
    """
    msg = s_connection()
    client.sendall(msg)
    # client.sendall("连接服务器成功!".encode(encoding='utf8'))
    flag = True
    while flag:
        bytes = client.recv(1024)
        while True:
            length_pck = int.from_bytes(bytes[:4],byteorder="little")
            pck = bytes[4:4 + length_pck]
            bytes = bytes[4 + length_pck:]
            r = pck_handler(pck)
            if r[0] == -1:
                print("客户端%s下线" %(g_conn_pool.index(client)))
                flag = False
                client.close()
                g_conn_pool.remove(client)
                break
            elif r[0]==3:
                player_id = r[1]
                company_id = r[2]
                print("%s choose Company: %s" %(player_id, company_id))
            if r[0] >= 0:
                for c in g_conn_pool:
                    if c != client:
                        c.sendall(Protocol(pck).get_pck_has_head())
            if len(bytes) == 0:
                break
        # print("客户端消息:", bytes.decode(encoding='utf8'))
        # if bytes.decode(encoding='utf8') == '#':
        # # if len(bytes) == 0:
        #     client.close()
        #     # 删除连接
        #     g_conn_pool.remove(client)
        #     print("有一个客户端下线了。")
        #     break
    

if __name__ == '__main__':
    init()
    # 新开一个线程，用于接收新连接
    thread = Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()
    while True:
        i = input("Enter \"exit\" to quit\n")
        if i == "exit":
            break
            exit()
        elif i=='0':
            print(len(g_conn_pool))
    # 主线程逻辑
#     while True:
#         cmd = input("""--------------------------
# 输入1:查看当前在线人数
# 输入2:给指定客户端发送消息
# 输入3:关闭服务端
# """)
#         if cmd == '1':
#             print("--------------------------")
#             print("当前在线人数：", len(g_conn_pool))
#         elif cmd == '2':
#             print("--------------------------")
#             index, msg = input("请输入“索引,消息”的形式：").split(",")
#             g_conn_pool[int(index)].sendall(msg.encode(encoding='utf8'))
#         elif cmd == '3':
#             for c in g_conn_pool:
#                 c.sendall("#".encode(encoding='utf8'))
#             exit()