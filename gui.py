import pygame
from my_color import *
from utility import *
import variables
from constants import *

pygame.font.init()
C_FONT = pygame.font.Font("simsun.ttf",13)
C_FONT_12 = pygame.font.Font("simsun.ttf",12)
C_FONT_13 = pygame.font.Font("simsun.ttf",13)
C_FONT_14 = pygame.font.Font("simsun.ttf",14)
C_FONT_15 = pygame.font.Font("simsun.ttf",15)
C_FONT_15_B = pygame.font.Font("simsun.ttf",15)
C_FONT_15_B.set_bold(True)
C_FONT_20 = pygame.font.Font("simsun.ttf",20)
C_FONT_20_B = pygame.font.Font("simsun.ttf",20)
C_FONT_20_B.set_bold(True)
E_FONT = pygame.font.Font("Arial.ttf",11)
E_FONT_14 = pygame.font.Font("Arial.ttf",14)
E_FONT_B = pygame.font.Font("Arial.ttf",11)
E_FONT_B.set_bold(True)
E_FONT_14_B = pygame.font.Font("Arial.ttf",14)
E_FONT_14_B.set_bold(True)
E_FONT_U = pygame.font.Font("Arial.ttf",11)
E_FONT_U.set_underline(True)
TNM = pygame.font.Font("Times New Roman.ttf",11)

def draw_frame(DISPLAYSURF):
        pygame.draw.rect(DISPLAYSURF,GRAYWHITE,MAP,2)
        pygame.draw.rect(DISPLAYSURF,GRAYWHITE,STOCK,2)
        pygame.draw.rect(DISPLAYSURF,GRAYWHITE,STATE,2)
        pygame.draw.rect(DISPLAYSURF,GRAYWHITE,LOG_WND,2)
        pygame.draw.rect(DISPLAYSURF,CYAN,SQUARE1,1)
        pygame.draw.rect(DISPLAYSURF,CYAN,SQUARE2,1)
        pygame.draw.rect(DISPLAYSURF,CYAN,SQUARE3,1)
        pygame.draw.rect(DISPLAYSURF,CYAN,SQUARE4,1)
        pygame.draw.rect(DISPLAYSURF,CYAN,SQUARE5,1)
        pygame.draw.rect(DISPLAYSURF,CYAN,SQUARE6,1)
        pygame.draw.rect(DISPLAYSURF,GREEN,C_NAME,1)
        pygame.draw.rect(DISPLAYSURF,BLUE,ESC_BTN,1)
        pygame.draw.rect(DISPLAYSURF,PINK,RULE)
        pygame.draw.rect(DISPLAYSURF,GRAYWHITE,NOTE_MEMBER,1)
        pygame.draw.rect(DISPLAYSURF,GRAYWHITE,REST_BLOCK,1)


def draw_bricks(DISPLAYSURF):
    map_lenth = MAP[2]
    map_height = MAP[3]
    blank_width = 10
    blank_height = 20
    brick_length = (map_lenth-2*blank_width)//12
    tl = (blank_width+MAP[0],blank_height+MAP[1])
    for i in range(12):
        for j in range(9):
            n_rect=pygame.draw.rect(DISPLAYSURF,COLORLIST[variables.BRICK_COLOR[coord2idx(i+1,j+1)]],(tl[0]+i*brick_length,tl[1]+j*brick_length,brick_length-1,brick_length-1))
            pygame.draw.rect(DISPLAYSURF,WHITE,n_rect,1)
            txt = E_FONT.render("T"+str(i+1)+str(j+1),True,BLACK)
            txt_rect = txt.get_rect()
            txt_rect.center = n_rect.center
            # txt_rect.center = (tl[0]+(i+0.5)*brick_length,tl[1]+(j+0.5)*brick_length)
            DISPLAYSURF.blit(txt,txt_rect)

def draw_stock(DISPLAYSURF,stock_pic):
    blank_width = 10
    blank_height = 20
    company=pygame.Rect(STOCK[0]+blank_width,STOCK[1]+blank_height,100,30)
    company_txt = C_FONT.render("公司",True,BLACK)
    company_txt_rect = company_txt.get_rect()
    company_txt_rect.center = company.center
    DISPLAYSURF.blit(company_txt,company_txt_rect)
    for i in range(7):
        n_rect = pygame.Rect(company[0],company[1]+40*(i+1),100,30)
        company_txt = E_FONT_14.render(COMPANY_NAME[i],True,COLORLIST[i])
        company_txt_rect = company_txt.get_rect()
        company_txt_rect.center = n_rect.center
        DISPLAYSURF.blit(company_txt,company_txt_rect)

    company_size=pygame.Rect(company[0]+company[2]+blank_width,STOCK[1]+blank_height,50,30)
    company_size_txt = C_FONT.render("公司规模",True,BLACK)
    company_size_txt_rect = company_size_txt.get_rect()
    company_size_txt_rect.center = company_size.center
    DISPLAYSURF.blit(company_size_txt,company_size_txt_rect)
    for i in range(7):
        n_rect = pygame.Rect(company_size[0],company_size[1]+40*(i+1),50,30)
        pygame.draw.rect(DISPLAYSURF,COLORLIST[i],n_rect)
        company_size_txt = E_FONT_14.render(str(variables.COMPANY_SIZE[i]),True,BLACK)
        company_size_txt_rect = company_size_txt.get_rect()
        company_size_txt_rect.center = n_rect.center
        DISPLAYSURF.blit(company_size_txt,company_size_txt_rect)
    
    price=pygame.Rect(company_size[0]+company_size[2]+blank_width,STOCK[1]+blank_height,50,30)
    price_txt = C_FONT.render("股价",True,BLACK)
    price_txt_rect = price_txt.get_rect()
    price_txt_rect.center = price.center
    DISPLAYSURF.blit(price_txt,price_txt_rect)
    for i in range(7):
        n_rect = pygame.Rect(price[0],price[1]+40*(i+1),50,30)
        pygame.draw.rect(DISPLAYSURF,COLORLIST[i],n_rect)
        price_txt = E_FONT_14.render(str(variables.COMPANY_PRICE[i]),True,BLACK)
        price_txt_rect = price_txt.get_rect()
        price_txt_rect.center = n_rect.center
        DISPLAYSURF.blit(price_txt,price_txt_rect)

    stock_num=pygame.Rect(price[0]+price[2]+blank_width,STOCK[1]+blank_height,50,30)
    stock_num_txt = C_FONT.render("发行量",True,BLACK)
    stock_num_txt_rect = stock_num_txt.get_rect()
    stock_num_txt_rect.center = stock_num.center
    DISPLAYSURF.blit(stock_num_txt,stock_num_txt_rect)
    for i in range(7):
        n_rect = pygame.Rect(stock_num[0],stock_num[1]+40*(i+1),50,30)
        pygame.draw.rect(DISPLAYSURF,COLORLIST[i],n_rect)
        stock_num_txt = E_FONT_14.render(str(variables.COMPANY_STOCK_NUM[i]),True,BLACK)
        stock_num_txt_rect = stock_num_txt.get_rect()
        stock_num_txt_rect.center = n_rect.center
        DISPLAYSURF.blit(stock_num_txt,stock_num_txt_rect)

    # stock_pic = pygame.transform.rotate(stock_pic, -90) 
    pic_rect = stock_pic.get_rect()
    pic_rect.center = pygame.Rect(stock_num[0]+stock_num[2]+180,stock_num[1]+140,50,30).center
    DISPLAYSURF.blit(stock_pic,pic_rect)

def draw_state(DISPLAYSURF):
    blank_width = 10
    blank_height = 20
    player=pygame.Rect(STATE[0]+blank_width,STATE[1]+blank_height,60,20)
    player_txt = C_FONT.render("用户",True,BLACK)
    player_txt_rect = player_txt.get_rect()
    player_txt_rect.center = player.center
    DISPLAYSURF.blit(player_txt,player_txt_rect)
    for i in range(variables.NUM_PLAYER):
        n_rect = pygame.Rect(player[0],player[1]+30*(i+1),60,20)
        # E_FONT.size(14)
        # E_FONT_14.set_bold(True)
        player_txt = E_FONT.render(variables.PLAYER_NAME[i],True,BLACK)
        player_txt_rect = player_txt.get_rect()
        player_txt_rect.center = n_rect.center
        DISPLAYSURF.blit(player_txt,player_txt_rect)

    money=pygame.Rect(player[0]+player[2]+blank_width,player[1],50,20)
    money_txt = C_FONT.render("金钱",True,BLACK)
    money_txt_rect = money_txt.get_rect()
    money_txt_rect.center = money.center
    DISPLAYSURF.blit(money_txt,money_txt_rect)
    for i in range(variables.NUM_PLAYER):
        n_rect = pygame.Rect(money[0],money[1]+30*(i+1),50,20)
        pygame.draw.rect(DISPLAYSURF,WHITE,n_rect)
        money_txt = E_FONT.render(str(variables.MONEY[i]),True,BLACK)
        money_txt_rect = money_txt.get_rect()
        money_txt_rect.center = n_rect.center
        DISPLAYSURF.blit(money_txt,money_txt_rect)

    turn=pygame.Rect(money[0]+money[2]+blank_width,money[1],40,20)
    turn_txt = C_FONT.render("执行",True,BLACK)
    turn_txt_rect = turn_txt.get_rect()
    turn_txt_rect.center = turn.center
    DISPLAYSURF.blit(turn_txt,turn_txt_rect)
    for i in range(variables.NUM_PLAYER):
        n_rect = pygame.Rect(turn[0]+10,turn[1]+30*(i+1),20,20)
        if i==variables.TURN:
            pygame.draw.rect(DISPLAYSURF,NOTEBLUE,n_rect)
        else:
            pygame.draw.rect(DISPLAYSURF,BLACK,n_rect)
        DISPLAYSURF.blit(turn_txt,turn_txt_rect)
    

    for j in range(len(COMPANY_NAME)):
        market=pygame.Rect(turn[0]+50+(55+blank_width)*j,player[1],50,20)
        market_txt = E_FONT_B.render(COMPANY_NAME[j],True,COLORLIST[j])
        market_txt_rect = market_txt.get_rect()
        market_txt_rect.center = market.center
        DISPLAYSURF.blit(market_txt,market_txt_rect)
        for i in range(variables.NUM_PLAYER):
            n_rect = pygame.Rect(market[0]+5,market[1]+30*(i+1),40,20)
            if variables.MAJOR_MINOR[i][j]==2:
                pygame.draw.rect(DISPLAYSURF,BIGCOLOR,n_rect)
            elif variables.MAJOR_MINOR[i][j]==1:
                pygame.draw.rect(DISPLAYSURF,SMALLCOLOR,n_rect)
            else:
                pygame.draw.rect(DISPLAYSURF,WHITE,n_rect)
            # pygame.draw.rect(DISPLAYSURF,WHITE,n_rect)
            market_txt = E_FONT.render(str(variables.STOCK_AT_HAND[i][j]),True,BLACK)
            market_txt_rect = market_txt.get_rect()
            market_txt_rect.center = n_rect.center
            DISPLAYSURF.blit(market_txt,market_txt_rect)

def draw_hand_brick(DISPLAYSURF,hand_brick_list):
    for i in range(6):
        n_rect = pygame.Rect(SQUARE1[0]+50*i,SQUARE1[1],SQUARE1[2],SQUARE1[3])
        color = GRAYWHITE if variables.my_turn else NEARWHITE
        font_color = BLACK if variables.my_turn else GRAYWHITE
        pygame.draw.rect(DISPLAYSURF,color,n_rect)
        if hand_brick_list[i]!=(0,0):
            SQUARE_txt = E_FONT_14.render(brick2str(hand_brick_list[i]),True,font_color)
            SQUARE_txt_rect = SQUARE_txt.get_rect()
            SQUARE_txt_rect.center = n_rect.center
            DISPLAYSURF.blit(SQUARE_txt,SQUARE_txt_rect)

def draw_c_name(DISPLAYSURF,turn):
    n_rect = pygame.Rect(C_NAME)
    pygame.draw.rect(DISPLAYSURF,PINK,n_rect)
    TURN_txt = C_FONT_15_B.render("轮到 "+variables.PLAYER_NAME[turn]+" 决策",True,BLACK)
    TURN_txt_rect = TURN_txt.get_rect()
    TURN_txt_rect.center = n_rect.center
    DISPLAYSURF.blit(TURN_txt,TURN_txt_rect)

def draw_end(DISPLAYSURF):
    n_rect = pygame.Rect(ESC_BTN)
    color = LIGHTSKY if variables.my_turn else NEARWHITE
    font_color = BLACK if variables.my_turn else GRAYWHITE
    pygame.draw.rect(DISPLAYSURF,color,n_rect)
    ESC_txt = C_FONT_15_B.render("结束回合",True,font_color)
    ESC_txt_rect = ESC_txt.get_rect()
    ESC_txt_rect.center = n_rect.center
    DISPLAYSURF.blit(ESC_txt,ESC_txt_rect)

def draw_rule(DISPLAYSURF):
    rule = "游戏结束条件（满足其一即可）：\n1.全部地皮都被用完。\n2.有一家公司规模至少为41。\n3.所有上市公司规模至少为11。"
    draw_cut_txt(rule,RULE,DISPLAYSURF,C_FONT)

def draw_note(DISPLAYSURF):
    NOTE_txt = C_FONT.render("说明",True,BLACK)
    n_rect = NOTE_txt.get_rect()
    n_rect.center = pygame.Rect(NOTE_MEMBER[0],NOTE_MEMBER[1]+5,NOTE_MEMBER[2],NOTE_MEMBER[3]/4).center
    DISPLAYSURF.blit(NOTE_txt,n_rect)
    big_block = pygame.draw.rect(DISPLAYSURF,BIGCOLOR,(NOTE_MEMBER[0]+5,NOTE_MEMBER[1]+NOTE_MEMBER[3]/4+10,15,10))
    BIG_txt = C_FONT_12.render("大股东",True,BLACK)
    big_rect = BIG_txt.get_rect()
    big_rect.center = pygame.Rect(big_block[0]+big_block[2]+10,big_block[1]-1,20,big_block[3]).center
    DISPLAYSURF.blit(BIG_txt,big_rect)
    second_block = pygame.draw.rect(DISPLAYSURF,SMALLCOLOR,(NOTE_MEMBER[0]+5,NOTE_MEMBER[1]+NOTE_MEMBER[3]/2+10,15,10))
    SECOND_txt = C_FONT_12.render("二股东",True,BLACK)
    second_rect = SECOND_txt.get_rect()
    second_rect.center = pygame.Rect(second_block[0]+second_block[2]+10,second_block[1]-1,20,second_block[3]).center
    DISPLAYSURF.blit(SECOND_txt,second_rect)

def draw_buy_menu(DISPLAYSURF):
    color = IVORY if variables.my_turn else NEARWHITE
    font_color = BLACK if variables.my_turn else GRAYWHITE
    pygame.draw.rect(DISPLAYSURF,color,BUY_MENU)
    BUY_txt = C_FONT_12.render("购买股票",True,font_color)
    n_rect = BUY_txt.get_rect()
    n_rect.center = pygame.Rect(BUY_MENU).center
    DISPLAYSURF.blit(BUY_txt,n_rect)

def draw_rest_block(DISPLAYSURF):
    REST_txt = C_FONT_12.render("剩余地块数",True,BLACK)
    rect1 = REST_txt.get_rect()
    rect1.center = pygame.Rect(REST_BLOCK[0],REST_BLOCK[1],REST_BLOCK[2],REST_BLOCK[3]/4).center
    DISPLAYSURF.blit(REST_txt,rect1)
    REST_txt = E_FONT_14.render(str(variables.REMAINING_BLOCK_NUM),True,BLACK)
    rect2 = REST_txt.get_rect()
    rect2.center = pygame.Rect(REST_BLOCK[0],REST_BLOCK[1]+REST_BLOCK[3]/4,REST_BLOCK[2],REST_BLOCK[3]/4).center
    pygame.draw.rect(DISPLAYSURF,WHITE,(rect1[0],rect1[1]+25,rect1[2],REST_BLOCK[3]/6))
    DISPLAYSURF.blit(REST_txt,rect2)

    BLANK_txt = C_FONT_12.render("空白地块数",True,BLACK)
    rect3 = BLANK_txt.get_rect()
    rect3.center = pygame.Rect(REST_BLOCK[0],REST_BLOCK[1]+REST_BLOCK[3]/2,REST_BLOCK[2],REST_BLOCK[3]/4).center
    DISPLAYSURF.blit(BLANK_txt,rect3)
    BLANK_txt = E_FONT_14.render(str(variables.BLANK_BLOCK_NUM),True,BLACK)
    rect4 = BLANK_txt.get_rect()
    rect4.center = pygame.Rect(REST_BLOCK[0],REST_BLOCK[1]+REST_BLOCK[3]*3/4,REST_BLOCK[2],REST_BLOCK[3]/4).center
    pygame.draw.rect(DISPLAYSURF,WHITE,(rect3[0],rect3[1]+25,rect3[2],REST_BLOCK[3]/6))
    DISPLAYSURF.blit(BLANK_txt,rect4)

def draw_log(DISPLAYSURF):
    # variables.MY_LOG = "LEO: GL,HF!\nLEO: GG\nLEO: GG again\n"
    display_log = variables.MY_LOG if variables.MY_LOG.count('\n')<=17 else "\n".join(variables.MY_LOG.split('\n')[-(1+17):-1])+'\n'
    draw_cut_txt(display_log,LOG_WND,DISPLAYSURF,C_FONT_14,17)

def which_btn(mousex,mousey,btn_list):
    for btn in btn_list:
        if pygame.Rect(btn).collidepoint(mousex,mousey):
            # print(btn_list.index(btn))
            return btn_list.index(btn)
    return -1

def select_company(DISPLAYSURF,available_list):
    s2 = DISPLAYSURF.convert_alpha()
    s2.fill((255,255,255,230))
    for c in range(len(C_BUTTON_LIST)):
        if available_list[c]==1:
            n_rect = pygame.draw.rect(s2, COLORLIST[c], pygame.Rect(C_BUTTON_LIST[c]))
            company_txt = E_FONT_14_B.render(COMPANY_NAME[c],True,BLACK)
        else:
            n_rect = pygame.draw.rect(s2, GRAY, pygame.Rect(C_BUTTON_LIST[c]))
            company_txt = E_FONT_14_B.render(COMPANY_NAME[c],True,WHITE)
        company_txt_rect = company_txt.get_rect()
        company_txt_rect.center = n_rect.center
        s2.blit(company_txt,company_txt_rect)
    DISPLAYSURF.blit(s2,(0,0))

def select_stock(DISPLAYSURF):
    s2 = DISPLAYSURF.convert_alpha()
    s2.fill((255,255,255,230))
    for c in range(len(C_BUTTON_LIST)):
        if variables.COMPANY_STOCK_NUM[c]!=0 and variables.LIVE_COMPANY[c]:
            n_rect = pygame.draw.rect(s2, COLORLIST[c], pygame.Rect(C_BUTTON_LIST[c]))
            company_txt = E_FONT_14_B.render(COMPANY_NAME[c],True,BLACK)
        else:
            n_rect = pygame.draw.rect(s2, GRAY, pygame.Rect(C_BUTTON_LIST[c]))
            company_txt = E_FONT_14_B.render(COMPANY_NAME[c],True,WHITE)
        company_txt_rect = company_txt.get_rect()
        company_txt_rect.center = n_rect.center
        s2.blit(company_txt,company_txt_rect)
        n_rect[1]+=100
        pygame.draw.rect(s2, GRAYWHITE, pygame.Rect(n_rect))
        stock_txt = E_FONT_14_B.render(str(variables.BUY_STOCK_LIST[c]),True,BLACK)
        stock_txt_rect = stock_txt.get_rect()
        stock_txt_rect.center = n_rect.center
        s2.blit(stock_txt,stock_txt_rect)

    buy_C_txt = C_FONT_12.render(str("本轮购买股数"),True,BLACK)
    buy_C_txt_rect = buy_C_txt.get_rect()
    buy_C_txt_rect.center = pygame.Rect(450,560,80,30).center
    s2.blit(buy_C_txt,buy_C_txt_rect)
    buy_num = pygame.draw.rect(s2, GRAYWHITE, pygame.Rect(450,600,80,30))
    buy_num_txt = E_FONT_14_B.render(str(sum(variables.BUY_STOCK_LIST)),True,BLACK)
    buy_num_txt_rect = buy_num_txt.get_rect()
    buy_num_txt_rect.center = buy_num.center
    s2.blit(buy_num_txt,buy_num_txt_rect)

    price_C_txt = C_FONT_12.render(str("需要资金"),True,BLACK)
    price_C_txt_rect = price_C_txt.get_rect()
    price_C_txt_rect.center = pygame.Rect(550,560,80,30).center
    s2.blit(price_C_txt,price_C_txt_rect)
    price_num = pygame.draw.rect(s2, GRAYWHITE, pygame.Rect(550,600,80,30))
    price_num_txt = E_FONT_14_B.render(str(buy_cost(variables.BUY_STOCK_LIST)),True,BLACK)
    price_num_txt_rect = price_num_txt.get_rect()
    price_num_txt_rect.center = price_num.center
    s2.blit(price_num_txt,price_num_txt_rect)

    money_C_txt = C_FONT_12.render(str("剩余资金"),True,BLACK)
    money_C_txt_rect = money_C_txt.get_rect()
    money_C_txt_rect.center = pygame.Rect(650,560,80,30).center
    s2.blit(money_C_txt,money_C_txt_rect)
    money_num = pygame.draw.rect(s2, GRAYWHITE, pygame.Rect(650,600,80,30))
    money_num_txt = E_FONT_14_B.render(str(variables.MONEY[variables.TURN]-buy_cost(variables.BUY_STOCK_LIST)),True,BLACK)
    money_num_txt_rect = money_num_txt.get_rect()
    money_num_txt_rect.center = money_num.center
    s2.blit(money_num_txt,money_num_txt_rect)

    confirm_C_txt = C_FONT_12.render(str("确认"),True,BLACK)
    confirm_C_txt_rect = confirm_C_txt.get_rect()
    confirm_C_txt_rect.center = pygame.draw.rect(s2, GRAYWHITE, S_CONFIRM).center
    s2.blit(confirm_C_txt,confirm_C_txt_rect)

    cancel_C_txt = C_FONT_12.render(str("取消"),True,BLACK)
    cancel_C_txt_rect = cancel_C_txt.get_rect()
    cancel_C_txt_rect.center = pygame.draw.rect(s2, GRAYWHITE, S_CANCEL).center
    s2.blit(cancel_C_txt,cancel_C_txt_rect)

    DISPLAYSURF.blit(s2,(0,0))

def deal_stock(DISPLAYSURF): #deal with stocks after acquire
    s2 = DISPLAYSURF.convert_alpha()
    s2.fill((255,255,255,230))
    pygame.draw.rect(s2, GRAYWHITE, pygame.Rect(DEAL_STOCK_FRAME),2)
    note_txt_center = (DEAL_STOCK_FRAME[0]+DEAL_STOCK_FRAME[2]/2,DEAL_STOCK_FRAME[1]+DEAL_STOCK_FRAME[3]/7)
    note_txt = C_FONT_20.render("您持有%s股%s，如何处理？"%(variables.STOCK_AT_HAND[variables.MY_ID][variables.SMALL_COMPANY],COMPANY_NAME[variables.SMALL_COMPANY]),True,BLACK)
    note_txt_rect = note_txt.get_rect()
    note_txt_rect.center = note_txt_center
    s2.blit(note_txt,note_txt_rect)

    sell_note_txt_center = (DEAL_STOCK_FRAME[0]+DEAL_STOCK_FRAME[2]/6,DEAL_STOCK_FRAME[1]+DEAL_STOCK_FRAME[3]/3)
    sell_note_txt = C_FONT_15.render("出售股票",True,BLACK)
    sell_note_txt_rect = sell_note_txt.get_rect()
    sell_note_txt_rect.center = sell_note_txt_center
    s2.blit(sell_note_txt,sell_note_txt_rect)
    sell_btn = pygame.Rect(SELL_STOCK_BTN)
    sell_btn.center = (sell_note_txt_center[0]+DEAL_STOCK_FRAME[2]/2,sell_note_txt_center[1])
    pygame.draw.rect(s2, GRAYWHITE, sell_btn)
    sell_btn_txt = C_FONT_15.render("以每股%s元出售" %variables.COMPANY_PRICE[variables.SMALL_COMPANY],True,BLACK)
    sell_btn_txt_rect = sell_btn_txt.get_rect()
    sell_btn_txt_rect.center = sell_btn.center
    s2.blit(sell_btn_txt,sell_btn_txt_rect)

    change_note_txt_center = (DEAL_STOCK_FRAME[0]+DEAL_STOCK_FRAME[2]/6,DEAL_STOCK_FRAME[1]+DEAL_STOCK_FRAME[3]/2)
    change_note_txt = C_FONT_15.render("转换为新公司股票",True,BLACK)
    change_note_txt_rect = change_note_txt.get_rect()
    change_note_txt_rect.center = change_note_txt_center
    s2.blit(change_note_txt,change_note_txt_rect)
    change_btn = pygame.Rect(CHANGE_STOCK_BTN)
    change_btn.center = (change_note_txt_center[0]+DEAL_STOCK_FRAME[2]/2,change_note_txt_center[1])
    pygame.draw.rect(s2, GRAYWHITE, change_btn)
    change_btn_txt = C_FONT_15.render("以2：1的比例转换为%s的股票" %COMPANY_NAME[variables.LARGE_COMPANY],True,BLACK)
    change_btn_txt_rect = change_btn_txt.get_rect()
    change_btn_txt_rect.center = change_btn.center
    s2.blit(change_btn_txt,change_btn_txt_rect)

    money_txt = C_FONT_15.render(str("当前资金"),True,BLACK)
    money_txt_rect = money_txt.get_rect()
    money_txt_rect.center = pygame.Rect(350,460,40,30).center
    s2.blit(money_txt,money_txt_rect)
    money_num = pygame.draw.rect(s2, NEARWHITE, pygame.Rect(420,460,60,30))
    money_num_txt = C_FONT_15_B.render(str(variables.MONEY[variables.MY_ID]+variables.COMPANY_PRICE[variables.SMALL_COMPANY]*variables.TMP_SELL),True,BLACK)
    money_num_txt_rect = money_num_txt.get_rect()
    money_num_txt_rect.center = money_num.center
    s2.blit(money_num_txt,money_num_txt_rect)

    old_stock_txt = C_FONT_15.render(str("旧公司股数"),True,BLACK)
    old_stock_txt_rect = old_stock_txt.get_rect()
    old_stock_txt_rect.center = pygame.Rect(540,460,40,30).center
    s2.blit(old_stock_txt,old_stock_txt_rect)
    old_stock_num = pygame.draw.rect(s2, NEARWHITE, pygame.Rect(610,460,60,30))
    old_stock_num_txt = C_FONT_15_B.render(str(variables.STOCK_AT_HAND[variables.MY_ID][variables.SMALL_COMPANY]-variables.TMP_DECREASE),True,BLACK)
    old_stock_num_txt_rect = old_stock_num_txt.get_rect()
    old_stock_num_txt_rect.center = old_stock_num.center
    s2.blit(old_stock_num_txt,old_stock_num_txt_rect)

    new_stock_txt = C_FONT_15.render(str("新公司股数"),True,BLACK)
    new_stock_txt_rect = new_stock_txt.get_rect()
    new_stock_txt_rect.center = pygame.Rect(730,460,40,30).center
    s2.blit(new_stock_txt,new_stock_txt_rect)
    new_stock_num = pygame.draw.rect(s2, NEARWHITE, pygame.Rect(800,460,60,30))
    new_stock_num_txt = C_FONT_15_B.render(str(variables.STOCK_AT_HAND[variables.MY_ID][variables.LARGE_COMPANY]+variables.TMP_CHANGE),True,BLACK)
    new_stock_num_txt_rect = new_stock_num_txt.get_rect()
    new_stock_num_txt_rect.center = new_stock_num.center
    s2.blit(new_stock_num_txt,new_stock_num_txt_rect)

    confirm_C_txt = C_FONT_15.render(str("确认"),True,BLACK)
    confirm_C_txt_rect = confirm_C_txt.get_rect()
    confirm_C_txt_rect.center = pygame.draw.rect(s2, GRAYWHITE, pygame.Rect(D_CONFIRM_BTN)).center
    s2.blit(confirm_C_txt,confirm_C_txt_rect)

    reset_C_txt = C_FONT_15.render(str("重置"),True,BLACK)
    reset_C_txt_rect = reset_C_txt.get_rect()
    reset_C_txt_rect.center = pygame.draw.rect(s2, GRAYWHITE, pygame.Rect(D_RESET_BTN)).center
    s2.blit(reset_C_txt,reset_C_txt_rect)    
    
    DISPLAYSURF.blit(s2,(0,0))

def display_box(screen, message,RECT):
    # "Print a message in a box in the middle of the screen"
    fontobject = pygame.font.Font(None,18)
    pygame.draw.rect(screen, (0,0,0),RECT, 0)
    pygame.draw.rect(screen, (255,255,255),RECT, 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255,255,255)),(RECT[0]+2,RECT[1]+RECT[3]/3))
    pygame.display.flip()

def draw_win_screen(DISPLAYSURF):
    s2 = DISPLAYSURF.convert_alpha()
    s2.fill((255,255,255,230))
    pygame.draw.rect(s2,WHITE,WIN_FRAME)
    pygame.draw.rect(s2,BLACK,WIN_FRAME,1)
    note_txt_center = (WIN_FRAME[0]+WIN_FRAME[2]/2,WIN_FRAME[1]+WIN_FRAME[3]/12)
    note_txt = C_FONT_20.render("游戏结束",True,BLACK)
    note_txt_rect = note_txt.get_rect()
    note_txt_rect.center = note_txt_center
    s2.blit(note_txt,note_txt_rect)
    rank_txt_center = (WIN_FRAME[0]+WIN_FRAME[2]/6,WIN_FRAME[1]+WIN_FRAME[3]/5)
    rank_txt = C_FONT_15_B.render("排名",True,BLACK)
    rank_txt_rect = rank_txt.get_rect()
    rank_txt_rect.center = rank_txt_center
    s2.blit(rank_txt,rank_txt_rect)
    name_txt_center = (WIN_FRAME[0]+WIN_FRAME[2]/2,WIN_FRAME[1]+WIN_FRAME[3]/5)
    name_txt = C_FONT_15_B.render("姓名",True,BLACK)
    name_txt_rect = name_txt.get_rect()
    name_txt_rect.center = name_txt_center
    s2.blit(name_txt,name_txt_rect)
    property_txt_center = (WIN_FRAME[0]+WIN_FRAME[2]*5/6,WIN_FRAME[1]+WIN_FRAME[3]/5)
    property_txt = C_FONT_15_B.render("总资产",True,BLACK)
    property_txt_rect = property_txt.get_rect()
    property_txt_rect.center = property_txt_center
    s2.blit(property_txt,property_txt_rect)
    for i in range(variables.NUM_PLAYER):
        rank_txt_center = (WIN_FRAME[0]+WIN_FRAME[2]/6,WIN_FRAME[1]+WIN_FRAME[3]*((i+1)/9+1/5))
        rank_txt = C_FONT_15_B.render(str(i+1),True,RANK_COLOR[i])
        rank_txt_rect = rank_txt.get_rect()
        rank_txt_rect.center = rank_txt_center
        s2.blit(rank_txt,rank_txt_rect)
        name_txt_center = (WIN_FRAME[0]+WIN_FRAME[2]/2,WIN_FRAME[1]+WIN_FRAME[3]*((i+1)/9+1/5))
        name_txt = C_FONT_15_B.render(str(variables.PLAYER_NAME[variables.FINAL_RANKING[i]]),True,RANK_COLOR[i])
        name_txt_rect = name_txt.get_rect()
        name_txt_rect.center = name_txt_center
        s2.blit(name_txt,name_txt_rect)
        property_txt_center = (WIN_FRAME[0]+WIN_FRAME[2]*5/6,WIN_FRAME[1]+WIN_FRAME[3]*((i+1)/9+1/5))
        property_txt = C_FONT_15_B.render(str(variables.TOTAL_PROPERTY[variables.FINAL_RANKING[i]]),True,RANK_COLOR[i])
        property_txt_rect = property_txt.get_rect()
        property_txt_rect.center = property_txt_center
        s2.blit(property_txt,property_txt_rect)
    DISPLAYSURF.blit(s2,(0,0))