# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 14:02:18 2021

@author: Xcz
"""
# %%
# from __future__ import division 
# #控制台 初始化时，设置了 会加载 这部分语句，但 .py 文件不会，所以得 额外 提前声明一下
# from sympy import *
# x, y, z, t = symbols('x y z t')
# k, m, n = symbols('k m n', integer=True)
# f, g, h = symbols('f g h', cls=Function)
# init_printing(use_latex='svg')

import os
import numpy as np
import math
from matplotlib import pyplot as plt
import cv2
from PIL import Image
import gc
import time
import inspect

Image.MAX_IMAGE_PIXELS = 10E10  # Image 的 默认参数 无法处理那么大的图片


def CGH_grating(l=1, structure_xy_mode="x",
                m_x=-1, T_x=10, Duty_Cycle_x=0.5,
                m_y=-1, T_y=10, Duty_Cycle_y=0.5,
                # %%
                size_pattern=100, size_PerPixel=0.1,
                is_transverse=0, is_positive=1, is_transparent=1,
                is_reverse=0, **kwargs):
    # l = 1
    # T_x = 10 # unit: um
    # m_x = -1
    # size_pattern = 8.5 * T_x # unit: um 如果 只是 示意图，填 10 或 8.5 倍 的 周期 T_x 左右，即 8.5 * T_x 即可
    # size_PerPixel = 0.1 # unit: um / pixel，分辨率
    # is_transverse = 0 # 如果 要生成 tif 文件，则需要 转置 is_transverse = 1；否则 若想看 正向，则 不转置
    # is_positive = 1
    # is_transparent = 1 # is_transparent = 0 是指 不论黑白 都保留 不透明
    # Duty_Cycle_x = 0.5 # -1 ~ 1，正表示 is_positive 片 中 黑色 (R,G,B,A) = (0,0,0,1) 调制（畴反转，chi_2 < 0）区域 占空比 更小
    # 0.5 意味着 1/3 占空比， -0.5 意味着 2/3 占空比 

    def image_border(src, dst, loc='a', width=3, color=(0, 0, 0, 255)):
        '''
        src: (str) 需要加边框的图片路径
        dst: (str) 加边框的图片保存路径
        loc: (str) 边框添加的位置, 默认是'a'(
            四周: 'a' or 'all'
            上: 't' or 'top'
            右: 'r' or 'rigth'
            下: 'b' or 'bottom'
            左: 'l' or 'left'
        )
        width: (int) 边框宽度 (默认是3)
        color: (int or 3-tuple) 边框颜色 (默认是0, 表示黑色; 也可以设置为三元组表示RGB颜色)
        '''
        # 读取图片
        img_ori = Image.open(src)
        w = img_ori.size[0]
        h = img_ori.size[1]

        # 添加边框
        if loc in ['a', 'all']:
            w += 2 * width
            h += 2 * width
            img_new = Image.new('RGBA', (w, h), color)
            img_new.paste(img_ori, (width, width))
        elif loc in ['t', 'top']:
            h += width
            img_new = Image.new('RGBA', (w, h), color)
            img_new.paste(img_ori, (0, width, w, h))
        elif loc in ['r', 'right']:
            w += width
            img_new = Image.new('RGBA', (w, h), color)
            img_new.paste(img_ori, (0, 0, w - width, h))
        elif loc in ['b', 'bottom']:
            h += width
            img_new = Image.new('RGBA', (w, h), color)
            img_new.paste(img_ori, (0, 0, w, h - width))
        elif loc in ['l', 'left']:
            w += width
            img_new = Image.new('RGBA', (w, h), color)
            img_new.paste(img_ori, (width, 0, w, h))
        else:
            pass

        # 保存图片
        img_new.save(dst)

    # def hello():
    #     print("hello world")
    # hello()

    # expr=(x+y)**3
    # print(expr)
    # print(expr.expand())
    # expr
    # expr.expand()

    # img = cv2.imread(r'D:\Users\ZML\Desktop\Grating.png', 0) # 按绝对路径读取图片

    def step(U, Duty_Cycle):
        return (U > (2 * is_positive - 1) * np.cos(Duty_Cycle * np.pi)).astype(np.int8())

    # 如果 不是 is_positive == 1，则 negative == 1 ， 则 需要用到 如下 reverse 函数
    # is_transparent == 1 也会用到 以下 透明度 反转 函数
    def reverse(x):
        return np.array(x == 0, dtype=np.uint8()) * 255
        # if x != 0:
        #     return 0
        # else:
        #     return 255

    # %%
    # 生成二值测试图像

    G_x = 2 * math.pi * m_x / T_x  # unit: /um
    G_y = 2 * math.pi * m_y / T_y  # unit: /um

    size_pattern_y = size_pattern  # unit: um
    size_pattern_x = kwargs.get("size_pattern_y", size_pattern)  # unit: um

    size_PerPixel_y = size_PerPixel  # unit: um / pixel，横向分辨率
    size_PerPixel_x = size_PerPixel  # unit: um / pixel，纵向分辨率

    width_y = int(size_pattern_y / size_PerPixel_y)  # 横向 像素点个数
    hight_x = int(size_pattern_x / size_PerPixel_x)  # 纵向 像素点个数

    # if is_transverse == 1:
    #     width_y, hight_x = hight_x, width_y

    array_yx = np.ones((hight_x, width_y, 4), dtype='uint8')  # 整体定义，不需要大量内存
    # array_yx = np.zeros((width_y,hight_x),dtype='float32') # 整体定义，需要大量内存

    array_yx = array_yx * 255  # RGB = 255,255,255，白色，全区域，均不调制；（这里可以 不初始化 RGB）
    # 不透明度 alpha = 255，完全显示 RGB 三色

    center_y = width_y // 2
    center_x = hight_x // 2
    # %%
    tick_start = time.time()
    
    X, Y = np.meshgrid([i for i in range(width_y)], [j for j in range(hight_x)])
    center_x = center_x if is_transverse == 1 else - center_x
    Mesh_centered = np.dstack((X, Y)) - (center_y, center_x)
    y_relative = Mesh_centered[:, :, 0] * size_PerPixel_y  # unit: um
    x_relative = Mesh_centered[:, :, 1] * size_PerPixel_x  # unit: um
    del X, Y, Mesh_centered
    gc.collect()
    # %%
    OAM_phase = l * (np.arctan2(x_relative, y_relative) + math.pi) if l != 0 else 0
    if structure_xy_mode == 'x':
        CGH = step(np.cos(G_x * y_relative - OAM_phase), Duty_Cycle_x)
    elif structure_xy_mode == 'y':
        CGH = step(np.cos(G_y * x_relative - OAM_phase), Duty_Cycle_y)
    elif structure_xy_mode == 'xy':
        CGH = step(np.cos(G_x * y_relative + G_y * x_relative - OAM_phase), Duty_Cycle_x)
    elif structure_xy_mode == 'x+y' or structure_xy_mode == 'x*y':
        CGH_x = step(np.cos(G_x * y_relative - OAM_phase), Duty_Cycle_x)
        CGH_y = step(np.cos(G_y * x_relative - OAM_phase), Duty_Cycle_y)
        if structure_xy_mode == 'x*y':
            CGH = CGH_x * CGH_y
        else:
            CGH = np.mod(CGH_x + CGH_y, 2)
        del CGH_x, CGH_y
        gc.collect()
    del x_relative, y_relative
    gc.collect()
    RGBs = np.uint8(CGH * 255)
    del CGH
    gc.collect()
    # RGBs = RGBs.T
    # %%
    for k in range(3):
        array_yx[:, :, k] = RGBs
    array_yx = array_yx.transpose(1, 0, 2) if is_transverse == 1 else array_yx
    del RGBs
    gc.collect()
    # %%
    array_yx = 255 - array_yx
    if is_reverse == 1:  # 如果 黑白 反转
        array_yx = 255 - array_yx

    if is_transparent == 1:  # 如果 想把 白色 弄成 透明的
        array_yx[:, :, 3] = reverse(array_yx[:, :, 0])
    else:
        if is_transverse == 0:  # 全都 不透明
            array_yx[:, :, 3] = np.ones((hight_x, width_y), dtype='uint8') * 255
        else:
            array_yx[:, :, 3] = np.ones((width_y, hight_x), dtype='uint8') * 255
        # for i in range(width_y):
        #     for j in range(hight_x):
        #         array_yx[j, i, 3] = reverse(array_yx[j, i, 0]) # 若 白 (RGB = 255) ，则 透明 (A = 0)；
        #                                                        # 否则 若 黑 (RGB = 0) ，则 不透明 (A = 255)
    # print(array_yx[:, :, 3])
    
    print("{} a.1. --> consume time: {} s".format(inspect.stack()[1][3], time.time() - tick_start))
    # %%
    # 绘图
    tick_start = time.time()
    
    is_plot = kwargs.get("is_plot", 0)

    # if is_plot >= 0:

    dpi = 100
    size_fig_y = array_yx.shape[1] / dpi
    size_fig_x = array_yx.shape[0] / dpi

    plt.figure(figsize=(size_fig_y, size_fig_x), dpi=dpi)
    # 图中图的大底板图，长=10英寸，宽=10英寸，每英寸300像素，共3000*3000像素

    plt.axis('off')  # 去掉 外侧 框线
    # plt.xticks([])  # 去掉 横坐标值
    # plt.yticks([])  # 去掉 纵坐标值
    # plt.gca().xaxis.set_major_locator(plt.NullLocator())
    # plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)

    plt.imshow(array_yx)
    # plt.imshow(array_yx, 'gray')
    # plt.imshow(array_yxl_cos_step[l], 'gray'), \
    #     plt.title("pattern_yx, l = %s" % (l), fontsize = 10)

    # image_yx = Image.fromarray(array_yx)
    # is_transparent = image_yx.convert('RGBA')

    # location = r'D:\Users\ZML\Desktop'
    location = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(location + "\\Grating.svg", transparent=True, pad_inches=0)
    plt.savefig(location + "\\Grating.png", transparent=True, pad_inches=0)  # dpi=100 和上文相对应 pixel尺寸/dpi=inch尺寸
    # cv2.imencode('.png', array_xy)[1].tofile(location)

    plt.show()  # 此处顺序不能弄反 imshow(),savefig(),show()
    # plt.clf()                  #plt.clf()的作用：用于批量存储图片时 每一次显示图片并保存以后，释放图窗，接受下一个图片显示和存储

    image_border(location + "\\Grating.png", location + "\\Grating.png", loc='a', width=10, color=(255, 255, 255, 0))

    # test = cv2.imread(location + "\\test.png", -1) # 按绝对路径 以及 'RGBA' 格式 全保真 地 读取图片
    print("{} a.2. --> consume time: {} s".format(inspect.stack()[1][3], time.time() - tick_start))

if __name__ == '__main__':
    kwargs = \
        {"l": 0, "structure_xy_mode": 'x',
         "m_x": -1, "T_x": 6, "Duty_Cycle_x": 0.5,
         "m_y": -1, "T_y": 6, "Duty_Cycle_y": 0.5,
         # %%
         "size_pattern": 500, "size_PerPixel": 1,
         "size_pattern_y": 1800,  # size_pattern / size_PerPixel = 65536 = 2 ^ 16 是上限
         # %%
         "is_transverse": 1, "is_positive": 1, "is_transparent": 1,
         "is_reverse": 1,
         # %%
         "is_plot": 1,
         }

    CGH_grating(**kwargs)
