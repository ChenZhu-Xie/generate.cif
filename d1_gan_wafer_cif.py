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
                  Lx=[3, 4, 5], Ly=[10, 20, 30],
                  Tx_min=6, Ty_min=7,
                  dTx=0.2, dTy=0.1,
                  **kwargs):

    # %% 1D ------------------------------------

    kwargs.update({
        "xy_mode": 'x',
        # %%
        "LD_x": wafer_LU_LD_x, "LD_y": wafer_LU_LD_y,  # 结构左下角 x,y (mm)
        "L_x": Lx[0], "L_y": Ly[0],  # L_x：x 方向 结构长度 (mm)， L_y: y 方向 结构长度 (mm)
        # %%
        "T_x": Tx_min, "D_x": 2,
    })
    Tx_62_1D = gan_cif(**kwargs)

    interval_x = 3
    kwargs.update({
        "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
        "T_x": kwargs["T_x"] + dTx,
    })
    Tx_64_1D = gan_cif(**kwargs)

    kwargs.update({
        "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
        "T_x": kwargs["T_x"] + dTx,
    })
    Tx_66_1D = gan_cif(**kwargs)
    
    # write_out_cif(Tx_62_1D + Tx_64_1D + Tx_66_1D)

    # %% 2D ------------------------------------

    kwargs.update({
        "xy_mode": 'xy',
        # %%
        "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
        "T_x": Tx_min,
        "T_y": Ty_min, "D_y": 2,
    })
    Tx_62_2D = gan_cif(add_level=-1, **kwargs)

    kwargs.update({
        "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
        "T_x": kwargs["T_x"] + dTx,
        "T_y": kwargs["T_y"] + dTy,
    })
    Tx_64_2D = gan_cif(**kwargs)

    kwargs.update({
        "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
        "T_x": kwargs["T_x"] + dTx,
        "T_y": kwargs["T_y"] + dTy,
    })
    Tx_66_2D = gan_cif(**kwargs)

    # write_out_cif(Tx_62_1D + Tx_64_1D + Tx_66_1D +
    #               Tx_62_2D + Tx_64_2D + Tx_66_2D)
    
    # %% 1D ------------------------------------
    interval_y = 3
    Tx_min += 0.1
    Ty_min += 0.05
    
    kwargs.update({
        "xy_mode": 'x',
        # %%
        "LD_x": wafer_LU_LD_x, 
        "LD_y": wafer_LU_LD_y - interval_y - Ly[1],  # 结构左下角 x,y (mm)
        "L_x": Lx[1], "L_y": Ly[1],  # L_x：x 方向 结构长度 (mm)， L_y: y 方向 结构长度 (mm)
        # %%
        "T_x": Tx_min,
    })
    Tx_63_1D = gan_cif(**kwargs)

    kwargs.update({
        "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
        "T_x": kwargs["T_x"] + dTx,
    })
    Tx_65_1D = gan_cif(**kwargs)

    kwargs.update({
        "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
        "T_x": kwargs["T_x"] + dTx,
    })
    Tx_67_1D = gan_cif(**kwargs)
    
    write_out_cif(Tx_62_1D + Tx_64_1D + Tx_66_1D +
                  Tx_62_2D + Tx_64_2D + Tx_66_2D +
                  Tx_63_1D + Tx_65_1D + Tx_67_1D)

    # %% 2D ------------------------------------

    # kwargs.update({
    #     "xy_mode": 'xy', 
    #     # %%
    #     "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
    #     "T_x": Tx_min,
    #     "T_y": Ty_min,
    # })
    # Tx_63_2D = gan_cif(add_level=-1, **kwargs)

    # kwargs.update({
    #     "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
    #     "T_x": kwargs["T_x"] + dTx,
    #     "T_y": kwargs["T_y"] + dTy,
    # })
    # Tx_65_2D = gan_cif(**kwargs)

    # kwargs.update({
    #     "LD_x": kwargs["LD_x"] + kwargs["L_x"] + interval_x,  # 加的 interval 得 > 上一个的 L_x
    #     "T_x": kwargs["T_x"] + dTx,
    #     "T_y": kwargs["T_y"] + dTy,
    # })
    # Tx_67_2D = gan_cif(**kwargs)

    # write_out_cif(Tx_62_1D + Tx_64_1D + Tx_66_1D +
    #               Tx_62_2D + Tx_64_2D + Tx_66_2D +
    #               Tx_63_1D + Tx_65_1D + Tx_67_1D +
    #               Tx_63_2D + Tx_65_2D + Tx_67_2D)
    

if __name__ == '__main__':
    kwargs = \
        {"wafer_LU_LD_x": -19.5, "wafer_LU_LD_y": 7.5,
         "Lx": [4, 4], "Ly": [12, 24],
         "Tx_min": 6.2, "Ty_min": 6.9,
         # %%
         "kwargs_seq": 0, "root_dir": r'1',
         "is_remove_root_dir": 1,
         }
    
    from fun_global_var import init_GLV_DICT

    init_GLV_DICT(**kwargs)
    gan_wafer_cif(**kwargs)
