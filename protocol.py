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

def original_handbrick(brick_list):
    p = Protocol()
    p.add_str("original brick")
    p.add_int32(len(brick_list))
    for brick in brick_list:
        p.add_int32(brick)
    return p.get_pck_has_head()

def send_place_brick(ID,brick_idx): #place a new brick
    p = Protocol()
    p.add_str("place brick")
    p.add_int32(ID)
    p.add_int32(brick_idx)
    return p.get_pck_has_head()

def new_brick(ID,brick_idx): #tell the client the new brick index
    p = Protocol()
    p.add_str("new brick")
    p.add_int32(ID)
    p.add_int32(brick_idx)
    return p.get_pck_has_head()    

def acquire_msg(brick_idx,company_id):
    p = Protocol()
    p.add_str("acquire msg")
    p.add_int32(brick_idx)
    p.add_int32(company_id)
    return p.get_pck_has_head()

def buy_stock_msg(buy_stock_list): #which stock the player bought
    p = Protocol()
    p.add_str("buy stock")
    for i in range(7):
        p.add_int32(buy_stock_list[i])
    return p.get_pck_has_head()    

def deal_stock_msg(ID,sell,change,small,large):
    p = Protocol()
    p.add_str("deal stock choice")
    p.add_int32(ID)
    p.add_int32(sell)
    p.add_int32(change)
    p.add_int32(small)
    p.add_int32(large)
    return p.get_pck_has_head()

def send_exit():
    p = Protocol()
    p.add_str("exit")
    return p.get_pck_has_head()

def get_id(id):
    p = Protocol()
    p.add_str("id")
    p.add_int32(id)
    return p.get_pck_has_head()

def send_name(ID,name):
    p = Protocol()
    p.add_str("name")
    p.add_int32(ID)
    p.add_str(name)
    return p.get_pck_has_head()

def send_name_list(origin_list,sequence):
    p = Protocol()
    p.add_str("name list")
    p.add_int32(len(origin_list))
    for i in range(len(origin_list)):
        p.add_str(origin_list[sequence[i]])
    return p.get_pck_has_head()

def send_end_turn(ID):
    p = Protocol()
    p.add_str("end turn")
    p.add_int32(ID)
    return p.get_pck_has_head()

def send_establish(company_id):
    p = Protocol()
    p.add_str("establish")
    p.add_int32(company_id)
    return p.get_pck_has_head()

def pck_handler(pck):
    p = Protocol(pck)
    pck_type = p.get_str()
    # if pck_type != "":
    #     print(pck_type) 
    print(pck_type)
    if pck_type=="successful connection":
        print("Successfully connect the server!")
        return [-2,]
    elif pck_type=="exit":
        return [-1,]
    elif pck_type=="place brick":
        ID = p.get_int32()
        brick_idx = p.get_int32()
        # print("%s place a brick on %s" %(ID,brick_idx))
        return [0,ID,brick_idx]
    elif pck_type=="new brick":
        ID = p.get_int32()
        brick_idx = p.get_int32()
        # print("%s get brick %s" %(ID,brick_idx))
        return [1,ID,brick_idx]
    elif pck_type=="id":
        ID = p.get_int32()
        return [2,ID]
    elif pck_type=="acquire msg":
        brick_idx = p.get_int32()
        company_id = p.get_int32()
        return [3,brick_idx,company_id]
    elif pck_type=="name":
        ID = p.get_int32()
        name = p.get_str()
        return [4,ID,name]
    elif pck_type=="name list":
        length = p.get_int32()
        name_list = []
        for i in range(length):
            name_list.append(p.get_str())
        return [5,length,name_list]
    elif pck_type=="original brick":
        length = p.get_int32()
        brick_list = []
        for i in range(length):
            brick_list.append(p.get_int32())
        return [6,brick_list]
    elif pck_type=="buy stock":
        stock_list = []
        for i in range(7):
            stock_list.append(p.get_int32())
        return [7,stock_list]
    elif pck_type=="end turn":
        ID = p.get_int32()
        return [8,ID]
    elif pck_type=="establish":
        company_id = p.get_int32()
        return [9,company_id]
    elif pck_type=="deal stock choice":
        ID = p.get_int32()
        sell = p.get_int32()
        change = p.get_int32()
        small = p.get_int32()
        large = p.get_int32()
        return [10,ID,sell,change,small,large]
    else:
        return [-3,]
