'''
陈伟霖
2022年6月30日
本代码是用于求GOE是否存在，如果存在则找到没有原像的配置(层次)
目前没有实现图形化功能
'''
import re
from turtle import st
import numpy as np
from queue import Queue
#全局数据
#字典，用来判断结点内容是否是唯一的，如果出现过则停止
#结点内容->0
unique_table = {}
#规则关系
# 组合->状态
rude = {}
# 遍历队列
q_Node = Queue(maxsize=0)
# 结果队列
q_result = Queue(maxsize=0)
#规则初始化函数
def get_rude(simplify_rude):
    global rude,q_result,q_Node
    #字符串反转
    rude_one = []
    rude_zero = []
    simplify_rude = simplify_rude[::-1]
    for i in range(0,8):
        num = bin(i)[2:]
        num = num.zfill(3)
        if simplify_rude[i] == '1':
            rude_one.append(num)
        else:
            rude_zero.append(num)
        rude[num] = simplify_rude[i]
    q_Node.put(rude_zero)
    q_Node.put(rude_one)
    q_result.put(rude_zero)
    q_result.put(rude_one)

# 函数功能：得到下一个结点的各种信息，包括结点的内容以及原像
# values：当前结点的原像值
# id：要走的状态
def get_Node(values,id):
    global rude
    new_values = []
    new_nodes = []
    for value in values:
        temp_value = value[-2:]
        temp = temp_value + '0'
        if (temp in rude.keys()) and rude[temp] == str(id):
            new_nodes.append(temp)
            new_values.append(value + '0')
        temp = temp_value + '1'
        if (temp in rude.keys()) and rude[temp] == str(id):
            new_nodes.append(temp)
            new_values.append(value + '1')
    # 删除列表中重复元素
    new_nodes = list(set(new_nodes))
    new_values = list(set(new_values))
    return new_values,new_nodes

#递归函数
# values存的是当前结点的值
# id是当前结点是何种状态
# result记录当前路径上的值（如果是终止结点，则将GOE结果返回到全局变量results中）
def get_GOE():
    global q_Node,q_result
    length = q_Node.qsize()
    if length == 0:
        return 1
    for i in range(length):
        node = q_Node.get()
        values = q_result.get()
        # 检查是否为空结点
        if len(node) == 0:
            return -1
        # 检查结点是否符合规范
        if len(values[0])>3:
            have_same = False
            for value in values:
                if value[0:2] == value[-2:]:
                    have_same = True
                    break
            if have_same == False:
                return -1
        # 存储原像首位的映射关系
        relat = {}
        for value in values:
            if value[:2] in relat.keys():
                if value[-2:] not in relat[value[:2]]:
                    relat[value[:2]].append(value[-2:])
            else:
                relat[value[:2]] = [value[-2:]]
        # 检查当前结点是否已经出现过
        Node_temp = sorted(node)
        str_Node = "".join(Node_temp)
        if str_Node in unique_table.keys():
            if relat in unique_table[str_Node]:
                # 已经出现过该结点,则函数结束
                continue
            else:
                unique_table[str_Node].append(relat)
        else:
            unique_table[str_Node] = [relat]
        # 没有出现过，往下走
        # 走0
        new_values,new_nodes = get_Node(values,0)
        q_Node.put(new_nodes)
        q_result.put(new_values)
        # 走1
        new_values,new_nodes = get_Node(values,1)
        q_Node.put(new_nodes)
        q_result.put(new_values)
    return get_GOE()

#主函数
if __name__ == '__main__':
    get_rude('00001111')
    # get_rude('01110100')
    print(get_GOE())
    
    # -------------------------------------------------------------------------------
    # # 跑256
    # save_txt = []
    # for i in range(0,256):
    #     num = bin(i)[2:]
    #     num = num.zfill(8)
    #     # 参数清空
    #     unique_table.clear()
    #     rude.clear()
    #     q_Node.queue.clear()
    #     q_result.queue.clear()
    #     get_rude(num)
    #     if get_GOE() == 1:
    #         save_txt.append(num)
        
    # # 输出到txt文件中
    # with open('256_result_loop.txt', 'w') as f:
    #     for num in save_txt:
    #         f.write(num)
    #         f.write('：对于任意有限CA都是成立的')
    #         f.write('\n')

    
    
