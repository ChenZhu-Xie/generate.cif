# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 12:48:32 2021

@author: Xcz
"""

from c_CGH_grating_cif import CGH_grating_cif

# %%
if __name__ == '__main__':
    kwargs = \
        {"l": 0, "structure_xy_mode": 'x*y',
         "m_x": 1, "T_x": 6, "Duty_Cycle_x": 0.3,
         "m_y": 1, "T_y": 7.2, "Duty_Cycle_y": 0.25, # 0.6 每像素 的情况下，0.33 占空比 效果 = 0.25
         # %%
         "size_PerCIF_Unit": 1 / 2000,
         "size_pattern": 3000, "size_PerPixel": 0.6,  # 不能是 0.奇数，得是 0.偶数
         "size_pattern_y": 10000,  # size_pattern / size_PerPixel = 65536 = 2 ^ 16 是上限
         # %%
         "is_transverse": 1, "is_positive": 1, "is_transparent": 1,
         "is_reverse": 0,
         # %%
         "is_plot": 0,
         # %%
         "kwargs_seq": 0, "root_dir": r'1',
         "is_remove_root_dir": 1,
         }
    from fun_global_var import init_GLV_DICT

    init_GLV_DICT(**kwargs)
    CGH_grating_cif(**kwargs)
