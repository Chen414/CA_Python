'''
陈伟霖
2022年6月21日
本代码是用于找寻线性组合
y = k1 * x1 + k2 * x2 + k3 * x3 + k4
找到所有符合线性规则的序列，查看他们的GOE结果
'''
import numpy as np
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
def get_GOE(values,id,result):
    
    # 更新result
    result = result + str(id)
    # 首先判断是否为终止结点
    if len(values) == 0:
        results.append(result[1:])
        return 1
    # 检查当前结点是否已经出现过
    Value_temp = sorted(values)
    str_value = "".join(Value_temp)
    if str_value in unique_table.keys():
        # 已经出现过该结点,则函数结束
        return -1
    unique_table[str_value] = '0'
    # 没有出现过，往下走
    # 走0
    new_values = get_Node(values,0)
    get_GOE(new_values,0,result)
    # 走1
    new_values = get_Node(values,1)
    get_GOE(new_values,1,result)
    return -1 
if __name__ == '__main__':

    save_txt = {}
    save_can = {}
    # 一共有k1 k2 k3 k4四种，一共是2**4 = 16种
    # 找到每一种对应的规则
    for i in range(0,256):
        num = bin(i)[2:]
        num = num.zfill(8)
        # 参数清空
        results.clear()
        unique_table.clear()
        rude.clear()
        rudes.clear()
        # 创造对应的规则
        # simplify_rude = ""
        # for k in range(0,8):
        #     temp = bin(k)[2:]
        #     temp = temp.zfill(3)
        #     simplify_rude = str((int(num[0]) * int(temp[0]) + int(num[1]) * int(temp[1]) + int(num[2]) * int(temp[2]) + int(num[3]))%2) + simplify_rude
        if (int(num[0]) + int(num[2]) == 1) and (int(num[1]) + int(num[3]) == 1) and (int(num[4]) + int(num[6]) == 1) and (int(num[5]) + int(num[7]) == 1):
            get_rude(num)
            get_GOE(rudes,0,"")
            get_GOE(rudes,1,"")
            save_txt[num] = results.copy()
            #save_can[simplify_rude] = num
        

    # # 跑256
    # save_txt = {}
    # save_rude = {}
    # for i in range(0,256):
    #     num = bin(i)[2:]
    #     num = num.zfill(8)
    #     # 参数清空
    #     results.clear()
    #     unique_table.clear()
    #     rude.clear()
    #     rudes.clear()
    #     if get_rude_need(num):
    #         get_rude(num)
    #         get_GOE(rudes,0,"")
    #         get_GOE(rudes,1,"")
    #         save_txt[num] = results.copy()
    #         save_rude[num] = rude_one.copy()
        
    # # 输出到txt文件中
    number = 1
    with open('Solve.txt', 'w') as f:
        for key, value in save_txt.items():
            f.write('编号' + str(number) + '------')
            f.write(key + '是满足条件2的，其GOE结果为')
            f.write(': ')
            f.write(str(value))
            f.write('\n')
            number = number + 1


    