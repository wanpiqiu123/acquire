import random
import pygame
from my_color import *
import variables
# from main import C_FONT

def random_hand_brick():
    # for i in range(6):
    #     l.append((random.randint(0,12),random.randint(0,9)))
    l = random.sample(variables.REMAINING_BLOCK,k=6)
    for i in range(6):
        variables.REMAINING_BLOCK.remove(l[i])
        l[i] = idx2coord(l[i])
    variables.REMAINING_BLOCK_NUM-=6
    return l

def brick2str(brick):
    return 'T'+str(brick[0])+str(brick[1])

def draw_cut_txt(txt,full_rect,DISPLAYSURF,font,*piece):
    cut_result = txt.split('\n')
    blank_width = 10
    blank_height = 5
    if piece:
        block_num=piece[0]
    else:
        block_num = len(cut_result)
    for i in range(len(cut_result)):
        PART_txt = font.render(cut_result[i],True,BLACK)
        PART_txt_rect = PART_txt.get_rect()
        DISPLAYSURF.blit(PART_txt,(full_rect[0]+blank_width,full_rect[1]+full_rect[3]*i/block_num+blank_height))

def idx2coord(idx):
    assert 0<=idx<=108, "INDEX OUT OF RANGE!"
    x = (idx)%12+1
    y = (idx)//12+1
    return (x,y)

def coord2idx(x,y):
    idx = x+y*12-13
    return idx

def idx2str(idx):
    assert 0<=idx<=108, "INDEX OUT OF RANGE!"
    x = (idx)%12+1
    y = (idx)//12+1
    return 'T'+str(10*x+y)

def buy_cost(buy_stock_list):
    return sum([a*b for a,b in zip(buy_stock_list,variables.COMPANY_PRICE)])

def list_sum(l1,l2):
    return [a+b for a,b in zip(l1,l2)]
