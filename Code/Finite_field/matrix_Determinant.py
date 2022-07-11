
'''
陈伟霖
2022年6月12日
本代码是用于求矩阵的行列式，并且是在有限域上进行求解
使用的算法为代数余子式
'''
import numpy as np
import galois
#计算矩阵的秩的函数
#其中data为数组数据，p为有限域的阶
def Deter_m(data,p):
    #创建一个有限域,后续计算在该有限域上进行
    GF = galois.GF(p**1)
    # 数据备份
    Matrix_orl = data.copy()
    #列数
    cols = len(data[0])
    #特殊情况特殊处理
    if cols == 1:
        return data[0,0]
    if cols == 2 :
        Matrix = GF(data)
        return Matrix[0,0] * Matrix[1,1] - Matrix[0,1] * Matrix[1,0]
    #初始化参数
    col = 0
    result = GF(0)
    while col < cols:
        if(data[0,col] != 0):
            Matrix = np.delete(data,0,0)
            Matrix = np.delete(Matrix,col,1)
            #print(Matrix)
            #print(data[0,col])
            result = result + ( GF(data[0,col])* (-1)**(0 + col) * Deter_m(Matrix,p) )
            data = Matrix_orl.copy() 
        col = col + 1
    return result

if __name__ == '__main__':
    data = np.array([[1,0,1,0,1,1],
                    [0,0,0,1,0,1],
                    [0 ,0 ,0, 0, 0, 0],
                    [1,0,1, 0, 1, 1],
                    [1, 1, 0 ,0, 1, 1 ],
                    [0 ,0 ,0, 0, 1 ,0 ]])
    print(Deter_m(data,2))
    #print(np.linalg.det(data))
            

            
                    


