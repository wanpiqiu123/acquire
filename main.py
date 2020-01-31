import sys
from pygame.locals import *
# from my_color import *
from gui import *
import variables
from game import *
from protocol import *
import socket  
from threading import Thread

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
                variables.success_connection = True
                s.sendall(send_name(variables.MY_ID,variables.name))
                # print(variables.MY_ID,variables.name)
            elif r[0]==0: #place brick
                player_id = r[1]
                brick_idx = r[2]
                assert player_id==variables.TURN, "ID INCONSISTANT!"
                print("放置%s" %(brick_idx))
                others_place_brick(brick_idx)
            elif r[0]==1: #new brick
                player_id = r[1]
                brick_idx = r[2]
                assert player_id==variables.TURN, "ID INCONSISTANT!"
                ohters_new_brick(brick_idx)
                print("%s抽取地块%s" %(variables.PLAYER_NAME[variables.TURN],brick_idx))
            elif r[0]==2: #id
                variables.MY_ID = r[1]
                print("Client ID is: %s" %(variables.MY_ID))
            elif r[0]==3: #acquire
                brick_idx = r[1]
                company_id = r[2]
                print("choose Company: %s" %(company_id))
                acquire(brick_idx,company_id)
            elif r[0]==5: #name & sequence
                variables.NUM_PLAYER=r[1]
                variables.PLAYER_NAME=r[2]
                variables.MY_ID = variables.PLAYER_NAME.index(variables.name)
                print(variables.MY_ID,variables.name)
                if variables.MY_ID == variables.TURN:
                    variables.my_turn = True
                variables.all_is_ready = True
            elif r[0]==6: #original brick
                total_brick = r[1]
                for brick in total_brick:
                    print(brick)
                    variables.REMAINING_BLOCK.remove(brick)
                variables.REMAINING_BLOCK_NUM-=len(total_brick)
                my_brick= total_brick[variables.MY_ID*6:(variables.MY_ID+1)*6]
                variables.HAND_BRICK = [idx2coord(b) for b in my_brick]
            elif r[0]==7: #buy stock
                buy_stock_list = r[1]
                print("buy_stock_list",buy_stock_list)
                if buy_stock_list==[0,]*7:
                    variables.MY_LOG+="%s没有购买股票\n" %(variables.PLAYER_NAME[variables.TURN])
                else:
                    others_buy_stock(buy_stock_list)
            elif r[0]==8: #end_turn
                player_id = r[1]
                assert player_id==variables.TURN, "ID INCONSISTANT!"
                variables.TURN=(variables.TURN+1)%variables.NUM_PLAYER
                variables.MY_LOG+="\n轮到%s执行\n" %(variables.PLAYER_NAME[variables.TURN])
                if variables.TURN==variables.MY_ID:
                    variables.my_turn = True 
                check_final()
            elif r[0]==9: #establish
                company_id = r[1]
                print("choose company %s" %(COMPANY_NAME[company_id]))
                establish(brick_idx,company_id)
                update_stock_price()
                major_minor()
            elif r[0]==10: #deal stock
                turn_id,sell,change,small,large = r[1:6]
                print("sell:%s change:%s large:%s" %(sell,change,large))
                variables.MONEY[turn_id]+=variables.COMPANY_PRICE[small]*sell
                variables.STOCK_AT_HAND[turn_id][small]-=(sell+change*2)
                variables.STOCK_AT_HAND[turn_id][large]+=change
                variables.COMPANY_STOCK_NUM[small]+=(sell+change*2)
                variables.COMPANY_STOCK_NUM[large]-=change
                if (turn_id+1)%variables.NUM_PLAYER==variables.TURN:
                    update_stock_price()
                elif (turn_id+1)%variables.NUM_PLAYER==variables.MY_ID:
                    variables.deal_stock_flag = True
                    variables.LARGE_COMPANY = large
                    variables.SMALL_COMPANY = small
            if len(bytes) == 0:
                break

s = socket.socket() 

screen = pygame.display.set_mode((320,240))
pygame.display.set_caption('Client')
connect_string = pygame.font.Font(None,18).render("connect", 1, (255,255,255))
c_rect = connect_string.get_rect()
c_rect.center = pygame.draw.rect(screen,(150,150,150),CONNECT_RECT).center
screen.blit(connect_string,c_rect)
confirm_string = pygame.font.Font(None,18).render("confirm", 1, (255,255,255))
c_rect = confirm_string.get_rect()
c_rect.center = pygame.draw.rect(screen,(150,150,150),CONFIRM_RECT).center
screen.blit(confirm_string,c_rect)
display_box(screen, "name" + ": " + "".join(variables.name_string),NAME_RECT)
display_box(screen, "ip" + ": " + "".join(variables.ip_string),IP_RECT)
flag = True
c_idx = 0
while flag:
    if variables.success_connection:
        s_txt = C_FONT_20.render("success!", 1, (255,255,255))
        screen.blit(s_txt,(170,30))
        pygame.display.flip()
    if variables.all_is_ready:
        ready_txt = C_FONT_20.render("READY!", 1, (255,255,255))
        screen.blit(ready_txt,(180,70))
        pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            c_idx = which_btn(mousex,mousey,CLIENT_LIST)
            if c_idx==3 and variables.all_is_ready: #confirm
                flag=False
                break
            elif c_idx==2 and not variables.success_connection: #connect
                s.connect((variables.ip, 8712))
                # s.connect(('127.0.0.1', 8712))
                thread = Thread(target=message_handle,args=(s,))
                thread.setDaemon(True)
                thread.start()
                
                # variables.success_connection = True
        elif event.type == KEYDOWN and c_idx==0:
            inkey = event.key
            if inkey == K_BACKSPACE:
                variables.name_string = variables.name_string[0:-1]
            elif inkey == K_MINUS:
                variables.name_string.append("_")
            elif inkey <= 127:
                variables.name_string.append(chr(inkey))
            display_box(screen, "name" + ": " + "".join(variables.name_string),NAME_RECT)
        elif event.type == KEYDOWN and c_idx==1:
            inkey = event.key
            if inkey == K_BACKSPACE:
                variables.ip_string = variables.ip_string[0:-1]
            elif inkey == K_MINUS:
                variables.ip_string.append("_")
            elif inkey <= 127:
                variables.ip_string.append(chr(inkey))
            display_box(screen, "ip" + ": " + "".join(variables.ip_string),IP_RECT)
        variables.name = "".join(variables.name_string)
        variables.ip = "".join(variables.ip_string)

def main():
    FPS = 60
    clock = pygame.time.Clock()
    pygame.display.set_caption('Acquire')
    
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.fill(BGCOLOR)
    stock_pic = pygame.image.load("stock_pic.png").convert()
    stock_pic = pygame.transform.smoothscale(stock_pic, (350, 340))
    if len(variables.HAND_BRICK) == 0:
        # variables.HAND_BRICK = random_hand_brick()
        variables.HAND_BRICK = [idx2coord(i) for i in list(range(6))]
    # print(variables.HAND_BRICK)
    # place_brick(0)
    variables.MONEY = [6000,]*variables.NUM_PLAYER
    variables.STOCK_AT_HAND = [[2,]*7 for i in range(variables.NUM_PLAYER)]
    variables.MAJOR_MINOR = [[0,]*7 for i in range(variables.NUM_PLAYER)]
    variables.TOTAL_PROPERTY = [0,]*variables.NUM_PLAYER
    variables.FINAL_RANKING = [0,]*variables.NUM_PLAYER
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        draw_frame(DISPLAYSURF)
        draw_end(DISPLAYSURF)
        draw_rule(DISPLAYSURF)
        draw_note(DISPLAYSURF)
        draw_bricks(DISPLAYSURF)
        draw_stock(DISPLAYSURF,stock_pic)
        draw_state(DISPLAYSURF)
        draw_hand_brick(DISPLAYSURF,variables.HAND_BRICK)
        draw_c_name(DISPLAYSURF,variables.TURN)
        draw_buy_menu(DISPLAYSURF)
        draw_rest_block(DISPLAYSURF)
        draw_log(DISPLAYSURF)

        if variables.win_flag:
            calculate_property()
            draw_win_screen(DISPLAYSURF)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                s.sendall(send_exit())
                s.close()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                if variables.establish_flag:
                    idx = which_btn(mousex,mousey,C_BUTTON_LIST)
                    if 0<=idx<7:
                        establish(variables.brick_idx,idx)
                        s.sendall(send_establish(idx))
                        variables.establish_flag=False
                        update_stock_price()
                        major_minor()
                elif variables.acquire_flag:
                    idx = which_btn(mousex,mousey,C_BUTTON_LIST)
                    if variables.AC_LIST[idx]==1:
                        variables.AC_LIST[idx]=2
                        variables.SMALL_COMPANY = variables.AC_LIST.index(1)
                        variables.LARGE_COMPANY = idx
                        acquire(variables.brick_idx,idx)
                        s.sendall(acquire_msg(variables.brick_idx,idx))
                        variables.deal_stock_flag = True
                        variables.acquire_flag=False
                elif variables.buy_stock_flag:
                    idx = which_btn(mousex,mousey,S_BUTTON_LIST)
                    if 0<=idx<7 and variables.COMPANY_STOCK_NUM[idx]!=0 and variables.MONEY[variables.TURN]-buy_cost(variables.BUY_STOCK_LIST)>=variables.COMPANY_PRICE[idx] and sum(variables.BUY_STOCK_LIST)<(3-variables.BUY_STOCK_NUM) and variables.LIVE_COMPANY[idx]:
                        variables.BUY_STOCK_LIST[idx]+=1
                    elif idx==7: #confirm
                        variables.MONEY[variables.TURN] = variables.MONEY[variables.TURN]-buy_cost(variables.BUY_STOCK_LIST)
                        variables.BUY_STOCK_NUM+=sum(variables.BUY_STOCK_LIST)
                        if variables.BUY_STOCK_NUM==0 and sum(variables.BUY_STOCK_LIST)==0:
                            variables.MY_LOG+="%s没有购买股票\n" %(variables.PLAYER_NAME[variables.TURN])
                        else:
                            s.sendall(buy_stock_msg(variables.BUY_STOCK_LIST))
                            variables.MY_LOG+="%s购买了" %(variables.PLAYER_NAME[variables.TURN])
                        for i in range(len(variables.BUY_STOCK_LIST)):
                            variables.STOCK_AT_HAND[variables.TURN][i]+=variables.BUY_STOCK_LIST[i]
                            variables.COMPANY_STOCK_NUM[i]-=variables.BUY_STOCK_LIST[i]
                            if variables.BUY_STOCK_LIST[i]!=0:
                                variables.MY_LOG+="%s股%s, " %(variables.BUY_STOCK_LIST[i],COMPANY_NAME[i])
                            variables.BUY_STOCK_LIST[i]=0
                        variables.MY_LOG+="\n"
                        variables.buy_stock_flag=False
                        major_minor()
                    elif idx ==8: #cancel
                        variables.buy_stock_flag=False
                        variables.BUY_STOCK_LIST=[0,]*7

                elif variables.deal_stock_flag:
                    idx = which_btn(mousex,mousey,D_BUTTON_LIST)
                    if idx==0 and variables.STOCK_AT_HAND[variables.MY_ID][variables.SMALL_COMPANY]-variables.TMP_DECREASE>0:
                        variables.TMP_SELL+=1
                        variables.TMP_DECREASE+=1
                    elif idx==1 and variables.STOCK_AT_HAND[variables.MY_ID][variables.SMALL_COMPANY]-variables.TMP_DECREASE>1:
                        variables.TMP_CHANGE+=1
                        variables.TMP_DECREASE+=2
                    elif idx==2:
                        s.sendall(deal_stock_msg(variables.MY_ID,variables.TMP_SELL,variables.TMP_CHANGE,variables.SMALL_COMPANY,variables.LARGE_COMPANY))
                        variables.MONEY[variables.MY_ID]+=variables.COMPANY_PRICE[variables.SMALL_COMPANY]*variables.TMP_SELL
                        variables.STOCK_AT_HAND[variables.MY_ID][variables.SMALL_COMPANY]-=variables.TMP_DECREASE
                        variables.STOCK_AT_HAND[variables.MY_ID][variables.LARGE_COMPANY]+=variables.TMP_CHANGE
                        variables.COMPANY_STOCK_NUM[variables.SMALL_COMPANY]+=variables.TMP_DECREASE
                        variables.COMPANY_STOCK_NUM[variables.LARGE_COMPANY]-=variables.TMP_CHANGE
                        variables.TMP_SELL=variables.TMP_CHANGE=variables.TMP_DECREASE=0
                        variables.deal_stock_flag=False
                        # update_stock_price()
                        major_minor()
                    elif idx==3:
                        variables.TMP_SELL=variables.TMP_CHANGE=variables.TMP_DECREASE=0


                elif variables.my_turn:
                    idx = which_btn(mousex,mousey,BUTTON_LIST)
                    if idx!=-1 and idx<6 and not variables.has_put_flag:
                        variables.brick_idx = place_brick(idx)
                        variables.place_flag=True
                        variables.has_put_flag=True
                        s.sendall(send_place_brick(variables.MY_ID,variables.brick_idx))
                    elif idx==6 and variables.has_put_flag:
                        if variables.BUY_STOCK_NUM==0 :
                            variables.MY_LOG+="%s没有购买股票\n" %(variables.PLAYER_NAME[variables.TURN])
                            s.sendall(buy_stock_msg([0,]*7))
                        n_brick = take_brick()
                        if n_brick==-1:
                            variables.MY_LOG+="没有新的地块了\n"
                        else:
                            print("n_brick:",n_brick)
                            s.sendall(new_brick(variables.MY_ID,n_brick))
                        end_turn()
                        s.sendall(send_end_turn(variables.MY_ID))
                        variables.my_turn=False
                    elif idx==7 and variables.has_put_flag:
                        variables.buy_stock_flag=True
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        if variables.place_flag or variables.establish_flag or variables.acquire_flag: #have already place a brick
            cnt = detect_connection(variables.brick_idx)
            # print(cnt)
            if cnt==-1:
                pass
            elif cnt==0 and variables.LIVE_COMPANY!=[1,]*7: #single
                select_company(DISPLAYSURF,[1-i for i in variables.LIVE_COMPANY])
                variables.establish_flag = True
                # variables.company_choice_flag = True
            elif cnt==1: #expand
                expand(variables.brick_idx)
            elif cnt==2: #acquire
                c1,c2 = acquire_list(variables.brick_idx)
                if variables.COMPANY_SIZE[c1]>=3 and variables.COMPANY_SIZE[c2]>=3: #safe company
                    desert(variables.brick_idx)
                    variables.MY_LOG+="均为安全公司，废弃地块%s\n" %(idx2str(variables.brick_idx))
                elif variables.COMPANY_SIZE[c1]==variables.COMPANY_SIZE[c2]:
                    variables.AC_LIST[c1]=1
                    variables.AC_LIST[c2]=1
                    select_company(DISPLAYSURF,variables.AC_LIST)
                    variables.acquire_flag = True
                else:
                    large_idx = c1 if variables.COMPANY_SIZE[c1]>variables.COMPANY_SIZE[c2] else c2
                    variables.AC_LIST[c1]=1
                    variables.AC_LIST[c2]=1
                    variables.AC_LIST[large_idx]=2
                    variables.LARGE_COMPANY = large_idx
                    variables.SMALL_COMPANY = variables.AC_LIST.index(1)
                    acquire(variables.brick_idx,large_idx)
                    s.sendall(acquire_msg(variables.brick_idx,large_idx))
                    variables.deal_stock_flag = True
            elif cnt>=3:
                desert(variables.brick_idx)
            variables.place_flag = False

        if variables.buy_stock_flag:
            select_stock(DISPLAYSURF)

        if variables.deal_stock_flag and not variables.acquire_flag:
            deal_stock(DISPLAYSURF)
        # deal_stock(DISPLAYSURF)
        # if (0,0) in variables.HAND_BRICK:
        #     take_brick()
        pygame.display.update()
        clock.tick()
        # print(clock.get_fps())
        # print(pygame.time.get_ticks())
    s.sendall(send_exit())
    s.close()

if __name__ == "__main__":
    main()
