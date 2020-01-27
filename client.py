import socket  # 导入 socket 模块
from threading import Thread
import queue

q = queue.Queue()
def message_handle(server):
    """
    消息处理
    """
    while True:
        bytes = server.recv(1024)
        print("服务器消息:", bytes.decode(encoding='utf8'))
        if bytes.decode(encoding='utf8') == '#':
            server.close()
            # 删除连接
            print("服务器下线了。按下回车结束")
            q.put("$")
            break
 
s = socket.socket()  # 创建 socket 对象
s.connect(('127.0.0.1', 8712))
print(s.recv(1024).decode(encoding='utf8'))
s.send("连接了".encode('utf8'))
thread = Thread(target=message_handle,args=(s,))
thread.setDaemon(True)
thread.start()
while True:
    cmd = input("#结束\n")    
    if not q.empty():
        if q.get()=="$":
            break
            exit()
    s.sendall(cmd.encode(encoding='utf8'))
    if cmd == '#':
        break
        exit()
