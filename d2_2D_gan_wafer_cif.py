# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 12:48:32 2021

@author: Xcz
"""

import numpy as np
from c_gan_cif import gan_cif
from b_grating_to_cif import write_out_cif


# %%
def gan_wafer_cif(wafer_LU_LD_x=-20, wafer_LU_LD_y=5,
                  interval_x=3, interval_y=3,
                  Lx=[3, 4, 5], Ly=[12, 24],
                  Tx_1=[8, 7, 6], Ty_1=[7.95, 7.98, 8.04],
                  Tx_2=[8.5, 7.5, 6.5], Ty_2=[7.93, 7.96, 8.01],
                  **kwargs):
    # %% 2D ------------------------------------

    kwargs.update({
        "xy_mode": 'xy',
        # %%
        "LD_x": wafer_LU_LD_x, "LD_y": wafer_LU_LD_y,  # 结构左下角 x,y (mm)
        "L_x": Lx[0], "L_y": Ly[0],  # L_x：x 方向 结构长度 (mm)， L_y: y 方向 结构长度 (mm)
        "T_x": Tx_1[0], "T_y": Ty_1[0],
        "D_x": 1, "D_y": 1,
    })
    Tx_8_2D = gan_cif(add_level=-1, **kwargs)

    kwargs.update({
        "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
        "L_x": Lx[1],
        "T_x": Tx_1[1], "T_y": Ty_1[1],
    })
    Tx_7_2D = gan_cif(**kwargs)

    kwargs.update({
        "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
        "L_x": Lx[2],
        "T_x": Tx_1[2], "T_y": Ty_1[2],
    })
    Tx_6_2D = gan_cif(**kwargs)

    # write_out_cif(Tx_8_2D + Tx_7_2D + Tx_6_2D)

    # %% -2D ------------------------------------

    kwargs.update({
        "xy_mode": '-xy',
        # %%
        "LD_x": wafer_LU_LD_x,  # 结构左下角 x,y (mm)
        "L_x": Lx[0],  # L_x：x 方向 结构长度 (mm)， L_y: y 方向 结构长度 (mm)
        "T_x": Tx_1[0], "T_y": Ty_1[0],
    })
    Tx_8_nega_2D = gan_cif(**kwargs)

    kwargs.update({
        "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
        "L_x": Lx[1],
        "T_x": Tx_1[1], "T_y": Ty_1[1],
    })
    Tx_7_nega_2D = gan_cif(**kwargs)

    kwargs.update({
        "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
        "L_x": Lx[2],
        "T_x": Tx_1[2], "T_y": Ty_1[2],
    })
    Tx_6_nega_2D = gan_cif(**kwargs)

    # write_out_cif(Tx_8_2D + Tx_7_2D + Tx_6_2D +
    #               Tx_8_nega_2D + Tx_7_nega_2D + Tx_6_nega_2D)

    # %% 2D ------------------------------------

    kwargs.update({
        "xy_mode": 'xy',
        # %%
        "LD_x": wafer_LU_LD_x,
        "LD_y": wafer_LU_LD_y - interval_y - Ly[1],  # 结构左下角 x,y (mm)
        "L_x": Lx[0], "L_y": Ly[1],  # L_x：x 方向 结构长度 (mm)， L_y: y 方向 结构长度 (mm)
        "T_x": Tx_2[0], "T_y": Ty_2[0],
    })
    Tx_85_2D = gan_cif(**kwargs)

    kwargs.update({
        "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
        "L_x": Lx[1],
        "T_x": Tx_2[1], "T_y": Ty_2[1],
    })
    Tx_75_2D = gan_cif(**kwargs)

    kwargs.update({
        "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
        "L_x": Lx[2],
        "T_x": Tx_2[2], "T_y": Ty_2[2],
    })
    Tx_65_2D = gan_cif(**kwargs)

    # write_out_cif(Tx_8_2D + Tx_7_2D + Tx_6_2D +
    #               Tx_8_nega_2D + Tx_7_nega_2D + Tx_6_nega_2D +
    #               Tx_85_2D + Tx_75_2D + Tx_65_2D)

    # %% -2D ------------------------------------

    kwargs.update({
        "xy_mode": '-xy',
        # %%
        "LD_x": wafer_LU_LD_x,  # 结构左下角 x,y (mm)
        "L_x": Lx[0],  # L_x：x 方向 结构长度 (mm)， L_y: y 方向 结构长度 (mm)
        "T_x": Tx_2[0], "T_y": Ty_2[0],
    })
    Tx_85_nega_2D = gan_cif(**kwargs)

    kwargs.update({
        "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
        "L_x": Lx[1],
        "T_x": Tx_2[1], "T_y": Ty_2[1],
    })
    Tx_75_nega_2D = gan_cif(**kwargs)

    kwargs.update({
        "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
        "L_x": Lx[2],
        "T_x": Tx_2[2], "T_y": Ty_2[2],
    })
    Tx_65_nega_2D = gan_cif(**kwargs)

    write_out_cif(Tx_8_2D + Tx_7_2D + Tx_6_2D +
                  Tx_8_nega_2D + Tx_7_nega_2D + Tx_6_nega_2D +
                  Tx_85_2D + Tx_75_2D + Tx_65_2D +
                  Tx_85_nega_2D + Tx_75_nega_2D + Tx_65_nega_2D)


if __name__ == '__main__':  # 2D PPCLT
    kwargs = \
        {"wafer_LU_LD_x": -20, "wafer_LU_LD_y": 7,  # mm
         "interval_x": 3, "interval_y": 3,  # mm
         "Lx": [3, 4, 5], "Ly": [12, 24],  # mm
         "Tx_1": [8, 7, 6], "Ty_1": [7.95, 7.98, 8.04],  # um
         "Tx_2": [8.5, 7.5, 6.5], "Ty_2": [7.93, 7.96, 8.01],  # um
         # %%
         "kwargs_seq": 0, "root_dir": r'1',
         "is_remove_root_dir": 1,
         }

    from fun_global_var import init_GLV_DICT

    init_GLV_DICT(**kwargs)
    gan_wafer_cif(**kwargs)
