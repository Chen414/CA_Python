'''
陈伟霖
2022年7月17日
本代码是复现老板论文中的代码功能【Reversibility of general 1D linear cellular automata】
代码功能是找到某个LCA规则中的周期是多少，并且判断某一个长度的细胞是否是可逆的
目前没有实现图形化功能
'''
# 全局变量，用于存储LCA规则
LCA = ''
# 全局变量，用于存储最终的周期结果
Period = 0
# 全局变量，用于存储可逆的模余数
Reversible = []
# 初始结点
Initial_Node = []
# 初始化参数函数
def init(lca):
    global LCA,Initial_Node,Reversible
    LCA = lca
    length = len(lca)
    Reversible.append(0)
    R_r = int(length/2)
    R_l = length - 1 - R_r
    for i in range(2**R_r):
        temp = '0'*R_l + bin(i)[2:].zfill(R_r)
        Initial_Node.append(temp)
    
# 通过LCA得到映射结果
def f(rude):
    global LCA
    length = len(LCA)
    sum = 0
    for i in range(length):
        sum = sum + int(LCA[i]) * int(rude[i])
    return sum%2

# 构造结点，得到结果
def get_Node(values,n):
    global Initial_Node,Reversible,Period
    if values == Initial_Node and n != 0:
        Period = n
        Reversible.pop()
        return 0
    else:
        n = n + 1
    result = []
    unique = []
    for value in values:
        if f(value + '0') == 0:
            result.append(value[1:] + '0')
            unique.append(value[-1] + '0')
        else:
            result.append(value[1:] + '1')
            unique.append(value[-1] + '1')
    
    unique_set = list(set(unique))
    if len(unique) == len(unique_set):
        Reversible.append(n)
    return get_Node(result,n)

# 检验某个长度是否可逆
def check_Reversible(n):
    global Period,Reversible
    num = n % Period
    if num in Reversible:
        print('长度为' + str(n) + '的线性细胞自动机是可逆的！')
    else:
        print('长度为' + str(n) + '的线性细胞自动机是不可逆的！')

if __name__ == '__main__':
    init('11011')
    get_Node(Initial_Node,0)
    check_Reversible(15)
    
    
    