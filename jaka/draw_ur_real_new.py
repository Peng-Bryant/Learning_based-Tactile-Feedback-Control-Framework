import numpy as np
import copy
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import matplotlib as mpl
import math as m
import cv2
from scipy.interpolate import interp1d

sns.set()

for q in range(3,4):
    input_txt_o1 = './draw/push/real/obj_path'+str(q)+'.txt'
    input_txt_g = './draw/push/real/path'+str(q)+'.txt'
    input_txt_o = './draw/drawing/real/real/input_txt_o.txt'

    print(q)

    x_o = []
    y_o = []
    rz_o = []
    x_g = []
    y_g = []
    rz_g = []
    a = 70
    s = 0

    f = open(input_txt_o)
    g = open(input_txt_g)


    with open(input_txt_o1, mode='r', encoding='utf-8') as h:
        line = h.readlines()  # 读取文件
        try:
            line = line[1:]  # 只读取第一行之后的内容
            h = open(input_txt_o, mode='w', encoding='utf-8')  # 以写入的形式打开txt文件
            h.writelines(line)    # 将修改后的文本内容写入
            h.close()             # 关闭文件
        except:
            pass


    for line in f:
        line = line.strip('\n')
        line = line.split(' ')

        x_o.append(1000*float(line[0]))
        y_o.append(1000*float(line[1]))
        rz_o.append(float(line[5]))
    f.close

    for line in g:
        line = line.strip('\n')
        line = line.split(' ')

        x_g.append(1000*float(line[0]))
        y_g.append(1000*float(line[1]))
        rz_g.append(float(line[5]))
        
    f.close

    x_o = np.array(x_o)
    goal_pred = interp1d(x_g,y_g,kind='cubic', fill_value='extrapolate')
    x_pred = x_o
    y_pred = goal_pred(x_pred)
    # print((np.max(y_o)-np.min(y_o)))

    # n is related to the color of the error, changeable
    # n = (np.max(y_o)-np.min(y_o))/2.5
    n = 0.03*1000
    r = rz_o[0]
    # print(n)
    # x_a = (x_o[0]+x_o[1])/2
    # y_a = goal_pred(x_a)
    # theta_a = m.atan((y_pred[1]-y_a)/(x_pred[1]-x_a))
    # co_a = (abs(y_o[1]-y_pred[1])/n+abs(y_o[0]-y_pred[0])/n)/2
    # rect2 = mp.Rectangle(((x_a-(m.sqrt(2)/2*a*m.sin(m.pi/4-theta_a/180*m.pi))), (y_a-m.sqrt(2)/2*a*m.cos(m.pi/4-theta_a/180*m.pi))), a, a, color=(co_a,0,0), alpha=0.5, angle=theta_a)
    # plt.gca().add_patch(rect2)

    for i in range (len(rz_o)-1):
        if(i ==0):
            co = 0
        else:
            if (abs(y_o[i]-y_pred[i])<=n):
                co = abs(y_o[i]-y_pred[i])/n*1
            else:
                co = 1
        s = s+abs(y_o[i]-y_pred[i])
        # for 15 and 18
        theta_p = m.atan((y_pred[i+1]-y_pred[i])/(x_pred[i+1]-x_pred[i]))
        if(i == 0):
            theta = 0
        else:
            if(i==1):
                theta = ((rz_o[i]-r)*180/m.pi+theta_p*180/m.pi)/4
                # co = 1
            else:
                theta = ((rz_o[i]-r)*180/m.pi+theta_p*180/m.pi)/2
           
        rect1 = mp.Rectangle(((x_o[i]-(m.sqrt(2)/2*a*m.sin(m.pi/4-theta/180*m.pi))), (y_o[i]-m.sqrt(2)/2*a*m.cos(m.pi/4-theta/180*m.pi))), a, a, color=(co,0,0), alpha=0.5, angle=theta)
        
        angle=(rz_o[i]-r)*180/m.pi
        # print(angle)
        plt.gca().add_patch(rect1)
        
        plt.scatter(x_o[i], y_o[i], c='g', marker='o')  # 点

    # 0 1 2 3 4 5 6 7 8
    # 0   1   2   3   4
    for i in range (len(x_g)-1):
        # theta = m.atan((y_pred[2*i+1]-y_pred[2*i])/(x_pred[2*i+1]-x_pred[2*i]))
        theta = m.atan((y_g[i+1]-y_g[i])/(x_g[i+1]-x_g[i]))
        plt.arrow(x_g[i], y_g[i], 15*m.cos(theta), 15*m.sin(theta), width=1,
                facecolor='#00FF00',edgecolor='#00FF00',
                length_includes_head=True
            )
        plt.arrow(x_g[i], y_g[i], 15*m.cos((m.pi/2+theta)), 15*m.sin((m.pi/2+theta)), width=1,
                facecolor='#FF0000',edgecolor='#FF0000',
                length_includes_head=True
            )
        plt.scatter(x_g[i], y_g[i], c='b', marker='.')  # 点

    avr = s/len(x_o)
    print('The average error is:',avr)

    # plt.scatter(x_g[], y_g, c='b', marker='.')  # 点
    # plt.scatter(x_o, y_o, c='g', marker='o')  # 点

    plt.xticks(np.linspace(-50, 450, 11))
    plt.yticks(np.linspace(-150, 150, 7))
    #plt.yticks(np.arange(-200, 150, 50))	# 在绘制9_obj_path时使用此范围

    ax=plt.gca()

    plt.xlabel("x position (mm)")
    plt.ylabel("y position (mm)")
    # plt.axis("equal")
    plt.tick_params(axis="both")
    ax.set_aspect('equal') #x轴y轴等比例

    # colorbar cmap
    from matplotlib.colors import ListedColormap,LinearSegmentedColormap

    N = 256
    vals = np.ones((N, 4))
    vals[:, 0] = np.linspace(0, 1, N)
    vals[:, 1] = np.linspace(0, 0, N)
    vals[:, 2] = np.linspace(0, 0, N)
    newcmp = ListedColormap(vals)


    
    # change scale 0-1 to 0-n
    norm = mpl.colors.Normalize(vmin=0, vmax=n) 
    scale = plt.cm.ScalarMappable(norm=norm,cmap = newcmp) 
    scale.set_array([]) 
    cb = plt.colorbar(scale,fraction=0.03,ax=plt.gca()) 
    cb.set_label('Error(mm)', fontsize=12)

    plt.savefig('./draw/push/real/'+str(q)+'_rec.png')
    plt.close()
    # plt.show()
