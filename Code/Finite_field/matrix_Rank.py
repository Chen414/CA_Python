
'''
陈伟霖
2022年6月12日
本代码是用于求矩阵的秩，并且是在有限域上进行求解
使用的算法为行阶梯式
'''
import numpy as np
import galois
#计算矩阵的秩的函数
#其中data为数组数据，p为有限域的阶
def rank_m(data,p):
    #创建一个有限域,后续计算在该有限域上进行
    GF = galois.GF(p**1)
    # 数据类型转换
    Matrix = GF(data)
    #行数
    rows = len(data)
    #列数
    cols = len(data[0])
    #初始化参数
    row = 0
    col = 0
    while row < rows and col < cols:
        #如果下一个位置上元素为0
        #则将下面的行加上来，除非全为零
        #如果全为0，则处理下一列
        if(Matrix[row,col] == 0):
            column_zero = True
            for k in range(row+1,rows):
                if(Matrix[k,col] != 0):
                    Matrix[row] = Matrix[row] + Matrix[k]
                    column_zero = False
                    break
            if column_zero == True:
                # 列向后移动，行不变
                col = col + 1
                continue
        #用第row行，将余下所有行的第col列都消去
        for k in range(row+1,rows):
            if(Matrix[k,col] == 0):
                #该行不用处理
                continue
            #计算它们之间的倍数
            temp = Matrix[k,col]/Matrix[row,col]
            Matrix[k] = Matrix[k] - GF(temp) * Matrix[row]
        row =row + 1
        col = col + 1
    return row

if __name__ == '__main__':
    data = np.array([[1, 0, 1, 0, 1 ,1 ,0 ,0],
                    [0 ,1 ,0, 1, 0 ,0 ,0, 0],
                    [0, 0 ,1 ,0, 1, 0 ,1 ,1],
                    [1 ,1 ,0 ,0 ,1, 1, 0, 0],
                    [0 ,0 ,1 ,0 ,1 ,0 ,1, 1],
                    [0 ,0 ,1, 1, 1, 0, 0, 0],
                    [1 ,0, 1 ,1, 1, 0 ,1, 0],
                    [1 ,1, 1, 0, 1 ,1 ,0, 0]])
    print(rank_m(data,2))
            

            
                    


