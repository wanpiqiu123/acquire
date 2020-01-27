class Protocol:
    """
    规定：
        数据包头部占4字节
        整型占4字节
        字符串长度位占2字节
        字符串不定长
    """
 
    def __init__(self, bs=None):
        """
        如果bs为None则代表需要创建一个数据包
        否则代表需要解析一个数据包
        """
        if bs:
            self.bs = bytearray(bs)
        else:
            self.bs = bytearray(0)
 
    def get_int32(self):
        try:
            ret = self.bs[:4]
            self.bs = self.bs[4:]
            return int.from_bytes(ret, byteorder='little')
        except:
            raise Exception("数据异常！")
 
    def get_str(self):
        try:
            # 拿到字符串字节长度(字符串长度位2字节)
            length = int.from_bytes(self.bs[:2], byteorder='little')
            # 再拿字符串
            ret = self.bs[2:length + 2]
            # 删掉取出来的部分
            self.bs = self.bs[2 + length:]
            return ret.decode(encoding='utf8')
        except:
            raise Exception("数据异常！")
 
    def add_int32(self, val):
        bytes_val = bytearray(val.to_bytes(4, byteorder='little'))
        self.bs += bytes_val
 
    def add_str(self, val):
        bytes_val = bytearray(val.encode(encoding='utf8'))
        bytes_length = bytearray(len(bytes_val).to_bytes(2, byteorder='little'))
        self.bs += (bytes_length + bytes_val)
 
    def get_pck_not_head(self):
        return self.bs
 
    def get_pck_has_head(self):
        bytes_pck_length = bytearray(len(self.bs).to_bytes(4, byteorder='little'))
        return bytes_pck_length + self.bs

def s_connection():
    p = Protocol()
    p.add_str("successful connection")
    return p.get_pck_has_head()

def put_brick(ID,brick_idx): #place a new brick
    p = Protocol()
    p.add_str("put brick")
    p.add_int32(ID)
    p.add_int32(brick_idx)
    return p.get_pck_has_head()

def new_brick(ID,brick_idx): #tell the client the new brick index
    p = Protocol()
    p.add_str("new brick")
    p.add_int32(ID)
    p.add_int32(brick_idx)
    return p.get_pck_has_head()    

def acquire_msg(ID,company_id):
    p = Protocol()
    p.add_str("acquire msg")
    p.add_int32(ID)
    p.add_int32(company_id)
    return p.get_pck_has_head()

def buy_stock_msg(ID,buy_stock_list): #which stock the player bought
    p = Protocol()
    p.add_str("buy stock msg")
    for i in range(7):
        p.add_int32(buy_stock_list[i])
    return p.get_pck_has_head()    

def deal_stock_msg(ID,small_id,large_id,sell,change):
    p = Protocol()
    p.add_str("deal stock choice")
    p.add_int32(ID)
    p.add_int32(small_id)
    p.add_int32(large_id)
    p.add_int32(sell)
    p.add_int32(change)
    return p.get_pck_has_head()

def end_turn():
    p = Protocol()
    p.add_str("exit")
    return p.get_pck_has_head()

def get_id(id):
    p = Protocol()
    p.add_str("id")
    p.add_int32(id)
    return p.get_pck_has_head()

def pck_handler(pck):
    p = Protocol(pck)
    pck_type = p.get_str()
    # if pck_type != "":
    #     print(pck_type) 
    if pck_type=="successful connection":
        print("Successfully connect the server!")
        return [-2,]
    if pck_type=="put brick":
        ID = p.get_int32()
        brick_idx = p.get_int32()
        print("%s place a brick on %s" %(ID,brick_idx))
        return [0,]
    elif pck_type=="new brick":
        ID = p.get_int32()
        brick_idx = p.get_int32()
        print("%s get brick %s" %(ID,brick_idx))
        return [1,]
    elif pck_type=="exit":
        return [-1,]
    elif pck_type=="id":
        ID = p.get_int32()
        return [2,ID]
    elif pck_type=="acquire msg":
        player_id = p.get_int32()
        company_id = p.get_int32()
        return [3,player_id,company_id]
    else:
        return [-2,]
