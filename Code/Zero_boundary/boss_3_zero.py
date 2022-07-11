'''
陈伟霖
2022年7月2日
本代码是用于求GOE是否存在，如果存在则找到没有原像的配置(层次)【零边界】
这里是老板论文里的算法
目前没有实现图形化功能
'''
from operator import truediv
import string
import numpy as np
from queue import Queue
#全局数据
#字典，用来判断结点内容是否是唯一的，如果出现过则停止
#结点内容->0
unique_table = {}
#规则关系
# 组合->状态
rude = {}
#所有规则
rudes = []
# E 输出集合
E = []
# I 输入集合
I = []
# 遍历队列
q_Node = Queue(maxsize=0)
#规则初始化函数
def get_rude(simplify_rude):
    global rudes,rude
    #字符串反转
    simplify_rude = simplify_rude[::-1]
    for i in range(0,8):
        num = bin(i)[2:]
        num = num.zfill(3)
        rudes.append(num)
        rude[num] = simplify_rude[i]
    # 构造输入集和输出集
    get_E('00')
    get_I('00')

# 获得E 输出集合
def get_E(Sequence):
    global rude,E
    # 添加 0
    temp_Sequence =  Sequence[-2:] + '0'
    if temp_Sequence in rude.keys() and rude[temp_Sequence] == '0'and temp_Sequence[1:] not in E:
        E.append(temp_Sequence[1:])
        get_E(Sequence + '0')
    # 添加 1
    temp_Sequence =  Sequence[-2:] + '1' 
    if temp_Sequence in rude.keys() and rude[temp_Sequence] == '0' and temp_Sequence[1:] not in E:
        E.append(temp_Sequence[1:])
        get_E(Sequence + '1')

# 获得 I 输入集合
def get_I(Sequence):
    global rude,I
    # 添加 0
    temp_Sequence = '0' + Sequence[:2]
    if temp_Sequence in rude.keys() and rude[temp_Sequence] == '0'and temp_Sequence[0:2] not in I:
        I.append(temp_Sequence[0:2])
        get_I('0' + Sequence)
    # 添加 1
    temp_Sequence = '1' + Sequence[:2]
    if temp_Sequence in rude.keys() and rude[temp_Sequence] == '0' and temp_Sequence[0:2] not in I:
        I.append(temp_Sequence[0:2])
        get_I('1' + Sequence )
    
    

# 函数功能：找结点的值
# values：当前结点的值
# id：要走的状态
def get_Node(values,id):
    global rude
    new_values = []
    for value in values:
        temp = value + '0'
        if (temp in rude.keys()) and rude[temp] == str(id):
            new_values.append(temp[1:])
        temp = value + '1'
        if (temp in rude.keys()) and rude[temp] == str(id):
            new_values.append(temp[1:])
    # 删除列表中重复元素
    new_values = list(set(new_values))
    return new_values

#递归函数
# values存的是当前结点的值
# id是当前结点是何种状态
# result记录当前路径上的值（如果是终止结点，则将GOE结果返回到全局变量results中）
def get_GOE():
    global q_Node
    length = q_Node.qsize()
    if length == 0:
        return 1
    for i in range(length):
        values = q_Node.get()
        # 检查是否为空结点
        if len(values) == 0:
            return -1
        # 检查当前结点是否已经出现过
        Value_temp = sorted(values)
        str_value = "".join(Value_temp)
        if str_value in unique_table.keys():
            # 已经出现过该结点,则函数结束
            continue
        # 检查该结点与输入集的交集是否为空
        if len(set(I)&set(values)) == 0 :
            return -1
        unique_table[str_value] = '0'
        # 没有出现过，往下走
        # 走0
        new_values = get_Node(values,0)
        q_Node.put(new_values)
        # 走1
        new_values = get_Node(values,1)
        q_Node.put(new_values) 
    return get_GOE()

#主函数
if __name__ == '__main__':
    # get_rude('11110000')
    # # get_rude('01110100')
    # q_Node.put(E)
    # print(get_GOE())
    # print(E,I)
    # -------------------------------------------------------------------------------
    # 跑256
    # # nums = np.loadtxt('256_No_GOE.txt',dtype=str)
    save_txt = []
    for i in range(0,256):
        num = bin(i)[2:]
        num = num.zfill(8)
        if num[-1] != '0':
            continue
        # 参数清空
        unique_table.clear()
        rude.clear()
        rudes.clear()
        I.clear()
        E.clear()
        q_Node.queue.clear()
        get_rude(num)
        q_Node.put(E)
        if get_GOE() == 1:
            save_txt.append(num)   
    # 输出到txt文件中
    with open('256_result_boss_zero.txt', 'w') as f:
        for value in save_txt:
            f.write(value)
            f.write(': 是满足条件的规则！')
            f.write('\n')


    
    
