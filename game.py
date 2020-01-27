import pygame
from utility import *
import variables
from constants import *

def place_brick(idx):
    brick_idx = coord2idx(variables.HAND_BRICK[idx][0],variables.HAND_BRICK[idx][1])
    brick_display = variables.HAND_BRICK[idx][0]*10+variables.HAND_BRICK[idx][1]
    variables.BRICK_COLOR[brick_idx]=-2
    variables.HAND_BRICK[idx] = (0,0)
    variables.ON_BOARD_NUM += 1
    variables.BLANK_BLOCK_NUM-=1
    variables.MY_LOG+="%s放置了T%s\n" %(variables.PLAYER_NAME[variables.TURN],brick_display)
    return brick_idx

def take_brick():
    idx = variables.HAND_BRICK.index((0,0))
    n_brick = random.choice(variables.REMAINING_BLOCK)
    variables.HAND_BRICK[idx] = idx2coord(n_brick)
    variables.REMAINING_BLOCK.remove(n_brick)
    variables.REMAINING_BLOCK_NUM-=1

def real_neibour(brick):
    assert 0<=brick<=107, "INVALID BRICK!"
    x,y = idx2coord(brick)
    neibours = [(x,y-1),(x,y+1),(x-1,y),(x+1,y)] 
    real_neibours = []
    for neibour in neibours:
        if 0<neibour[0]<13 and 0<neibour[1]<10:
            real_neibours.append(coord2idx(neibour[0],neibour[1]))
    # print(real_neibours)
    return real_neibours

def detect_connection(brick):
    neibour = real_neibour(brick)
    cnt = 0 #how many kind of companys
    cnt_list = [0,]*9
    for i in neibour:
        if variables.BRICK_COLOR[i]>=0 and cnt_list[variables.BRICK_COLOR[i]]==0: #company
            cnt+=1
        cnt_list[variables.BRICK_COLOR[i]]+=1
    if cnt==0 and cnt_list[-2]==0:
        return -1
    return cnt

def expand(brick):
    neibour = real_neibour(brick)
    single_brick = [brick,]
    company_id = -1
    for i in neibour:
        if variables.BRICK_COLOR[i]==-2: #single brick
            single_brick.append(i)
        elif variables.BRICK_COLOR[i]!=-1: #company
            company_id = variables.BRICK_COLOR[i]
    for b in single_brick:
        variables.BRICK_COLOR[b]=company_id
    variables.COMPANY_SIZE[company_id]+=len(single_brick)

def acquire_list(brick):
    neibour = real_neibour(brick)
    company_id_list = []
    for i in neibour:
        if 0<=variables.BRICK_COLOR[i]<7: #company
            company_id_list.append(variables.BRICK_COLOR[i])
    return company_id_list

def acquire(brick,large_idx):
    neibour = real_neibour(brick)
    single_brick = [brick,]
    small_company_id = -1
    for i in neibour:
        if variables.BRICK_COLOR[i]==-2: #single brick
            single_brick.append(i)
        elif variables.BRICK_COLOR[i]!=-1 and variables.BRICK_COLOR[i]!=large_idx:
            small_company_id = variables.BRICK_COLOR[i]
    for b in single_brick:
        variables.BRICK_COLOR[b]=large_idx
    variables.MY_LOG+="%s公司收购了%s公司\n" %(COMPANY_NAME[variables.LARGE_COMPANY],COMPANY_NAME[variables.SMALL_COMPANY])
    variables.COMPANY_SIZE[large_idx]+=(variables.COMPANY_SIZE[small_company_id]+len(single_brick))
    variables.BRICK_COLOR=[large_idx if value == small_company_id else value for value in variables.BRICK_COLOR]
    variables.COMPANY_SIZE[small_company_id]=0
    variables.LIVE_COMPANY[small_company_id]=0
    company_stock_list = [stock[small_company_id] for stock in variables.MAJOR_MINOR]
    large_num = company_stock_list.count(2)
    small_num = company_stock_list.count(1)
    if small_num==0: #common major or only one major
        share = 15*variables.COMPANY_PRICE[small_company_id]
        for i in range(variables.NUM_PLAYER):
            if variables.MAJOR_MINOR[i][small_company_id]==2:
                ma_share = share//100//large_num*100
                variables.MONEY[i]+=ma_share
                variables.MY_LOG+="%s作为大股东获得分红%s\n" %(variables.PLAYER_NAME[i],ma_share)
    else:
        l_share = 10*variables.COMPANY_PRICE[small_company_id]
        s_share = 5*variables.COMPANY_PRICE[small_company_id]
        for i in range(variables.NUM_PLAYER):
            if variables.MAJOR_MINOR[i][small_company_id]==2:
                ma_share = l_share//100//large_num*100
                variables.MONEY[i]+=ma_share
                variables.MY_LOG+="%s作为大股东获得分红%s\n" %(variables.PLAYER_NAME[i],ma_share)
            elif variables.MAJOR_MINOR[i][small_company_id]==1:
                mi_share = s_share//100//small_num*100
                variables.MONEY[i]+=mi_share
                variables.MY_LOG+="%s作为二股东获得分红%s\n" %(variables.PLAYER_NAME[i],mi_share)
    
def desert(brick):
    pass

def establish(brick,selection):
    neibour = real_neibour(brick)
    single_brick = [brick,]
    for i in neibour:
        if variables.BRICK_COLOR[i]==-2: #single brick
            single_brick.append(i)
    for b in single_brick:
        variables.BRICK_COLOR[b]=selection
    variables.COMPANY_SIZE[selection]+=len(single_brick)
    variables.LIVE_COMPANY[selection]=1
    if variables.COMPANY_STOCK_NUM[selection]>0:
        variables.STOCK_AT_HAND[variables.TURN][selection]+=1
        variables.COMPANY_STOCK_NUM[selection]-=1
    variables.MY_LOG+="%s建立了公司%s\n" %(variables.PLAYER_NAME[variables.TURN],COMPANY_NAME[selection])
    
def update_stock_price():
    for i in range(7):
        c_sz = variables.COMPANY_SIZE[i]
        if c_sz == 0:
            price = 0
        elif 2<=c_sz<=5:
            price = COMPANY_PRICE_TABLE[COMPANY[COMPANY_NAME[i]]+c_sz-2]
        elif 5<c_sz<=10:
            price = COMPANY_PRICE_TABLE[COMPANY[COMPANY_NAME[i]]+4]
        elif 10<c_sz<=20:
            price = COMPANY_PRICE_TABLE[COMPANY[COMPANY_NAME[i]]+5]
        elif 20<c_sz<=30:
            price = COMPANY_PRICE_TABLE[COMPANY[COMPANY_NAME[i]]+6]
        elif 30<c_sz<=40:
            price = COMPANY_PRICE_TABLE[COMPANY[COMPANY_NAME[i]]+7]
        elif c_sz>40:
            price = COMPANY_PRICE_TABLE[COMPANY[COMPANY_NAME[i]]+8]
        variables.COMPANY_PRICE[i]=price
        
def major_minor():
    for i in range(7):
        if variables.LIVE_COMPANY[i]==0:
            for j in range(variables.NUM_PLAYER):
                variables.MAJOR_MINOR[j][i]=0 
        elif variables.LIVE_COMPANY[i]==1:
            company_stock_list = [stock[i] for stock in variables.STOCK_AT_HAND]
            sorted_list = sorted(enumerate(company_stock_list), key=lambda x: x[1],reverse=True)
            idx = [i[0] for i in sorted_list]
            nums = [i[1] for i in sorted_list]
            major_num = nums[0]
            if major_num==0:
                for j in range(variables.NUM_PLAYER):
                    variables.MAJOR_MINOR[idx[j]][i]=0 
            else:
                if nums.count(major_num)>=2: #common major
                    for j in range(nums.count(major_num)):
                        variables.MAJOR_MINOR[idx[j]][i]=2
                else:
                    minor_num = nums[1]
                    variables.MAJOR_MINOR[idx[0]][i]=2
                    if minor_num==0:
                        for j in range(nums.count(minor_num)):
                            variables.MAJOR_MINOR[idx[j+1]][i]=0
                    else:
                        for j in range(nums.count(minor_num)):
                            variables.MAJOR_MINOR[idx[j+1]][i]=1


def end_turn():
    variables.TURN=(variables.TURN+1)%variables.NUM_PLAYER
    variables.BUY_STOCK_NUM=0
    variables.place_flag = False
    variables.brick_idx = None
    variables.establish_flag = False
    variables.acquire_flag = False
    variables.buy_stock_flag = False
    variables.has_put_flag = False
    variables.has_buy_flag = False
    variables.AC_LIST = [0,]*7
    variables.MY_LOG+="\n轮到%s执行\n" %(variables.PLAYER_NAME[variables.TURN])
    take_brick()

