import socket  # 导入 socket 模块
import random
from threading import Thread
from protocol import *

ADDRESS = ('127.0.0.1', 8712)  # 绑定地址
# ADDRESS = ('127.0.0.1', 8712)  # 绑定地址
 
g_socket_server = None  # 负责监听的socket
 
g_conn_pool = []  # 连接池
player_num = 6
name_list = []
sequence = []
start_flag = False

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
        # client.sendall(get_id(g_conn_pool.index(client)))
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
    player_name = ""
    global start_flag
    while flag:
        if not start_flag and len(name_list)==player_num:
            name_msg = send_name_list(name_list,sequence)
            start_flag = True
            # brick_list = random.sample(range(108),player_num*6)
            brick_list = list(range(12))
            for c in g_conn_pool:
                c.sendall(name_msg)
                c.sendall(original_handbrick(brick_list))
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
            elif r[0]==1:
                player_id = r[1]
                brick_idx = r[2]
                print("抽取地块%s" %(brick_idx))
            elif r[0]==3:
                player_id = r[1]
                company_id = r[2]
                print("%s choose Company: %s" %(player_id, company_id))
            elif r[0]==4:
                player_id = r[1]
                player_name = r[2]
                name_list.append(player_name)
                print("%s choose name: %s" %(player_id, player_name))
            if r[0] in [0,1,3,7,8,9,10]:
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
    player_num = int(input("Player num: "))
    sequence = list(range(player_num))
    random.shuffle(sequence)
    while True:
        i = input("Enter \"exit\" to quit\n")
        if i == "exit":
            break
            exit()
        elif i=='0':
            print(len(g_conn_pool))
