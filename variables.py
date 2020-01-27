NUM_PLAYER = 6
PLAYER_NAME = ['Leo','Qu','John','Risky','player1','player2']
COMPANY_SIZE = [0,]*7 #company size
COMPANY_PRICE = [100,]*7 #stock price
COMPANY_STOCK_NUM = [25,]*7 #how many stocks left
LIVE_COMPANY = [0,]*7 #companys on the board
MONEY = [6000,]*NUM_PLAYER
TURN = 0
MY_LOG = ""

HAND_BRICK = [] #bricks at hand
REMAINING_BLOCK = list(range(108)) #bricks remaining on the deck
REMAINING_BLOCK_NUM = len(REMAINING_BLOCK)
ON_BOARD_NUM = 0
BLANK_BLOCK_NUM = 108 #how many bricks unplaced on the game board
BRICK_COLOR = [-1]*108

AC_LIST = [0,]*7
BUY_STOCK_LIST = [0,]*7
BUY_STOCK_NUM = 0
STOCK_AT_HAND = [[2,]*7 for i in range(NUM_PLAYER)]
MAJOR_MINOR = [[0,]*7 for i in range(NUM_PLAYER)]
TMP_SELL = 0
TMP_CHANGE = 0
TMP_DECREASE = 0
LARGE_COMPANY = 0
SMALL_COMPANY = 0

place_flag = False
brick_idx = None
establish_flag = False
acquire_flag = False
deal_stock_flag = False
buy_stock_flag = False
has_put_flag = False
has_buy_flag = False
