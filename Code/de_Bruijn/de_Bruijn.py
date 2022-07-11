'''
陈伟霖
2022年6月26日
本代码是用于模拟德布鲁因图寻找原像
'''
import numpy as np
# table:记录了图中的信息，采用矩阵的方式进行
table = np.array([
    [-1,-1,-1,-1],
    [-1,-1,-1,-1],
    [-1,-1,-1,-1],
    [-1,-1,-1,-1]
])
#记录结果
results = []
# 结点对应信息按照0:00,1:01,2:10,3:11
Node = ['00','01','10','11']
#规则初始化函数
def get_rude(simplify_rude):
    global table
    #字符串反转
    simplify_rude = simplify_rude[::-1]
    for i in range(0,8):
        table[int(i/2),i%4] = int(simplify_rude[i])
# 寻找原像的函数
# 其中id是当前结点的编号
# configuration是当前需要处理的配置
# original得到的原像
def find_Original(id,configuration,original):
    global table,Node
    if len(configuration) == 0:
        #print("计算得到的原像为：" + original)
        # if original[0] == '0' and original[-1] == '0':
        #     results.append(original)
        if original[0:2] == original[-2:]:
            results.append(original)
        # results.append(original)
        return 0
    for i in range(0,4):
        if table[id,i] == int(configuration[0]):
            find_Original(i,configuration[1:],original + Node[i][1])
if __name__ == '__main__':
    rude = "10010110"
    get_rude(rude)
    #length = 5
    with open('./de_Bruijin/' + rude + '_1-10' +'.txt', 'w') as f:
        for length in range(1,10):
            for k in range(0,2**length):
                num = bin(k)[2:]
                configuration = num.zfill(length)
                # 参数清空
                results.clear()
                for i in range(0,4):
                    find_Original(i,configuration,Node[i])       
                f.write(configuration + '的原像为：')
                f.write(str(results))
                f.write('\n')

    # configuration = '001000'
    # for i in range(0,4):
    #     find_Original(i,configuration,Node[i])


    