from my_color import LIGHTGRAY

WINDOWWIDTH = 1200
WINDOWHEIGHT = 800
BGCOLOR = LIGHTGRAY

MAP     = (20,20,450,350)
STOCK   = (500,20,680,350)
STATE   = (20,390,650,250)
LOG_WND = (690,390,490,390)
SQUARE1 = (20,660,40,40)
SQUARE2 = (70,660,40,40)
SQUARE3 = (120,660,40,40)
SQUARE4 = (170,660,40,40)
SQUARE5 = (220,660,40,40)
SQUARE6 = (270,660,40,40)
C_1 = (40,300,100,60)
C_2 = (210,300,100,60)
C_3 = (380,300,100,60)
C_4 = (550,300,100,60)
C_5 = (720,300,100,60)
C_6 = (890,300,100,60)
C_7 = (1060,300,100,60)
S_CONFIRM = (500,650,80,30)
S_CANCEL  = (600,650,80,30)

C_NAME  = (20,720,160,60)
ESC_BTN = (190,720,120,60)
RULE    = (320,660,200,120)
NOTE_MEMBER = (530,660,60,70)
BUY_MENU = (530,750,60,30)
REST_BLOCK = (600,660,80,120)

DEAL_STOCK_FRAME = (300,150,600,500)
SELL_STOCK_BTN = (550,296,300,41)
CHANGE_STOCK_BTN = (550,380,300,41)
D_CONFIRM_BTN = (500,540,60,30)
D_RESET_BTN = (650,540,60,30)

BUTTON_LIST = [SQUARE1,SQUARE2,SQUARE3,SQUARE4,SQUARE5,SQUARE6,ESC_BTN,BUY_MENU]
C_BUTTON_LIST = [C_1,C_2,C_3,C_4,C_5,C_6,C_7]
S_BUTTON_LIST = [C_1,C_2,C_3,C_4,C_5,C_6,C_7,S_CONFIRM,S_CANCEL]
D_BUTTON_LIST = [SELL_STOCK_BTN,CHANGE_STOCK_BTN,D_CONFIRM_BTN,D_RESET_BTN]
COMPANY = {'Worldwide':0,'Sackson':0,'Festival':1,'Imperial':1,'American':1,'Continental':2,'Tower':2}
COMPANY_NAME = [x for x,y in COMPANY.items()]
COMPANY_PRICE_TABLE = list(range(200,1300,100))
