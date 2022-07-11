'''
陈伟霖
2022年6月30日
本代码是用于求GOE是否存在，如果存在则找到没有原像的配置(层次)
目前没有实现图形化功能
'''
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
#最终结果
results = []
# 遍历队列
q_Node = Queue(maxsize=0)
# 结果队列
q_result = Queue(maxsize=0)
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

# 函数功能：找结点的值
# values：当前结点的值
# id：要走的状态
def get_Node(values,id):
    global rude
    new_values = []
    for value in values:
        value = value[1:]
        temp = value + '0'
        if (temp in rude.keys()) and rude[temp] == str(id):
            new_values.append(temp)
        temp = value + '1'
        if (temp in rude.keys()) and rude[temp] == str(id):
            new_values.append(temp)
    # 删除列表中重复元素
    new_values = list(set(new_values))
    return new_values

#递归函数
# values存的是当前结点的值
# id是当前结点是何种状态
# result记录当前路径上的值（如果是终止结点，则将GOE结果返回到全局变量results中）
def get_GOE():
    global q_Node,q_result,results
    length = q_Node.qsize()
    if length == 0:
        return -1
    for i in range(length):
        values = q_Node.get()
        result = q_result.get()
        # 检查是否为空结点
        if len(values) == 0:
            results.append(result)
            continue
        # 检查当前结点是否已经出现过
        Value_temp = sorted(values)
        str_value = "".join(Value_temp)
        if str_value in unique_table.keys():
            # 已经出现过该结点,则函数结束
            continue
        unique_table[str_value] = '0'
        # 没有出现过，往下走
        # 走0
        new_values = get_Node(values,0)
        q_Node.put(new_values)
        q_result.put(result+"0")
        # 走1
        new_values = get_Node(values,1)
        q_Node.put(new_values)
        q_result.put(result+"1")
    get_GOE()
    return -1 

#主函数
if __name__ == '__main__':
    # get_rude('00101011')
    # # get_rude('01110100')
    # q_Node.put(rudes)
    # q_result.put("")
    # get_GOE()
    # if len(results) == 0:
    #     print('不存在GOE')
    # else:
    #     print('存在GOE，且结果为：',results)
    # -------------------------------------------------------------------------------
    # 跑256
    save_txt = {}
    for i in range(0,256):
        num = bin(i)[2:]
        num = num.zfill(8)
        # 参数清空
        results.clear()
        unique_table.clear()
        rude.clear()
        rudes.clear()
        get_rude(num)
        q_Node.queue.clear()
        q_result.queue.clear()
        q_Node.put(rudes)
        q_result.put("")
        get_GOE()
        save_txt[num] = results.copy()
        
    # 输出到txt文件中
    with open('256_result.txt', 'w') as f:
        for key, value in save_txt.items():
            f.write(key)
            f.write(': ')
            f.write(str(value))
            f.write('\n')


    
    
