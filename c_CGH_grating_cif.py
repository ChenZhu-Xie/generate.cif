# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 12:48:32 2021

@author: Xcz
"""

from a_CGH_grating import CGH_grating
from b_grating_to_cif import grating_to_cif


# %%

def CGH_grating_cif(l=1, structure_xy_mode="x",
                    m_x=1, T_x=10, Duty_Cycle_x=0.5,
                    m_y=1, T_y=10, Duty_Cycle_y=0.5,
                    # %%
                    size_pattern=100, size_PerPixel=0.1,
                    size_PerCIF_Unit=1 / 2000,
                    # %%
                    is_transverse=0, is_positive=1, is_transparent=1,
                    **kwargs):
    # l = 1
    # T_x = 10 # unit: um
    # m = -1
    # size_pattern = 8.5 * T_x # unit: um 如果 只是 示意图，填 10 或 8.5 倍 的 周期 T_x 左右，即 8.5 * T_x 即可
    # size_PerPixel = 0.1 # unit: um / pixel，分辨率
    # size_PerCIF_Unit = 1 / 2000 # unit: um / cif_unit
    # is_transverse = 0 # 如果 要生成 tif 文件，则需要 转置 is_transverse = 1；否则 若想看 正向，则 不转置
    # is_positive = 1
    # is_transparent = 1 # is_transparent = 0 是指 不论黑白 都保留 不透明
    # Duty_Cycle_x = 0.5 # -1 ~ 1，正表示 is_positive 片 中 黑色 (R,G,B,A) = (0,0,0,1) 调制（畴反转，chi_2 < 0）区域 占空比 更小
    # 0.5 意味着 1/3 占空比， -0.5 意味着 2/3 占空比 

    CGH_grating(l, structure_xy_mode,
                m_x, T_x, Duty_Cycle_x,
                m_y, T_y, Duty_Cycle_y,
                # %%
                size_pattern, size_PerPixel,
                is_transverse, is_positive, is_transparent, **kwargs)

    grating_to_cif(size_PerCIF_Unit,
                   size_pattern, size_PerPixel,
                   is_transverse, is_positive, is_transparent, **kwargs)


# %%

if __name__ == '__main__':
    kwargs = \
        {"l": 0, "structure_xy_mode": 'xy',
         "m_x": 1, "T_x": 6, "Duty_Cycle_x": 0.5,
         "m_y": 1, "T_y": 6, "Duty_Cycle_y": 0.5,
         # %%
         "size_PerCIF_Unit": 1 / 2000,
         "size_pattern": 300, "size_PerPixel": 1,
         "size_pattern_y": 1000,  # size_pattern / size_PerPixel = 65536 = 2 ^ 16 是上限
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
    CGH_grating_cif(**kwargs)
