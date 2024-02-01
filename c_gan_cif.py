# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 12:48:32 2021

@author: Xcz
"""

import numpy as np


# %%

def gan_mesh_xy(xy_mode="x",
                # %% 结构整体 区域大小
                LD_x=0, LD_y=0,  # Left_Down_xy
                L_x=10, L_y=3,
                # %% 结构内部 畴的大小
                T_x=10, T_y=10,
                D_x=0.5, D_y=0.5, **kwargs, ):  # Duty_circle_x
    LD_x *= 1000  # 统一为 um 单位
    LD_y *= 1000  # 统一为 um 单位
    L_x *= 1000  # 统一为 um 单位
    L_y *= 1000  # 统一为 um 单位
    Dx = D_x if D_x >= 1 else T_x * D_x  # 已经是 um 单位 （如果 >= 1 则不认为是 占空比，而是 图案畴宽）
    Dy = D_y if D_y >= 1 else T_y * D_y  # 已经是 um 单位 （如果 >= 1 则不认为是 占空比，而是 图案畴宽）
    if "x" in xy_mode and "y" in xy_mode:
        ruler_x = np.arange(0, L_x, T_x) + LD_x + Dx / 2  # cif 里，以 第一个 B（矩形）的 中间 为 原点
        ruler_y = np.arange(0, L_y, T_y) + LD_y + Dy / 2  # cif 里，以 第一个 B（矩形）的 中间 为 原点
        mesh_x, mesh_y = np.meshgrid(ruler_x, ruler_y)
        unit_x = np.ones(mesh_x.shape, ) * Dx
        unit_y = np.ones(mesh_x.shape, ) * Dy
    elif "x" in xy_mode:
        mesh_x = np.arange(0, L_x, T_x) + LD_x + Dx / 2  # cif 里，以 第一个 B（矩形）的 中间 为 原点
        mesh_y = np.ones((len(mesh_x)), ) * LD_y + L_y / 2  # cif 里，以 第一个 B（矩形）的 中间 为 原点
        unit_x = np.ones((len(mesh_x)), ) * Dx
        unit_y = np.ones((len(mesh_x)), ) * L_y
        # print(mesh_x)
    elif "y" in xy_mode:
        mesh_y = np.arange(0, L_y, T_y) + LD_y + Dy / 2  # cif 里，以 第一个 B（矩形）的 中间 为 原点
        mesh_x = np.ones((len(mesh_y)), ) * LD_x + L_x / 2  # cif 里，以 第一个 B（矩形）的 中间 为 原点
        unit_x = np.ones((len(mesh_y)), ) * L_x
        unit_y = np.ones((len(mesh_y)), ) * Dy
    if "-x" in xy_mode:  # 左右翻转
        mesh_x *= -1
    if "-y" in xy_mode:  # 上下翻转
        mesh_y *= -1
    return mesh_x, mesh_y, \
           unit_x, unit_y


def gan_txt(mesh_x, mesh_y, unit_x, unit_y,
            # %% cif 文件 一个像素 默认 1/2000 um ？
            xy_mode="x",
            # %%
            size_PerCIF_Unit=1 / 2000,
            prefix_context_core="L CPG;\n", **kwargs, ):
    mesh_units = np.dstack((unit_x, unit_y, mesh_x, mesh_y)) / size_PerCIF_Unit
    mesh_units = np.floor(mesh_units / 2) * 2
    # %%
    global context_core
    context_core = prefix_context_core
    # %%
    if "x" in xy_mode and "y" in xy_mode:
        # %%  单线程
        # for i in range(mesh_units.shape[0]):
        #     for j in range(mesh_units.shape[1]):
        #         context_core += "B %d %d %d %d;\n" % (mesh_units[i, j, 0],
        #                                               mesh_units[i, j, 1],
        #                                               mesh_units[i, j, 2],
        #                                               mesh_units[i, j, 3])
        # %%  多线程 begin
        def fun1(for_th, fors_num, *arg, **kkwargs, ):
            context_core_i = ""
            for j in range(mesh_units.shape[1]):
                context_core_i += "B %d %d %d %d;\n" % (mesh_units[for_th, j, 0],
                                                        mesh_units[for_th, j, 1],
                                                        mesh_units[for_th, j, 2],
                                                        mesh_units[for_th, j, 3])
            # print(context_core_i)
            return context_core_i

        def fun2(for_th, fors_num, context_core_i, *args, **kkwargs, ):
            # print(context_core_i)
            global context_core
            context_core += context_core_i

        from fun_thread import my_thread, noop
        my_thread(10, mesh_units.shape[0],
                  fun1, fun2, noop,
                  is_ordered=1, **kwargs, )
        # %%
    elif "x" in xy_mode or "y" in xy_mode:
        # print(mesh_units.shape[1])
        for j in range(mesh_units.shape[1]):
            context_core += "B %d %d %d %d;\n" % (mesh_units[0, j, 0],
                                                  mesh_units[0, j, 1],
                                                  mesh_units[0, j, 2],
                                                  mesh_units[0, j, 3])
        # if i == 0:
        #     print(context_core)
    # print(context_core)
    return context_core


# %%
def gan_cif(**kwargs):
    return gan_txt(*gan_mesh_xy(**kwargs), **kwargs, )

    # %%


if __name__ == '__main__':
    kwargs = \
        {"xy_mode": 'x',
         # %%
         "LD_x": -0.01, "LD_y": 0.01,  # 第一个结构 左下角 x,y (mm)
         "L_x": 20, "L_y": 1,  # L_x：x 方向 结构长度 (mm)， L_y: y 方向 结构长度 (mm)
         # %%
         "T_x": 3.08, "T_y": 6,
         "D_x": 1, "D_y": 1,
         # %%
         "kwargs_seq": 0, "root_dir": r'1',
         "is_remove_root_dir": 1,
         # %%
         }
    from fun_global_var import init_GLV_DICT
    from b_grating_to_cif import write_out_cif

    init_GLV_DICT(**kwargs)
    write_out_cif(gan_cif(**kwargs))
