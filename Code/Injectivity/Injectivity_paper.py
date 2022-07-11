'''
陈伟霖
2022年7月4日
该代码是实现论文中对单射规则的判断
实现了规则长度接口，可以直接修改length_rude的值实现对不同长度规则进行计算
目前没有实现图形化功能
'''
# 全局规则函数，例如:'0000':'0'
from ftplib import all_errors
import time
from ast import For, Or
from operator import length_hint
from turtle import Turtle, update
# 规则长度
length_rude = 3
rude = {}
# 对规则进行分类
class_rude = {}
# 对表格进行分类，普通格、圈叉格、叉格
# 普通格
Ordinary_box = {}
# 圈叉格
Circle_box = {}
# 叉格
Fork_box = {}

#规则初始化函数
def get_rude(simplify_rude):
    global rude,class_rude,length_rude
    #字符串反转
    simplify_rude = simplify_rude[::-1]
    # 用于判断是否平衡
    num_one = 0
    for i in range(0,2**length_rude):
        num = bin(i)[2:]
        num = num.zfill(length_rude)
        rude[num] = simplify_rude[i]
        if simplify_rude[i] == '1':
            num_one = num_one + 1
        if simplify_rude[i] not in class_rude.keys():
            class_rude[simplify_rude[i]] = [i]
        else:
            class_rude[simplify_rude[i]].append(i)
    if num_one != (2**length_rude)/2:
        return -1
    return get_box()
# 构造后续序列，这里可以判断是否单射，所以需要返回值
def get_sequent(a,b):
    global Ordinary_box,Circle_box,Fork_box,rude,length_rude
    # 首先判断后三位是否相同，如果相同则有可能进去 “圈叉”
    bin_a = bin(a)[2:].zfill(length_rude)
    bin_b = bin(b)[2:].zfill(length_rude)
    if bin_a[1:] == bin_b[1:]:
        temp = bin_a[1:]
        if rude[temp + '0'] == rude[temp + '1']:
            if str((a%8)*2) + '-' + str(((a%8)*2) +1) == str(a) + '-' + str(b):
                return -1
            Circle_box[str(a) + '-' + str(b)] = [str((a%8)*2) + '-' + str(((a%8)*2) +1),'@']
        else:
            Fork_box[str(a) + '-' + str(b)] = []
    else:
        # 正常流程
        temp_a = bin_a[1:]
        temp_b = bin_b[1:]
        ten_a = int(temp_a + '0',2)
        ten_b = int(temp_b + '0',2)
        # 判断是否是第一个
        is_Ori = False
        if rude[temp_a + '0'] == rude[temp_b + '0']:
            is_Ori = True
            t_a = ten_a
            t_b = ten_b
            entry = str(t_a) + '-' + str(t_b) if t_a<t_b else str(t_b) + '-' + str(t_a)
            if entry == str(a) + '-' + str(b):
                return -1
            Ordinary_box[str(a) + '-' + str(b)] = [entry]
        if rude[temp_a + '0'] == rude[temp_b + '1']:
            t_a = ten_a
            t_b = ten_b + 1
            entry = str(t_a) + '-' + str(t_b) if t_a<t_b else str(t_b) + '-' + str(t_a)
            if entry == str(a) + '-' + str(b):
                return -1
            if is_Ori:
                Ordinary_box[str(a) + '-' + str(b)].append(entry)
            else:
                is_Ori = True
                Ordinary_box[str(a) + '-' + str(b)] = [entry]
        if rude[temp_a + '1'] == rude[temp_b + '0']:
            t_a = ten_a + 1 
            t_b = ten_b
            entry = str(t_a) + '-' + str(t_b) if t_a<t_b else str(t_b) + '-' + str(t_a)
            if entry == str(a) + '-' + str(b):
                return -1
            if is_Ori:
                Ordinary_box[str(a) + '-' + str(b)].append(entry)       
            else:
                is_Ori = True
                Ordinary_box[str(a) + '-' + str(b)] = [entry] 
        if rude[temp_a + '1'] == rude[temp_b + '1']:
            t_a = ten_a + 1
            t_b = ten_b + 1
            entry = str(t_a) + '-' + str(t_b) if t_a<t_b else str(t_b) + '-' + str(t_a)
            if entry == str(a) + '-' + str(b):
                return -1
            if is_Ori:
                Ordinary_box[str(a) + '-' + str(b)].append(entry)     
            else:
                is_Ori = True
                Ordinary_box[str(a) + '-' + str(b)] = [entry]   
        if is_Ori == False:
            # 没有匹配的
            Fork_box[str(a) + '-' + str(b)] = []
        return 1
# 构造格子
def get_box():
    global class_rude
    for k in class_rude.keys():
        rudes = class_rude[k]
        length = len(rudes)
        for i in range(length):
            for j in range(i+1,length):
                get_sequent(rudes[i],rudes[j])
# 更新格子信息
def update_box():
    global Ordinary_box,Circle_box,Fork_box
    # have_change用于判断是否需要继续迭代
    have_change = False
    for key in list(Ordinary_box.keys()):
        values = Ordinary_box[key]
        temp_value = values.copy()
        for value in temp_value:
            if value in Fork_box.keys():
                values.remove(value)
        if len(values) == 0:
            have_change = True
            Ordinary_box.pop(key)
            Fork_box[key] = []
    for key in Circle_box.keys():
        value = Circle_box[key][0]
        if value in Fork_box.keys():
            Circle_box[key].remove(value)
    if have_change:
        update_box()
# 赋值权重，这里可以判断是否单射，所以需要返回值  
def get_weight(weights):
    global Ordinary_box,Circle_box
    # 权重 weights记录了已有权重的序对，初始：'@':0
    # have_change记录是否需要继续进行迭代
    have_change = False
    # 检查是否成功完成
    if len(weights) == len(Ordinary_box) + len(Circle_box) + 1:
        # print(weights)
        return 1
    for key in Circle_box.keys():
        if key in weights.keys():
            continue
        weight = 0
        # all_find用于判断是否都找到了
        all_find = True
        for value in Circle_box[key]:
            if value not in weights.keys():
                all_find = False
                break
            else:
                weight = max(weight,weights[value])
        if all_find:
            weight = weight + 1
            have_change = True
            weights[key] = weight
            
    for key in Ordinary_box.keys():
        if key in weights.keys():
            continue
        weight = 0
        # all_find用于判断是否都找到了
        all_find = True
        for value in Ordinary_box[key]:
            if value not in weights.keys():
                all_find = False
                break
            else:
                weight = max(weight,weights[value])
        if all_find:
            weight = weight + 1
            have_change = True
            weights[key] = weight
    
    if have_change:
        return get_weight(weights)
    else:
        return -1
# 最后一个判断点，同样需要返回参数
def final_decide():
    global Ordinary_box,Circle_box,length_rude
    Combinations = list(Ordinary_box.keys())
    Combinations.extend(list(Circle_box.keys()))
    for Combination in Combinations:
        key = str(Combination)
        a = int(key.split('-')[0])
        b = int(key.split('-')[1])
        bin_a = bin(a)[2:].zfill(length_rude)
        bin_b = bin(b)[2:].zfill(length_rude)
        if bin_a[:length_rude-1] == bin_b[:length_rude-1]:
            return -1
    return 1
        
if __name__ == '__main__':
    
    # if get_rude('1111000010110100') == -1:
    #     print('不是单射')
    # update_box()
    # if get_weight({'@':0}) == -1 or final_decide() == -1:
    #     print('不是单射')
    # print('满足单射')
    #print(Circle_box)
    # --------------------------------------------------------------------------------
    # 跑规则长度为4
    save_txt = []
    time_start = time.time()
    all_nums = 2**(2**length_rude)
    length_num = 2**length_rude
    for i in range(0,all_nums):
        num = bin(i)[2:]
        num = num.zfill(length_num)
        # 参数清空
        rude.clear()
        class_rude.clear()
        Ordinary_box.clear()
        Fork_box.clear()
        Circle_box.clear()
        if get_rude(num) == -1:
            continue
        update_box()
        if get_weight({'@':0}) == -1 or final_decide() == -1:
            continue
        save_txt.append(num)
    time_end = time.time()
    # 输出到txt文件中
    with open( str(all_nums) + '_result_Injectivity_paper.txt', 'w') as f:
        for key in save_txt:
            f.write(key)
            f.write(' 是满足单射的')
            f.write('\n')
        f.write("总计" + str(len(save_txt)) + '条规则\n')
        f.write('程序运行的时间为：' + str(time_end-time_start) + 's')

