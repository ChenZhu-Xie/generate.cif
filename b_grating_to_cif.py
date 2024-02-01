# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 14:02:18 2021

@author: Xcz
"""
# %%
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure, data, color
import time
import inspect


def write_out_cif(context_core, location=os.path.dirname(os.path.abspath(__file__)),
                  file_name="Grating_appr_contours", is_txt=0, is_add_outline=1, ):
    context_front = \
        '''
        DS 1 2 40;\n
        9 Cell0;\n
        '''

    if context_core[:6] != "L CPG;":
        # print(context_core[:6])
        context_core = "L CPG;\n" + context_core

    context_back = \
        '''
        DF;\n
        E;\n
        '''

    with open("外框.txt", "r") as f:
        context_outline = f.read() if is_add_outline == 1 else ""

    context = context_front + context_core + context_outline + context_back

    suffix = ".txt" if is_txt == 1 else ".cif"
    path = location + "\\" + file_name + suffix
    with open(path, "w") as f:
        f.write(context)


def grating_to_cif(size_PerCIF_Unit=1 / 2000,
                   size_pattern=100, size_PerPixel=0.1,
                   # %%
                   is_transverse=0, is_positive=1, is_transparent=1,
                   is_reverse=0,
                   # %%
                   tolerance=0.02, linewidth=0.5, **kwargs):
    def reverse(x):
        return np.array(x == 0, dtype=np.uint8()) * 255

    size_pattern_y = size_pattern  # unit: um
    size_pattern_x = kwargs.get("size_pattern_y", size_pattern)  # unit: um

    if is_transverse == 1:
        size_pattern_x, size_pattern_y = size_pattern_y, size_pattern_x

    size_PerPixel_y = size_PerPixel  # unit: um / pixel，横向分辨率
    size_PerPixel_x = size_PerPixel  # unit: um / pixel，纵向分辨率

    width_y = int(size_pattern_y / size_PerPixel_y)  # 横向 像素点个数
    hight_x = int(size_pattern_x / size_PerPixel_x)  # 纵向 像素点个数

    CifUnits_PerPixel = size_PerPixel / size_PerCIF_Unit  # unit: cif_unit / pixel，打印 分辩率
    # %% 生成二值测试图像
    # img=color.rgb2gray(data.horse())
    # location = r'D:\Users\ZML\Desktop'
    location = os.path.dirname(os.path.abspath(__file__))
    img = cv2.imdecode(np.fromfile(location + "\\Grating.png", dtype=np.uint8), 0)  # 按 绝对路径 + 灰度图 读取图片
    # img = cv2.imread(location + "\\Grating.png", 0) # 按 绝对路径 + 灰度图 读取图片
    img = np.array(img, dtype=bool)  # 将 灰度图 转换为 布尔图

    # %% 检测所有图形的轮廓
    contours = measure.find_contours(img, 0.5)

    global appr_contours
    appr_contours = []
    # %%  单线程
    # tick_start = time.time()
    # for i in range(len(contours)):
    #     appr_contours.append(measure.approximate_polygon(contours[i], tolerance=tolerance))
    # print("{} b.1. --> consume time: {} s".format(inspect.stack()[1][3], time.time() - tick_start))
    # %%  多线程 begin
    def fun1(for_th, fors_num, *arg, **kkwargs, ):
        return measure.approximate_polygon(contours[for_th], tolerance=tolerance)

    def fun2(for_th, fors_num, appr_contour, *args, **kkwargs, ):
        global appr_contours
        appr_contours.append(appr_contour)

    from fun_thread import my_thread, noop
    my_thread(10, len(contours),
              fun1, fun2, noop,
              is_ordered=1, add_level=-1, **kwargs, )
    # %%

    is_plot = kwargs.get("is_plot", 0)

    if is_plot == 1:
        dpi = 100
        size_fig_y = width_y / dpi
        size_fig_x = hight_x / dpi
        # print(size_fig_x, size_fig_y)

        # 绘制轮廓
        fig, axes = plt.subplots(2, 2, figsize=(3 * size_fig_y, 3 * size_fig_x), dpi=dpi)
        ax0, ax1, ax2, ax3 = axes.ravel()

        ax0.imshow(img, plt.cm.gray)
        ax0.set_title('original image')

        rows, cols = img.shape
        # print(rows, cols)
        ax1.axis([0, cols, rows, 0])
        for n, contour in enumerate(contours):
            ax1.plot(contour[:, 1], contour[:, 0], linewidth=linewidth)
        # ax1.axis('image')
        ax1.set_title('contours')

        ax2.axis([0, cols, rows, 0])

    # %%
    global context_core
    context_core = ""
    # %% 单线程
    # tick_start = time.time()
    # for n, appr_contour in enumerate(appr_contours):
    #     # print(appr_contour[0][0])
    #     # print(len(appr_contour))
    #     context_core += "P"
    #     for i in range(len(appr_contour)):
    #         context_core += " " + str(int(appr_contour[-(i + 1)][0] * CifUnits_PerPixel)) \
    #                         + "," + str(int(appr_contour[-(i + 1)][1] * CifUnits_PerPixel))
    #     context_core += ";" + "\n"
    #     if is_plot == 1:
    #         ax2.plot(appr_contour[:, 1], appr_contour[:, 0], linewidth=linewidth)
    # print("{} b.2. --> consume time: {} s".format(inspect.stack()[1][3], time.time() - tick_start))
            
    def fun1(for_th, fors_num, *arg, **kkwargs, ):
        appr_contour = appr_contours[for_th]
        context_core_i = "P"
        for i in range(len(appr_contour)):
            context_core_i += " " + str(int(appr_contour[-(i + 1)][0] * CifUnits_PerPixel)) \
                            + "," + str(int(appr_contour[-(i + 1)][1] * CifUnits_PerPixel))
        context_core_i += ";" + "\n"
        return context_core_i

    def fun2(for_th, fors_num, context_core_i, *args, **kkwargs, ):
        global context_core
        context_core += context_core_i
        # %%
        appr_contour = appr_contours[for_th]
        if is_plot == 1:
            ax2.plot(appr_contour[:, 1], appr_contour[:, 0], linewidth=linewidth)
        

    from fun_thread import my_thread, noop
    my_thread(10, len(appr_contours),
              fun1, fun2, noop,
              is_ordered=1, **kwargs, )
    # print(appr_contours[0][0][0])

    # %%
    if is_plot == 1:
        # ax2.axis('image')
        ax2.set_title('appr_contours')

        ax3.axis([0, cols, rows, 0])
        ax3.plot(appr_contours[-2][:, 1], appr_contours[-2][:, 0], linewidth=linewidth)
        # ax3.plot(appr_contours[0][:, 0], appr_contours[0][:, 1], linewidth=linewidth)
        ax3.plot(appr_contours[0][:, 1], appr_contours[0][:, 0], linewidth=linewidth)
        ax3.plot(appr_contours[-3][:, 1], appr_contours[-3][:, 0], linewidth=linewidth)
        ax3.plot(appr_contours[-1][:, 1], appr_contours[-1][:, 0], linewidth=linewidth)
        # ax3.axis('image')
        ax3.set_title('appr_contours[-2],[0],[-3],[1]')

        plt.show()

    # %%
    # #%% 生成 image_contours

    # image_contours = np.ones((width_y,hight_x,4),dtype='uint8') * 255 # 整体定义，不需要大量内存
    # image_appr_contours = np.ones((width_y,hight_x,4),dtype='uint8') * 255 # 整体定义，不需要大量内存
    # # RGB = 255,255,255，白色，全区域，均不调制；（这里可以 不初始化 RGB）
    # # 不透明度 alpha = 255，完全显示 RGB 三色

    # array_contours = contours[0]
    # for n in range(len(contours) - 1):
    #     array_contours = np.vstack((array_contours, contours[n+1]))

    # array_contours = np.uint(array_contours / img.shape[0] * width_y)

    # # array_contours = np.array(set(array_contours.tolist())) # 转换为 list 过滤 重复元素 后，再转回来
    # # 但 array_contours 中的每个元素 又是个 list，而 list 没有 hash 值，就没法 set 去重
    # array_contours = np.unique(array_contours, axis=0)

    # array_contours = array_contours.T

    # for k in range(3):
    #     image_contours[array_contours[0], array_contours[1], k] = 0

    # # for i in range(len(array_contours)):
    # #     for k in range(3):
    # #         image_contours[int(array_contours[i][0]), int(array_contours[i][1]), k] = 0
    # #         # image 中，边框 涂成 黑色 (0,0,0)

    # if is_positive != 1: # 如果 负片，则 黑白 反转
    #     image_contours = 255 - image_contours

    # if is_transparent == 1: # 如果 想把 白色 弄成 透明的
    #     image_contours[:, :, 3] = reverse(image_contours[:, :, 0])

    # #%%
    # #绘图：image_contours

    # plt.figure(figsize=(size_fig, size_fig), dpi=dpi)
    # plt.axis('off')
    # plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    # plt.margins(0,0)
    # plt.imshow(image_contours)

    # plt.savefig(location + "\\Grating_contours.svg", is_transparent = True, pad_inches=0) 
    # plt.savefig(location + "\\Grating_contours.png", is_transparent = True, pad_inches=0)
    # plt.show()

    # #%% 生成 image_appr_contours

    # array_appr_contours = appr_contours[0]
    # for n in range(len(appr_contours) - 1):
    #     array_appr_contours = np.vstack((array_appr_contours, appr_contours[n+1]))
    # # array_appr_contours = np.array(appr_contours, dtype=int)

    # array_appr_contours = np.uint(array_appr_contours / img.shape[0] * width_y)

    # array_appr_contours = np.unique(array_appr_contours, axis=0)

    # array_appr_contours = array_appr_contours.T

    # # array_appr_contours.astype(np.int32) # 等价于 上面的 np.uint8(...) 单独给 每个数据 改变 数据类型，不会改变 整个 数组 的 数据类型
    # # array_appr_contours.dtype = np.int32 # 这样做 虽然 会改变 整个 数组 的 数据类型， 但是 通过单独把 每个 float64 拆成了 8个 unit8 实现的

    # for k in range(3):
    #     image_appr_contours[array_appr_contours[0], array_appr_contours[1], k] = 0
    # # for i in range(len(array_appr_contours)):
    # #     for k in range(3):
    # #         image_appr_contours[int(array_appr_contours[i][0]), int(array_appr_contours[i][1]), k] = 0
    # #         # image 中，边框 涂成 黑色 (0,0,0)

    # if is_positive != 1: # 如果 负片，则 黑白 反转
    #     image_appr_contours = 255 - image_appr_contours

    # if is_transparent == 1: # 如果 想把 白色 弄成 透明的
    #     image_appr_contours[:, :, 3] = reverse(image_appr_contours[:, :, 0])

    # #%%
    # #绘图：image_appr_contours

    # plt.figure(figsize=(size_fig, size_fig), dpi=dpi)
    # # 图中图的大底板图，长=10英寸，宽=10英寸，每英寸300像素，共3000*3000像素

    # plt.axis('off') # 去掉 外侧 框线，只是 在 spyder 中去掉
    # # plt.xticks([])  # 去掉 横坐标值
    # # plt.yticks([])  # 去掉 纵坐标值
    # # plt.gca().xaxis.set_major_locator(plt.NullLocator())
    # # plt.gca().yaxis.set_major_locator(plt.NullLocator())
    # plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    # plt.margins(0,0)

    # plt.imshow(image_appr_contours)
    # # plt.imshow(array_yx, 'gray')
    # # plt.imshow(array_yxl_cos_step[l], 'gray'), \
    # #     plt.title("pattern_yx, l = %s" % (l), fontsize = 10)

    # # image_yx = Image.fromarray(array_yx)
    # # is_transparent = image_yx.convert('RGBA')

    # plt.savefig(location + "\\Grating_appr_contours.svg", is_transparent = True, pad_inches=0) 
    # plt.savefig(location + "\\Grating_appr_contours.png", is_transparent = True, pad_inches=0) # dpi=100 和上文相对应 pixel尺寸/dpi=inch尺寸
    # # cv2.imencode('.png', array_xy)[1].tofile(location)

    # plt.show()                 # 此处顺序不能弄反 imshow(),savefig(),show()
    # #plt.clf()                  #plt.clf()的作用：用于批量存储图片时 每一次显示图片并保存以后，释放图窗，接受下一个图片显示和存储

    # %%
    # 输出 txt
    from b_grating_to_cif import write_out_cif
    write_out_cif(context_core)


if __name__ == '__main__':
    kwargs = \
        {"size_PerCIF_Unit": 1 / 2000,
         "size_pattern": 3000, "size_PerPixel": 1,
         "size_pattern_y": 10000,  # size_pattern / size_PerPixel = 65536 = 2 ^ 16 是上限
         # %%
         "is_transverse": 1, "is_positive": 1, "is_transparent": 1,
         "is_reverse": 1,
         # %%
         "is_plot": 0,
         # %%
         "kwargs_seq": 0, "root_dir": r'1',
         "is_remove_root_dir": 1,
         }
    
    from fun_global_var import init_GLV_DICT
    init_GLV_DICT(**kwargs)
    
    grating_to_cif(**kwargs)
