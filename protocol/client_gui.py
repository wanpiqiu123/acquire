import pygame.font, pygame.event, pygame.draw, string
from pygame import *
from pygame.locals import *
import socket  # 导入 socket 模块
from threading import Thread
from Protocol import *
def display_box(screen, message,RECT):
    # "Print a message in a box in the middle of the screen"
    fontobject = pygame.font.Font(None,18)
    pygame.draw.rect(screen, (0,0,0),RECT, 0)
    pygame.draw.rect(screen, (255,255,255),RECT, 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255,255,255)),(RECT[0]+2,RECT[1]+RECT[3]/3))
    pygame.display.flip()

def which_btn(mousex,mousey,btn_list):
    for btn in btn_list:
        if pygame.Rect(btn).collidepoint(mousex,mousey):
            # print(btn_list.index(btn))
            return btn_list.index(btn)
    return -1

id = 0 
success = False
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
            if r[0]==-2:
                global success
                success = True
            elif r[0]==2:
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

screen = pygame.display.set_mode((320,240))
name_rect = (30,30,100,30)
ip_rect = (30,70,100,30)
connect_rect = (70,150,80,30)
confirm_rect = (170,150,80,30)
pygame.font.init()
name_string = []
ip_string = []
name = ""
ip = ""
flag = True
btn_list = [name_rect,ip_rect,connect_rect,confirm_rect]
idx=0
connect_string = pygame.font.Font(None,18).render("connect", 1, (255,255,255))
c_rect = connect_string.get_rect()
c_rect.center = pygame.draw.rect(screen,(150,150,150),connect_rect).center
screen.blit(connect_string,c_rect)
confirm_string = pygame.font.Font(None,18).render("confirm", 1, (255,255,255))
c_rect = confirm_string.get_rect()
c_rect.center = pygame.draw.rect(screen,(150,150,150),confirm_rect).center
screen.blit(confirm_string,c_rect)
display_box(screen, "name" + ": " + "".join(name_string),name_rect)
display_box(screen, "ip" + ": " + "".join(ip_string),ip_rect)
while flag:
    if success:
        s_txt = pygame.font.Font(None,18).render("success!", 1, (255,255,255))
        screen.blit(s_txt,(180,100))
        pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            idx = which_btn(mousex,mousey,btn_list)
            if idx==3:
                flag=False
                pygame.display.quit()
                pygame.quit()
                break
            # elif idx==2:
            #     s.connect((ip, 8712))
            #     # s.connect(('127.0.0.1', 8712))
            #     thread = Thread(target=message_handle,args=(s,))
            #     thread.setDaemon(True)
            #     thread.start()
        elif event.type == KEYDOWN and idx==0:
            inkey = event.key
            if inkey == K_BACKSPACE:
                name_string = name_string[0:-1]
            elif inkey == K_MINUS:
                name_string.append("_")
            elif inkey <= 127:
                name_string.append(chr(inkey))
            display_box(screen, "name" + ": " + "".join(name_string),name_rect)
        elif event.type == KEYDOWN and idx==1:
            inkey = event.key
            if inkey == K_BACKSPACE:
                ip_string = ip_string[0:-1]
            elif inkey == K_MINUS:
                ip_string.append("_")
            elif inkey <= 127:
                ip_string.append(chr(inkey))
            display_box(screen, "ip" + ": " + "".join(ip_string),ip_rect)
        name = "".join(name_string)
        ip = "".join(ip_string)
print("name: "+name)
print("ip: "+ip)
while True:
    if input("sth")=="exit":
        break
# while True:
#     cmd = input("""--------------------------
# 输入0:放置块
# 输入1:并购选项
# 输入2:关闭客户端
# """)
#     if cmd == '0':
#         brick_idx = input("输入块下标: ")
#         s.sendall(put_brick(id,eval(brick_idx)))
#     if cmd == '1':
#         company_idx = input("输入并购公司下标: ")
#         s.sendall(acquire_msg(id,eval(company_idx)))
#     elif cmd == '2':
#         s.sendall(end_turn())
#         s.close()
#         exit()