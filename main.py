import sys
from pygame.locals import *
# from my_color import *
from gui import *
import variables
from game import *
# from utility import *


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

    while True:
        DISPLAYSURF.fill(BGCOLOR)
        draw_frame(DISPLAYSURF)
        draw_esc(DISPLAYSURF)
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

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                if variables.establish_flag:
                    idx = which_btn(mousex,mousey,C_BUTTON_LIST)
                    if 0<=idx<7:
                        establish(variables.brick_idx,idx)
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
                        variables.deal_stock_flag = True
                        variables.acquire_flag=False
                elif variables.buy_stock_flag:
                    idx = which_btn(mousex,mousey,S_BUTTON_LIST)
                    if 0<=idx<7 and variables.COMPANY_STOCK_NUM[idx]!=0 and sum(variables.BUY_STOCK_LIST)<(3-variables.BUY_STOCK_NUM) and variables.LIVE_COMPANY[idx]:
                        variables.BUY_STOCK_LIST[idx]+=1
                    elif idx==7: #confirm
                        variables.MONEY[variables.TURN] = variables.MONEY[variables.TURN]-buy_cost()
                        variables.BUY_STOCK_NUM+=sum(variables.BUY_STOCK_LIST)
                        for i in range(len(variables.BUY_STOCK_LIST)):
                            variables.STOCK_AT_HAND[variables.TURN][i]+=variables.BUY_STOCK_LIST[i]
                            variables.COMPANY_STOCK_NUM[i]-=variables.BUY_STOCK_LIST[i]
                            variables.BUY_STOCK_LIST[i]=0
                        variables.buy_stock_flag=False
                        major_minor()
                    elif idx ==8: #cancel
                        variables.buy_stock_flag=False
                        variables.BUY_STOCK_LIST=[0,]*7

                elif variables.deal_stock_flag:
                    idx = which_btn(mousex,mousey,D_BUTTON_LIST)
                    if idx==0 and variables.STOCK_AT_HAND[variables.TURN][variables.SMALL_COMPANY]-variables.TMP_DECREASE>0:
                        variables.TMP_SELL+=1
                        variables.TMP_DECREASE+=1
                    elif idx==1 and variables.STOCK_AT_HAND[variables.TURN][variables.SMALL_COMPANY]-variables.TMP_DECREASE>1:
                        variables.TMP_CHANGE+=1
                        variables.TMP_DECREASE+=2
                    elif idx==2:
                        variables.MONEY[variables.TURN]+=variables.COMPANY_PRICE[variables.SMALL_COMPANY]*variables.TMP_SELL
                        variables.STOCK_AT_HAND[variables.TURN][variables.SMALL_COMPANY]-=variables.TMP_DECREASE
                        variables.STOCK_AT_HAND[variables.TURN][variables.LARGE_COMPANY]+=variables.TMP_CHANGE
                        variables.COMPANY_STOCK_NUM[variables.SMALL_COMPANY]+=variables.TMP_DECREASE
                        variables.COMPANY_STOCK_NUM[variables.LARGE_COMPANY]-=variables.TMP_CHANGE
                        variables.TMP_SELL=variables.TMP_CHANGE=variables.TMP_DECREASE=0
                        variables.deal_stock_flag=False
                        update_stock_price()
                        major_minor()
                    elif idx==3:
                        variables.TMP_SELL=variables.TMP_CHANGE=variables.TMP_DECREASE=0


                else:
                    idx = which_btn(mousex,mousey,BUTTON_LIST)
                    if idx!=-1 and idx<6 and not variables.has_put_flag:
                        variables.brick_idx = place_brick(idx)
                        variables.place_flag=True
                        variables.has_put_flag=True
                    elif idx==6 and variables.has_put_flag:
                        end_turn()
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
            elif cnt==0: #single
                select_company(DISPLAYSURF,[1-i for i in variables.LIVE_COMPANY])
                variables.establish_flag = True
                # variables.company_choice_flag = True
            elif cnt==1: #expand
                expand(variables.brick_idx)
            elif cnt==2: #acquire
                c1,c2 = acquire_list(variables.brick_idx)
                if variables.COMPANY_SIZE[c1]==variables.COMPANY_SIZE[c2]:
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
                    variables.deal_stock_flag = True


                
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
        


if __name__ == "__main__":
    main()
