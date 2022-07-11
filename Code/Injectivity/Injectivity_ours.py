'''
陈伟霖
2022年7月11日
本代码是我们新算法的实现
用于实现判断规则是否单射
实现了接口length，代表规则长度
目前没有实现图形化功能
'''
import re
import time
from turtle import st
import numpy as np
from queue import Queue
#全局数据
#字典，用来判断结点内容是否是唯一的，如果出现过则停止
#结点内容->0
unique_table = {}
#规则长度
length_rude = 4
#规则关系
# 组合->状态
rude = {}
# 遍历队列
q_Node = Queue(maxsize=0)
#规则初始化函数
def get_rude(simplify_rude):
    global rude,q_Node,length_rude
    #字符串反转
    rude_one = []
    rude_zero = []
    simplify_rude = simplify_rude[::-1]
    for i in range(0,2**length_rude):
        num = bin(i)[2:]
        num = num.zfill(length_rude)
        if simplify_rude[i] == '1':
            rude_one.append(num[:length_rude-1] + num)
        else:
            rude_zero.append(num[:length_rude-1] + num)
        rude[num] = simplify_rude[i]
    q_Node.put(rude_zero)
    q_Node.put(rude_one)

# 函数功能：得到下一个结点的各种信息，包括结点的内容以及原像
# values：当前结点的原像值
# id：要走的状态
def get_Node(values,id):
    global rude,length_rude
    new_nodes = []
    for value in values:
        temp_value = value[-(length_rude-1):]
        temp = temp_value + '0'
        if (temp in rude.keys()) and rude[temp] == str(id):
            new_nodes.append(value[:length_rude-1] + temp)
        temp = temp_value + '1'
        if (temp in rude.keys()) and rude[temp] == str(id):
            new_nodes.append(value[:length_rude-1] + temp)
    # 删除列表中重复元素
    new_nodes = list(set(new_nodes))
    return new_nodes
# 判断结点是否符合规定(过程a和过程b)
def Judgment_node(values):
    global length_rude
    # a过程：不同时出现两个满足循环边界的原像
    # b过程：所有节点内不存在一个元组和另一个元组满足前n-1位相同，后n-1位也相同的情况
    # a过程变量，显示满足循环边界原像的个数
    numbers = 0
    # b过程变量，用于存储原像首n-1位和末n-1位之间的关系
    unique_image = {}
    for value in values:
        # 判断a过程
        if value[:length_rude-1] == value[-(length_rude-1):]:
                numbers = numbers + 1
        # 判断b过程
        if value[:length_rude-1] in unique_image.keys():
            if value[-(length_rude-1):] == unique_image[value[:length_rude-1]]:
                return -1
        else:
            unique_image[value[:length_rude-1]] = value[-(length_rude-1):]
        if numbers == 2:
            return -1
    return 1
        
#递归函数
# values存的是当前结点的值
# id是当前结点是何种状态
# result记录当前路径上的值（如果是终止结点，则将GOE结果返回到全局变量results中）
def get_GOE():
    global q_Node,length_rude
    length = q_Node.qsize()
    if length == 0:
        return 1
    for i in range(length):
        node = q_Node.get()
        # 检查是否为空结点
        if len(node) == 0:
            return -1
        # 判断结点是否符合规定
        if Judgment_node(node) == -1:
            return -1
        # 检查当前结点是否已经出现过
        Node_temp = sorted(node)
        str_Node = "".join(Node_temp)
        if str_Node in unique_table.keys():
            continue
        else:
            unique_table[str_Node] = 0
        # 没有出现过，往下走
        # 走0
        new_nodes = get_Node(node,0)
        q_Node.put(new_nodes)
        # 走1
        new_nodes = get_Node(node,1)
        q_Node.put(new_nodes)
    return get_GOE()

#主函数
if __name__ == '__main__':
    # get_rude('00001111')
    # # get_rude('01110100')
    # print(get_GOE())
    
    # -------------------------------------------------------------------------------
    # 跑全部
    # 程序计时
    time_start = time.time() 
    save_txt = []
    for i in range(0,2**(2**length_rude)):
        num = bin(i)[2:]
        num = num.zfill(2**length_rude)
        # 参数清空
        unique_table.clear()
        rude.clear()
        q_Node.queue.clear()
        get_rude(num)
        if get_GOE() == 1:
            save_txt.append(num)
    time_end = time.time()
    # 输出到txt文件中
    with open(str(2**(2**length_rude)) + '_result_loop_ours.txt', 'w') as f:
        for num in save_txt:
            f.write(num)
            f.write('：对于任意有限CA都是成立的')
            f.write('\n')
        f.write("总计" + str(len(save_txt)) + '条规则！\n')
        f.write("执行时间为：" + str(time_end - time_start) + 's')

    
    
