# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 14:41:11 2021

@author: Xcz
"""
import winreg
import os
import sys
import re
import cv2
import numpy as np
import math
import inspect
from fun_global_var import init_Set, Set, Get, tree_print
from scipy.io import loadmat, savemat
from fun_plot import plot_1d, plot_2d, plot_3d_XYz, plot_3d_XYZ
from fun_gif_video import imgs2gif_imgio, imgs2gif_PIL, imgs2gif_art
from fun_built_in import str_to_float


# %%

def try_to_call_me():
    import os
    print(1, os.path.basename(__file__).split('.')[0])
    import sys
    print(2, sys.argv)
    print(3, sys.argv[0].split('\\')[-1].split('.')[0])  # 获取 main 函数，所在 的 py 文件名（而不是 函数名）
    import inspect
    print(4, inspect.stack()[1][0])
    print(5, inspect.stack()[1][3])
    print(6, [inspect.stack()[i][3] for i in range(len(inspect.stack()))])


# %%

def get_main_py_name():
    return sys.argv[0].split('\\')[-1].split('.')[0]


# %%
# 获取 桌面路径（C 盘 原生）

def GetDesktopPath():  # 修改过 桌面位置 后，就不准了
    return os.path.join(os.path.expanduser("~"), 'Desktop')


# %%
# 获取 桌面路径（注册表）

def get_desktop():  # 无论如何都准，因为读的是注册表
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]


# %%
# 获取 当前 py 文件 所在路径 Current Directory

def get_cd():
    return os.path.dirname(os.path.abspath(__file__))  # 其实不需要，默认就是在 相对路径下 读，只需要 文件名 即可


# %%
# 查找

# 查找 text 中的 数字部分
def find_nums(text):  # 这个没用了，也就是 ray
    return re.findall('(\d+)', text)


# 查找 text 中的 非数字部分
def find_NOT_nums(text):  # 这个没用了，也就是 ugHGU
    return re.findall('(\D+)', text)


# 查找 含 s 的 字符串 part，part 为在 text 中 被 separator（分隔符） 分隔 的 文字
def find_part_has_s_in_text(text, s, separator):
    for i, part in enumerate(text.split(separator)):
        if s in part:  # 找到 第一个 part 之后，不加 含 z 的 part，就 跳出 for 循环
            return part


# 查找 ray_sequence
def split_parts(U_name):
    if ' - ' in U_name:
        Part_1 = U_name.split(' - ')[0]  # 取出 seq + method + way 的 method_and_way
        method_and_way = Part_1.split(" ")[1] if " " in Part_1 else Part_1  # 去掉 seq，只保留 method + way
        Part_2 = U_name.split(' - ')[1]  # 取 由 AST - U0_ ... 分割的 第二部分：U0_ ...
    else:
        method_and_way = ""
        Part_2 = U_name  # 应该不存在 没有 method 而有 sequence 的可能（只有 文件夹 才有这 可能）
    if '_' in Part_2:
        part_1 = Part_2.split('_')[0]  # 取 part_2 中的 第一部分 U1
    elif ' ' in Part_2:
        part_1 = Part_2.split(" ")[1]
    else:
        part_1 = Part_2
    ray_seq = part_1[1:] if len(part_1[1:]) > 0 else ""  # 取出 U0_name 第一部分 第一个字符之后的东西
    ugHGU = part_1[0] if len(part_1) > 0 else ""
    U_name_no_seq = method_and_way + (' - ' if method_and_way != "" else "") + Part_2

    # print(U_name)
    # print(U_name_no_seq, method_and_way, Part_2, ugHGU, ray_seq)

    from fun_global_var import Set
    Set("method_and_way", method_and_way)

    return U_name_no_seq, method_and_way, Part_2, ugHGU, ray_seq


# 查找 ray （ 要么从 U_name 里传 ray 和 U 进来，要么 单独传个 U 和 ray ）
def set_ray(U0_name, ray_tag, **kwargs):  # U0_name 只在这有用，用于获取 其 ray，获取一次后就不需 U0_name 了
    if "ray" not in kwargs:  # 传 'U' 的值 进来的同时，要传个 'ray' 键 及其 对应的值
        U_name_no_seq, method_and_way, Part_2, ugHGU, ray_seq = split_parts(U0_name)  # 从 U0_name 中找到 ray_sequence
        ray = ray_seq[0] + ray_tag if len(ray_seq) != 0 else ray_tag
    else:
        ray = kwargs['ray'] + ray_tag if "ray" in kwargs else ray_tag  # 传 'U' 的值 进来的同时，要传个 'ray' 键 及其 对应的值

    return ray


# # 查找 ray（已废弃）
# def get_ray(U0_name, U_name, ): # 这个没用了，已经被 split_parts 和 set_ray 替代了
#     method_and_way, ugHGU, ray_seq = split_parts(U0_name)  # 从 U0_name 中找到 ray_sequence
#     # 如果 U0_name 被 _ 分割出的 第一部分 不是空的 且 含有数字，则将其 数字部分 取出，暂作为 part_1 的 数字部分（传染性）
#     ray = ray_seq[0] if len(ray_seq) != 0 else ""
#
#     # U_name_rays = find_nums(U_name.split('_')[0])
#     U_name_rays = U_name.split('_')[0][1:] # 取出 U_name 第一部分 第一个字符之后的东西
#     # 如果 U_name 第一部分 含有数字，则 在 part_1 后面 追加 U_name 第一部分 原本的 数字部分
#     ray += U_name_rays[0] if len(U_name_rays) != 0 else ""
#     return ray

# %%
# 替换

def replace_p_ray(title, ugHGU, ray):  # ugHGU 起到了 标识符的作用，防止误 replace 了 其他字符串
    return title.replace(ugHGU + ray, ugHGU + ray.replace("0", "p"))


def subscript_ray(title, ugHGU, ray):  # ugHGU 起到了 标识符的作用，防止误 replace 了 其他字符串
    # return title.replace(ugHGU + ray, ugHGU + "$_{" + ray.replace("0", "p") + "}$")
    return title.replace(ugHGU + ray, ugHGU + "$_{" + ray + "}$")


def subscript_way(title, method_and_way):  # method 起到了 标识符的作用，防止误 replace 了 其他字符串
    if '_' in method_and_way:
        method = method_and_way.split("_")[0]
        way = method_and_way.split("_")[1]
        return title.replace(method + "_" + way, method + "$_{" + way + "}$")
    else:
        return title


def add___between_ugHGU_and_ray(Uz_name, ugHGU, ray):
    return Uz_name.replace(ugHGU + ray, ugHGU + "_" + ray)

    # %%


# 生成 part_1 （被 分隔符 分隔的 第一个） 字符串
def gan_seq(U_name, is_add_sequence,  # 就 2 功能，加序号，减 method_and_way
            **kwargs, ):  # kwargs 是 “suffix”

    # ugHGU = find_NOT_nums(U_name.split('_')[0])[0]
    # ugHGU = U_name.split('_')[0][0] if len(U_name.split('_')[0]) != 0 else ""
    U_name_no_seq, method_and_way, Part_2, ugHGU, ray = split_parts(U_name)
    # print(ugHGU)

    seq = ''
    # 模为 1 即有 seq
    # >= 0 即有 method_and_way
    if abs(is_add_sequence) == 1:
        if ugHGU == 'g':
            seq = "3."
        elif ugHGU == 'H':
            seq = "4."
        elif ugHGU == 'G':
            seq = "3." if method_and_way == "PUMP" else "5."
        elif ugHGU == 'U':
            seq = "2." if method_and_way == "PUMP" else "6."
        # elif ugHGU == "χ" or ugHGU == "n":
        #     seq = "0."

        if "suffix" in kwargs:  # 如果 还传入了 后缀 "_phase" 或 '_amp'
            suffix = kwargs["suffix"]
            if suffix == '_amp' or suffix == '_amp_error' or suffix == '_energy':
                seq += '1.'
            elif suffix == '_phase' or suffix == '_phase_error':
                seq += '2.'

        if seq != "":
            seq += ' '  # 数字序号后 都得加个空格

    return seq


def gan_Uz_name(U_name, is_add_sequence, **kwargs, ):  # args 是 z 或 () 和 suffix

    U_name_no_seq, method_and_way, Part_2, ugHGU, ray = split_parts(U_name)
    seq = gan_seq(U_name, is_add_sequence, **kwargs, )  # is_add_sequence 模为 1 即有 seq
    # seq = "" # 取消了 手动 给最后一个 folder 添加 seq 的 机制，完全自动化了
    # oh 不，mat 文件 是要加 seq 的，folder 不加
    U_new_name = seq + U_name_no_seq
    # %%
    # 查找 含 z 的 字符串 part_z
    part_z = find_part_has_s_in_text(Part_2, 'z', '_')
    if (U_name.find('z') != -1 or U_name.find('Z') != -1) and 'z' in kwargs:
        # 如果 找到 z 或 Z，且 传了 额外的 参数 进来，这个参数 解包后的 第一个参数 不是 空 tuple ()
        z = kwargs['z']
        # print(U_name, z, part_z)
        part_z_context = "_" + part_z  # 需要 含 z 上下文 整体替换，否则 可能 误替换了 所有含 z 的 字符串
        part_z_format = "_" + str(float(Get('f_f') % z)) + "mm"  # Set('f_f') 首先得 初始化好；格式化的 z 不能是 str 类型
        U_new_name = U_new_name.replace(part_z_context, part_z_format, 1)  # 只替换 找到的 第一个 匹配项
        # 原版是 str(float('%.2g' % z))，还用过 format(z, Get("F_E"))、float(format(z, Get('F_E')))，这后两个 也得加 str
        # 把 原来含 z 的 part_z 替换为 str(float('%.2g' % z)) + "mm"
    # print(U_new_name)
    if is_add_sequence < 0:  # is_add_sequence >= 0 即有 method_and_way = method + way
        U_new_name = U_new_name.replace(method_and_way + " - ", "")

    return U_new_name, U_name_no_seq, method_and_way, Part_2, ugHGU, ray


def gan_Uz_plot_address(folder_address, img_name_extension,
                        U_name, suffix, **kwargs):
    Uz_name, U_name_no_seq, method_and_way, Part_2, ugHGU, ray = gan_Uz_name(U_name, 1, suffix=suffix,
                                                                             **kwargs, )  # 要加 序列号 # 有 method 和 suffix
    Uz_name += suffix if suffix not in U_name else ""
    Uz_name = add___between_ugHGU_and_ray(Uz_name, ugHGU, ray)
    Uz_full_name = Uz_name + img_name_extension
    Uz_plot_address = folder_address + "\\" + Uz_full_name

    return Uz_full_name, Uz_plot_address


def gan_Uz_title(U_name, suffix, **kwargs):
    Uz_title, U_name_no_seq, method_and_way, Part_2, ugHGU, ray = gan_Uz_name(U_name, 0, suffix=suffix,
                                                                              **kwargs, )  # 不加 序列号 # 有 method 和 suffix
    Uz_title += suffix if suffix not in U_name else ""
    Uz_title = subscript_ray(Uz_title, ugHGU, ray)
    Uz_title = subscript_way(Uz_title, method_and_way)
    return Uz_title


def gan_Uz_save_address(U_name, folder_address, is_save_txt,
                        **kwargs):
    U_full_name, U_name_no_seq, method_and_way, Part_2, ugHGU, ray = gan_Uz_name(U_name, 1,
                                                                                 **kwargs, )  # 要加 序列号 # 要有 method （诸如 'AST'）
    U_full_name = add___between_ugHGU_and_ray(U_full_name, ugHGU, ray)
    file_name = U_full_name + (is_save_txt and ".txt" or ".mat")
    U_address = folder_address + "\\" + file_name
    return U_address, ugHGU


# %%

def gan_Uz_dir_address(U_name, **kwargs, ):
    # folder_name, U_name_no_seq, method_and_way, Part_2, ugHGU, ray = gan_Uz_name(U_name, -1,
    #                                                                              **kwargs, )  # 要加 序列号 # 没有 method （诸如 'AST'）
    folder_name, U_name_no_seq, method_and_way, Part_2, ugHGU, ray = gan_Uz_name(U_name, 0,
                                                                                 **kwargs, )  # 不加 序列号 # 没有 method （诸如 'AST'）
    # print(folder_name)
    if ugHGU in "gHGU":
        folder_name = add___between_ugHGU_and_ray(folder_name, ugHGU, ray)
    if "p_dir" in kwargs:
        folder_address_relative = kwargs["p_dir"] + "\\" + folder_name
    else:
        folder_address_relative = folder_name
    folder_address = Get("root_dir") + "\\" + folder_address_relative
    # %% 自动给 非最末的 每一层 dirs[l] 添加 序数（现在也给 最末添加 序数了）
    txt_address = Get("root_dir") + "\\" + "all_data_info.txt"
    with open(txt_address, "a+") as txt:  # 追加模式；如果没有 该文件，则 创建之；+ 表示 除了 写 之外，还可 读
        data_th, Data_Seq, Level_Seq = gan_Data_Seq(txt, folder_address)

    dirs = folder_address_relative.split("\\")
    level = len(dirs)  # len(dirs) = len(level_seq)
    level_seq = Level_Seq.split('.')  # ['0','0','0',...]

    folder_address_relative = ''
    for l in range(level):
        dirs[l] = level_seq[l] + '. ' + dirs[l]  # 现在已经 解除限制了 = =
        # if l != level-1: # 如果不是 最后一级（最后一级 的 dirs[l] 已经设定了 seq 了，是其自带的）
        #     dirs[l] = level_seq[l] + '. ' + dirs[l]
        folder_address_relative += dirs[l]
        folder_address_relative += ("\\" if l != level - 1 else '')

    folder_address = Get("root_dir") + "\\" + folder_address_relative
    # %%
    if kwargs.get("is_no_data_save", 0) == 1:  # 如果 只产生 有父目录的 文件夹 以及 其下的图片，没有数据 存在里面
        # ugHGU, z_str, U_name_no_suffix, U_name, U_address = '', '', '', '', ''
        z_str = str(kwargs['z']) if 'z' in kwargs else 'z'
        U_name_no_suffix = folder_name.replace(kwargs['suffix'], '') if 'suffix' in kwargs else 'U_name_no_suffix'
        main_py_name, is_data_saved, kwargs_seq, root_dir_boot_times, \
        saver_name, ugHGU, z_str, U_name, U_name_no_suffix, root_dir, U_address = \
            Get("main_py_name"), 0, Get("kwargs_seq"), Get("root_dir_boot_times"), \
            inspect.stack()[1][3], ugHGU, z_str, folder_name, U_name_no_suffix, Get("root_dir"), ''

        txt_address = Get("root_dir") + "\\" + "all_data_info.txt"
        with open(txt_address, "a+") as txt:  # 追加模式；如果没有 该文件，则 创建之；+ 表示 除了 写 之外，还可 读
            attr_Auto_Set(locals())  # 定义完 所有 attr 后，就写入 记录之
            attr_line = auto_gan_attr_line()
            txt.write(attr_line)
    return folder_address


# %%

def U_energy_print(U_receive, U_name, is_print,  # 外面的 **kwargs 可能传进 “U” 这个关键字，所以...用 U_receive 代替 实参名 U
                   **kwargs, ):  # kwargs 是 z

    U_full_name, U_name_no_seq, method_and_way, Part_2, ugHGU, ray = gan_Uz_name(U_name, 0,
                                                                                 **kwargs, )  # 不加 序列号 # 要有 method （诸如 'AST'）

    # print(kwargs.get("is_end", 0))
    is_print and print(tree_print(kwargs.get("is_end", 0), add_level=-1) + U_full_name + ".total_energy = {}"
                       .format(format(np.sum(np.abs(U_receive) ** 2), Get("F_E"))))  # 重新调用 该方法时，无论如何都不存在 level + 1 的需求。
    kwargs.pop("is_end", None);
    kwargs.pop("add_level", None)  # 该 def 子分支 后续默认 is_end = 0，如果 kwargs 还会被 继续使用 的话。


def U_rsd_print(U_receive, U_name, is_print,
                **kwargs, ):  # kwargs 是 z

    U_full_name, U_name_no_seq, method_and_way, Part_2, ugHGU, ray = gan_Uz_name(U_name, 0,
                                                                                 **kwargs, )  # 不加 序列号 # 要有 method （诸如 'AST'）

    is_print and is_print - 1 and print(tree_print(kwargs.get("is_end", 0), add_level=-1) + U_full_name + ".rsd = {}"
                                        .format(
        format(np.std(np.abs(U_receive)) / np.mean(np.abs(U_receive)), Get("F_E"))))  # is_print 是 1 和 0 都不行，得是 2 等才行...
    kwargs.pop("is_end", None);
    kwargs.pop("add_level", None)  # 该 def 子分支 后续默认 is_end = 0，如果 kwargs 还会被 继续使用 的话。


def U_custom_print(U_receive, U_name, custom_info, is_print,  # 外面的 **kwargs 可能传进 “U” 这个关键字，所以...用 U_receive 代替 实参名 U
                   **kwargs, ):  # kwargs 是 z

    U_full_name, U_name_no_seq, method_and_way, Part_2, ugHGU, ray = gan_Uz_name(U_name, 0,
                                                                                 **kwargs, )  # 不加 序列号 # 要有 method （诸如 'AST'）

    is_print and print(tree_print(kwargs.get("is_end", 0), add_level=-1) + U_full_name + "." + custom_info + " = {}"
                       .format(format(U_receive, Get("F_E"))))  # 重新调用 该方法时，无论如何都不存在 level + 1 的需求。
    kwargs.pop("is_end", None);
    kwargs.pop("add_level", None)  # 该 def 子分支 后续默认 is_end = 0，如果 kwargs 还会被 继续使用 的话。


# %%

def U_dir(U_name, is_save,
          **kwargs, ):  # kwargs 是 z

    folder_address = gan_Uz_dir_address(U_name, **kwargs, )
    # print(folder_address)

    if is_save == 1:
        if not os.path.isdir(folder_address):
            os.makedirs(folder_address)

    return folder_address


# %%

def U_amp_plot_address_and_title(U_name, folder_address, img_name_extension,
                                 **kwargs, ):  # kwargs 是 z
    # %%
    # 绘制 U_amp
    suffix = kwargs.get("suffix", '_amp')
    kwargs.pop("suffix", None)
    # %%
    # 生成 要储存的 图片名 和 地址
    U_amp_full_name, U_amp_plot_address = gan_Uz_plot_address(folder_address, img_name_extension,
                                                              U_name, suffix, **kwargs)
    # %%
    # 生成 图片中的 title
    U_amp_title = gan_Uz_title(U_name, suffix, **kwargs)  # 增加 后缀 "_amp" 或 "_phase"

    return U_amp_plot_address, U_amp_title


# %%

def U_amp_error_plot_address_and_title(U_name, folder_address, img_name_extension,
                                       **kwargs, ):  # kwargs 是 z
    # %%
    # 绘制 U_amp
    suffix = kwargs.get("suffix", '_amp_error')
    kwargs.pop("suffix", None)
    # %%
    # 生成 要储存的 图片名 和 地址
    U_amp_error_full_name, U_amp_error_plot_address = gan_Uz_plot_address(folder_address, img_name_extension,
                                                                          U_name, suffix, **kwargs)
    # %%
    # 生成 图片中的 title
    U_amp_error_title = gan_Uz_title(U_name, suffix, **kwargs)  # 增加 后缀 "_amp" 或 "_phase"

    return U_amp_error_plot_address, U_amp_error_title


# %%

def U_phase_plot_address_and_title(U_name, folder_address, img_name_extension,
                                   **kwargs, ):
    # %%
    # 绘制 U_phase
    suffix = kwargs.get("suffix", '_phase')
    kwargs.pop("suffix", None)
    # %%
    # 生成 要储存的 图片名 和 地址
    U_phase_full_name, U_phase_plot_address = gan_Uz_plot_address(folder_address, img_name_extension,
                                                                  U_name, suffix, **kwargs)
    # %%
    # 生成 图片中的 title
    U_phase_title = gan_Uz_title(U_name, suffix, **kwargs)  # 增加 后缀 "_amp" 或 "_phase"

    return U_phase_plot_address, U_phase_title


# %%

def U_phase_error_plot_address_and_title(U_name, folder_address, img_name_extension,
                                         **kwargs, ):
    # %%
    # 绘制 U_phase
    suffix = kwargs.get("suffix", '_phase_error')
    kwargs.pop("suffix", None)
    # %%
    # 生成 要储存的 图片名 和 地址
    U_phase_error_full_name, U_phase_error_plot_address = gan_Uz_plot_address(folder_address, img_name_extension,
                                                                              U_name, suffix, **kwargs)
    # %%
    # 生成 图片中的 title
    U_phase_error_title = gan_Uz_title(U_name, suffix, **kwargs)  # 增加 后缀 "_amp" 或 "_phase"

    return U_phase_error_plot_address, U_phase_error_title


# %%

def U_amp_plot_save(folder_address,
                    U, U_name,
                    img_name_extension,
                    is_save_txt,
                    # %%
                    zj_plot_2d, sample, size_PerPixel,
                    is_save, dpi, size_fig,
                    # %%
                    cmap_2d, ticks_num, is_contourf,
                    is_title_on, is_axes_on, is_mm, is_propagation,
                    fontsize, font,
                    # %%
                    is_self_colorbar, is_colorbar_on, is_energy,
                    # %%
                    **kwargs, ):  # args 是 z 或 ()、is_save_txt、is_no_data_save

    U_amp_plot_address, U_amp_title = U_amp_plot_address_and_title(U_name, folder_address, img_name_extension,
                                                                   **kwargs, )
    # %%

    plot_2d(zj_plot_2d, sample, size_PerPixel,  # 防止 kwargs 里 出现 关键字 zj 后重名
            U, U_amp_plot_address, U_amp_title,
            is_save, dpi, size_fig,
            cmap_2d, ticks_num, is_contourf,
            is_title_on, is_axes_on, is_mm, is_propagation,
            fontsize, font,
            is_self_colorbar, is_colorbar_on, is_energy,
            **kwargs)

    if kwargs.get("is_no_data_save", 0) == 0:
        kwargs["suffix"] = kwargs.get("suffix", '_amp')
        U_address, ugHGU = U_save(U, U_name, folder_address,
                                  is_save, is_save_txt,
                                  **kwargs, )

    return U_amp_plot_address, U_amp_title


# %%

def U_amp_error_plot(folder_address,
                     U, U_name,
                     img_name_extension,
                     # %%
                     zj, sample, size_PerPixel,
                     is_save, dpi, size_fig,
                     # %%
                     cmap_2d, ticks_num, is_contourf,
                     is_title_on, is_axes_on, is_mm, is_propagation,
                     fontsize, font,
                     # %%
                     is_self_colorbar, is_colorbar_on, is_energy,
                     # %%
                     **kwargs, ):  # args 是 z 或 ()

    U_amp_error_plot_address, U_amp_error_title = U_amp_error_plot_address_and_title(U_name, folder_address,
                                                                                     img_name_extension,
                                                                                     **kwargs, )
    # %%

    plot_2d(zj, sample, size_PerPixel,
            U, U_amp_error_plot_address, U_amp_error_title,
            is_save, dpi, size_fig,
            cmap_2d, ticks_num, is_contourf,
            is_title_on, is_axes_on, is_mm, is_propagation,
            fontsize, font,
            is_self_colorbar, is_colorbar_on, is_energy,
            **kwargs)

    return U_amp_error_plot_address, U_amp_error_title


# %%

def U_phase_plot_save(folder_address,
                      U, U_name,
                      img_name_extension,
                      is_save_txt,
                      # %%
                      zj_plot_2d, sample, size_PerPixel,
                      is_save, dpi, size_fig,
                      # %%
                      cmap_2d, ticks_num, is_contourf,
                      is_title_on, is_axes_on, is_mm, is_propagation,
                      fontsize, font,
                      # %%
                      is_self_colorbar, is_colorbar_on,
                      # %%
                      **kwargs, ):  # args 是 z 或 ()、is_save_txt、is_no_data_save

    U_phase_plot_address, U_phase_title = U_phase_plot_address_and_title(U_name, folder_address, img_name_extension,
                                                                         **kwargs, )
    # %%

    plot_2d(zj_plot_2d, sample, size_PerPixel,  # 防止 kwargs 里 出现 关键字 zj 后重名
            U, U_phase_plot_address, U_phase_title,
            is_save, dpi, size_fig,
            cmap_2d, ticks_num, is_contourf,
            is_title_on, is_axes_on, is_mm, is_propagation,
            fontsize, font,
            is_self_colorbar, is_colorbar_on, 0,
            **kwargs)  # 相位 不能有 is_energy = 1

    if kwargs.get("is_no_data_save", 0) == 0:
        suffix = '_phase'
        U_address, ugHGU = U_save(U, U_name, folder_address,
                                  is_save, is_save_txt,
                                  suffix=suffix, **kwargs, )

    return U_phase_plot_address, U_phase_title


# %%

def U_phase_error_plot(folder_address,
                       U, U_name,
                       img_name_extension,
                       # %%
                       zj, sample, size_PerPixel,
                       is_save, dpi, size_fig,
                       # %%
                       cmap_2d, ticks_num, is_contourf,
                       is_title_on, is_axes_on, is_mm, is_propagation,
                       fontsize, font,
                       # %%
                       is_self_colorbar, is_colorbar_on,
                       # %%
                       **kwargs, ):  # args 是 z 或 ()

    U_phase_error_plot_address, U_phase_error_title = U_phase_error_plot_address_and_title(U_name, folder_address,
                                                                                           img_name_extension,
                                                                                           **kwargs, )
    # %%

    plot_2d(zj, sample, size_PerPixel,
            U, U_phase_error_plot_address, U_phase_error_title,
            is_save, dpi, size_fig,
            cmap_2d, ticks_num, is_contourf,
            is_title_on, is_axes_on, is_mm, is_propagation,
            fontsize, font,
            is_self_colorbar, is_colorbar_on, 0,
            **kwargs)  # 相位 不能有 is_energy = 1

    return U_phase_error_plot_address, U_phase_error_title


# %%

def U_plot(folder_address,
           U, U_name,
           img_name_extension,
           is_save_txt,
           # %%
           sample, size_PerPixel,
           is_save, dpi, size_fig,
           # %%
           cmap_2d, ticks_num, is_contourf,
           is_title_on, is_axes_on, is_mm,
           fontsize, font,
           # %%
           is_colorbar_on, is_energy,  # 默认无法 外界设置 vmax 和 vmin，因为 同时画 振幅 和 相位 得 传入 2*2 个 v
           # %%                          何况 一般默认 is_self_colorbar = 1...
           **kwargs, ):  # args 是 z 或 ()、is_save_txt、is_no_data_save

    U_amp_plot_address = U_amp_plot_save(folder_address,
                                         np.abs(U), U_name,
                                         img_name_extension,
                                         is_save_txt,
                                         # %%
                                         [], sample, size_PerPixel,
                                         is_save, dpi, size_fig,
                                         # %%
                                         cmap_2d, ticks_num, is_contourf,
                                         is_title_on, is_axes_on, is_mm, 0,
                                         fontsize, font,
                                         # %%
                                         0, is_colorbar_on, is_energy,
                                         # %% 何况 一般默认 is_self_colorbar = 1...
                                         **kwargs, )

    U_phase_plot_address = U_phase_plot_save(folder_address,
                                             np.angle(U), U_name,
                                             img_name_extension,
                                             is_save_txt,
                                             # %%
                                             [], sample, size_PerPixel,
                                             is_save, dpi, size_fig,
                                             # %%
                                             cmap_2d, ticks_num, is_contourf,
                                             is_title_on, is_axes_on, is_mm, 0,
                                             fontsize, font,
                                             # %%
                                             0, is_colorbar_on,
                                             # %% 何况 一般默认 is_self_colorbar = 1...
                                             **kwargs, )

    return U_amp_plot_address, U_phase_plot_address


# %%

def U_error_plot(folder_address,
                 U, U_0, ugHGU,
                 img_name_extension,
                 # %%
                 sample, size_PerPixel,
                 is_save, dpi, size_fig,
                 # %%
                 cmap_2d, ticks_num, is_contourf,
                 is_title_on, is_axes_on, is_mm,
                 fontsize, font,
                 # %%
                 is_colorbar_on, is_energy,  # 默认无法 外界设置 vmax 和 vmin，因为 同时画 振幅 和 相位 得 传入 2*2 个 v
                 # %%                          何况 一般默认 is_self_colorbar = 1...
                 **kwargs, ):  # args 是 z 或 ()

    from fun_global_var import fkey

    U_amp_error = np.abs(U) - np.abs(U_0)
    U_phase_error = np.angle(U) - np.angle(U_0)

    U_amp_error_plot_address = U_amp_error_plot(folder_address,
                                                U_amp_error, fkey(ugHGU),
                                                img_name_extension,
                                                # %%
                                                [], sample, size_PerPixel,
                                                is_save, dpi, size_fig,
                                                # %%
                                                cmap_2d, ticks_num, is_contourf,
                                                is_title_on, is_axes_on, is_mm, 0,
                                                fontsize, font,
                                                # %%
                                                0, is_colorbar_on, is_energy,
                                                # %% 何况 一般默认 is_self_colorbar = 1...
                                                **kwargs, )

    U_phase_error_plot_address = U_phase_error_plot(folder_address,
                                                    U_phase_error, fkey(ugHGU),
                                                    img_name_extension,
                                                    # %%
                                                    [], sample, size_PerPixel,
                                                    is_save, dpi, size_fig,
                                                    # %%
                                                    cmap_2d, ticks_num, is_contourf,
                                                    is_title_on, is_axes_on, is_mm, 0,
                                                    fontsize, font,
                                                    # %%
                                                    0, is_colorbar_on,
                                                    # %% 何况 一般默认 is_self_colorbar = 1...
                                                    **kwargs, )

    return U_amp_error_plot_address, U_phase_error_plot_address


# %%

def U_plot_save(U, U_name, is_print,
                img_name_extension,
                # %%
                size_PerPixel,
                is_save, is_save_txt, dpi, size_fig,
                # %%
                cmap_2d, ticks_num, is_contourf,
                is_title_on, is_axes_on, is_mm,
                fontsize, font,
                # %%
                is_colorbar_on, is_energy,  # 默认无法 外界设置 vmax 和 vmin，因为 同时画 振幅 和 相位 得 传入 2*2 个 v
                # %%                          何况 一般默认 is_self_colorbar = 1...
                **kwargs, ):  # **kwargs = z

    if is_print == 1:
        U_energy_print(U, U_name, is_print,
                       **kwargs, )
    elif is_print == 2:
        is_end, add_level = kwargs.get("is_end", 0), kwargs.get("add_level", 0)
        kwargs.pop("is_end", None);
        kwargs.pop("add_level", None)  # 该 def 子分支 后续默认 is_end = 0，如果 kwargs 还会被 继续使用 的话。

        U_energy_print(U, U_name, is_print,
                       **kwargs, )

        kwargs["is_end"] = is_end
        # 这里不能单纯地加 is_end=is_end，否则 会报错 U_rsd_print() got multiple values for keyword argument 'is_end'
        U_rsd_print(U, U_name, is_print,
                    **kwargs, )
        kwargs.pop("is_end", None)

    folder_address = U_dir(U_name, is_save, **kwargs, )

    # %%
    # 绘图：U

    kwargs["is_no_data_save"] = 1
    U_amp_plot_address, U_phase_plot_address = U_plot(folder_address,
                                                      U, U_name,
                                                      img_name_extension,
                                                      is_save_txt,
                                                      # %%
                                                      1, size_PerPixel,
                                                      is_save, dpi, size_fig,
                                                      cmap_2d, ticks_num, is_contourf,
                                                      is_title_on, is_axes_on, is_mm,
                                                      fontsize, font,
                                                      is_colorbar_on, is_energy,
                                                      # %%
                                                      **kwargs, )
    kwargs.pop("is_no_data_save", None)

    # %%
    # 储存 U 到 txt 文件

    U_address, ugHGU = U_save(U, U_name, folder_address,
                              is_save, is_save_txt, **kwargs, )

    return folder_address
    # return folder_address, U_address, U_amp_plot_address, U_phase_plot_address


# %%

def U_error_plot_save(U, U_0, ugHGU, is_print,
                      img_name_extension,
                      # %%
                      size_PerPixel,
                      is_save, is_save_txt, dpi, size_fig,
                      # %%
                      cmap_2d, ticks_num, is_contourf,
                      is_title_on, is_axes_on, is_mm,
                      fontsize, font,
                      # %%
                      is_colorbar_on, is_energy,  # 默认无法 外界设置 vmax 和 vmin，因为 同时画 振幅 和 相位 得 传入 2*2 个 v
                      # %%                          何况 一般默认 is_self_colorbar = 1...
                      **kwargs, ):  # **kwargs = z

    from fun_global_var import fkey

    info = ugHGU + "_先取模或相位_后误差"
    is_print and print(tree_print(kwargs.get("is_end", 0), add_level=2) + info)
    kwargs.pop("is_end", None);
    kwargs.pop("add_level", None)  # 该 def 子分支 后续默认 is_end = 0，如果 kwargs 还会被 继续使用 的话。

    U_error = U - U_0
    U_error_name = fkey(ugHGU) + "_error"

    folder_address = U_dir(U_error_name, is_save, **kwargs, )

    # %%
    U_amp_error = np.abs(U) - np.abs(U_0)
    U_amp_error_name = fkey(ugHGU) + "_amp_error"
    U_energy_print(U_amp_error, U_amp_error_name, is_print,
                   **kwargs, )
    U_rsd_print(U_amp_error, U_amp_error_name, is_print,
                **kwargs, )

    U_phase_error = np.angle(U) - np.angle(U_0)
    U_phase_error_name = fkey(ugHGU) + "_phase_error"
    if is_print == 1:
        kwargs["is_end"] = 1
        U_energy_print(U_phase_error, U_phase_error_name, is_print,
                       **kwargs, )
    elif is_print == 2:
        U_energy_print(U_phase_error, U_phase_error_name, is_print,
                       **kwargs, )
        kwargs["is_end"] = 1
        U_rsd_print(U_phase_error, U_phase_error_name, is_print,
                    **kwargs, )
    kwargs.pop("is_end", None)

    # %%
    # 绘图：U

    cmap_2d = "RdBu"
    # diverging colormaps:
    # "coolwarm", "bwr", "seismic", "Spectral", "RdBu", "RdYIBu"

    U_amp_error_plot_address, U_phase_error_plot_address = U_error_plot(folder_address,
                                                                        U, U_0, ugHGU,
                                                                        img_name_extension,
                                                                        # %%
                                                                        1, size_PerPixel,
                                                                        is_save, dpi, size_fig,
                                                                        cmap_2d, ticks_num, is_contourf,
                                                                        is_title_on, is_axes_on, is_mm,
                                                                        fontsize, font,
                                                                        is_colorbar_on, is_energy,
                                                                        # %%
                                                                        **kwargs, )

    # %%
    # 储存 U 到 txt 文件

    U_address, ugHGU = U_save(U_amp_error, U_amp_error_name, folder_address,
                              is_save, is_save_txt, **kwargs, )
    U_address, ugHGU = U_save(U_phase_error, U_phase_error_name, folder_address,
                              is_save, is_save_txt, **kwargs, )

    U_amp_error_energy = np.sum(np.abs(U_amp_error) ** 2)
    return folder_address, U_amp_error_energy


def GHU_plot_save(G, G_name, is_energy_evolution_on,  # 默认 全自动 is_auto_seq_and_z = 1
                  G_energy, is_print,
                  H, H_name,
                  U, U_name,  # U 容易重名，得在上一级就处理。
                  U_energy,
                  img_name_extension,
                  # %%
                  zj, sample, size_PerPixel,
                  is_save, is_save_txt, dpi, size_fig,
                  # %%
                  color_1d, cmap_2d,
                  ticks_num, is_contourf,
                  is_title_on, is_axes_on, is_mm,
                  fontsize, font,
                  # %%
                  is_colorbar_on, is_energy,  # 默认无法 外界设置 vmax 和 vmin，因为 同时画 振幅 和 相位 得 传入 2*2 个 v
                  # %%                          何况 一般默认 is_self_colorbar = 1...
                  z, **kwargs, ):  # 默认必须给 z，kwargs 里是 is_end
    is_end, add_level = kwargs.get("is_end", 0), kwargs.get("add_level", 0)
    kwargs.pop("is_end", None);
    kwargs.pop("add_level", None)
    # %%
    kwargs['p_dir'] = 'GHU_XY'
    # %%
    folder_address = U_plot_save(G, G_name, 0,
                                 img_name_extension,
                                 # %%
                                 size_PerPixel,
                                 is_save, is_save_txt, dpi, size_fig,
                                 # %%
                                 cmap_2d, ticks_num, is_contourf,
                                 is_title_on, is_axes_on, is_mm,
                                 fontsize, font,
                                 # %%
                                 is_colorbar_on, is_energy,  # 默认无法 外界设置 vmax 和 vmin，因为 同时画 振幅 和 相位 得 传入 2*2 个 v
                                 # %%                          何况 一般默认 is_self_colorbar = 1...
                                 z=z, **kwargs, )

    folder_address = U_plot_save(H, H_name, 0,
                                 img_name_extension,
                                 # %%
                                 size_PerPixel,
                                 is_save, is_save_txt, dpi, size_fig,
                                 # %%
                                 cmap_2d, ticks_num, is_contourf,
                                 is_title_on, is_axes_on, is_mm,
                                 fontsize, font,
                                 # %%
                                 is_colorbar_on, is_energy,  # 默认无法 外界设置 vmax 和 vmin，因为 同时画 振幅 和 相位 得 传入 2*2 个 v
                                 # %%                          何况 一般默认 is_self_colorbar = 1...
                                 z=z, **kwargs, )

    folder_address = U_plot_save(U, U_name, is_print,
                                 img_name_extension,
                                 # %%
                                 size_PerPixel,
                                 is_save, is_save_txt, dpi, size_fig,
                                 # %%
                                 cmap_2d, ticks_num, is_contourf,
                                 is_title_on, is_axes_on, is_mm,
                                 fontsize, font,
                                 # %%
                                 is_colorbar_on, is_energy,  # 默认无法 外界设置 vmax 和 vmin，因为 同时画 振幅 和 相位 得 传入 2*2 个 v
                                 # %%                          何况 一般默认 is_self_colorbar = 1...
                                 z=z, is_end=is_end, **kwargs, )

    if is_energy_evolution_on == 1:
        kwargs['p_dir'] = 'GU_energy(z)'
        # %% G
        U_energy_plot_save(G_energy, G_name,
                           img_name_extension,
                           is_save_txt,
                           # %%
                           zj, sample, size_PerPixel,
                           is_save, dpi, Get("size_fig_x"), Get("size_fig_y"),
                           color_1d, ticks_num, is_title_on, is_axes_on, is_mm,
                           fontsize, font,  # 默认无法 外界设置，只能 自动设置 y 轴 max 和 min 了（不是 但 类似 colorbar），还有 is_energy
                           # %%
                           z, **kwargs, )
        # %% U
        U_energy_plot_save(U_energy, U_name,
                           img_name_extension,
                           is_save_txt,
                           # %%
                           zj, sample, size_PerPixel,
                           is_save, dpi, Get("size_fig_x"), Get("size_fig_y"),
                           color_1d, ticks_num, is_title_on, is_axes_on, is_mm,
                           fontsize, font,  # 默认无法 外界设置，只能 自动设置 y 轴 max 和 min 了（不是 但 类似 colorbar），还有 is_energy
                           # %%
                           z, **kwargs, )


# %%

def U_slices_plot_save(folder_address,
                       U_XZ, U_XZ_name,
                       U_YZ, U_YZ_name,
                       img_name_extension,
                       is_save_txt,
                       # %%
                       zj, sample, size_PerPixel,
                       is_save, dpi, size_fig,
                       # %%
                       cmap_2d, ticks_num, is_contourf,
                       is_title_on, is_axes_on, is_mm,
                       fontsize, font,
                       # %%
                       is_colorbar_on, is_energy,
                       # %%
                       X, Y, **kwargs, ):  # args 是 X 和 Y， is_save_txt、is_no_data_save
    if kwargs.get("is_colorbar_log", 0) == -1:
        v_kwargs = {}
    else:
        U_YZ_amp = np.abs(U_YZ) if is_energy != 1 else np.abs(U_YZ) ** 2
        U_XZ_amp = np.abs(U_XZ) if is_energy != 1 else np.abs(U_XZ) ** 2
        U_YZ_XZ_amp_max = np.max([np.max(U_YZ_amp), np.max(U_XZ_amp)])
        U_YZ_XZ_amp_min = np.min([np.min(U_YZ_amp), np.min(U_XZ_amp)])
        v_kwargs = {
            "vmax": U_YZ_XZ_amp_max,
            "vmin": U_YZ_XZ_amp_min,
        }

    is_no_data_save = kwargs.get("is_no_data_save", 0)
    kwargs["is_no_data_save"] = 1
    U_amp_plot_save(folder_address,
                    np.abs(U_YZ), U_YZ_name,  # 不能是 U_YZ_amp，因为 不能包含平方 np.abs(U_YZ_amp) ** 2，因为 plot_2d 里还会平方
                    img_name_extension,
                    is_save_txt,
                    # %%
                    zj, sample, size_PerPixel,
                    is_save, dpi, size_fig,
                    # %%
                    cmap_2d, ticks_num, is_contourf,
                    is_title_on, is_axes_on, is_mm, 1,
                    fontsize, font,
                    # %%
                    0, is_colorbar_on, is_energy,
                    **v_kwargs,
                    # %%
                    z=X, **kwargs, )

    U_amp_plot_save(folder_address,
                    np.abs(U_XZ), U_XZ_name,
                    img_name_extension,
                    is_save_txt,
                    # %%
                    zj, sample, size_PerPixel,
                    is_save, dpi, size_fig,
                    # %%
                    cmap_2d, ticks_num, is_contourf,
                    is_title_on, is_axes_on, is_mm, 1,
                    fontsize, font,
                    # %%
                    0, is_colorbar_on, is_energy,
                    **v_kwargs,
                    # %%
                    z=Y, **kwargs, )

    if kwargs.get("is_colorbar_log", 0) == -1:
        v_kwargs = {}
    else:
        U_YZ_phase = np.angle(U_YZ)
        U_XZ_phase = np.angle(U_XZ)
        U_YZ_XZ_phase_max = np.max([np.max(U_YZ_phase), np.max(U_XZ_phase)])
        U_YZ_XZ_phase_min = np.min([np.min(U_YZ_phase), np.min(U_XZ_phase)])
        v_kwargs = {
            "vmax": U_YZ_XZ_phase_max,
            "vmin": U_YZ_XZ_phase_min,
        }

    U_phase_plot_save(folder_address,
                      np.angle(U_YZ), U_YZ_name,
                      img_name_extension,
                      is_save_txt,
                      # %%
                      zj, sample, size_PerPixel,
                      is_save, dpi, size_fig,
                      # %%
                      cmap_2d, ticks_num, is_contourf,
                      is_title_on, is_axes_on, is_mm, 1,
                      fontsize, font,
                      # %%
                      0, is_colorbar_on,
                      **v_kwargs,
                      # %%
                      z=X, **kwargs, )

    U_phase_plot_save(folder_address,
                      np.angle(U_XZ), U_XZ_name,
                      img_name_extension,
                      is_save_txt,
                      # %%
                      zj, sample, size_PerPixel,
                      is_save, dpi, size_fig,
                      # %%
                      cmap_2d, ticks_num, is_contourf,
                      is_title_on, is_axes_on, is_mm, 1,
                      fontsize, font,
                      # %%
                      0, is_colorbar_on,
                      **v_kwargs,
                      # %%
                      z=Y, **kwargs, )

    kwargs["is_no_data_save"] = is_no_data_save
    U_save(U_XZ, U_XZ_name, folder_address,
           is_save, is_save_txt,
           z=X, suffix="_XZ", **kwargs, )
    U_save(U_YZ, U_YZ_name, folder_address,
           is_save, is_save_txt,
           z=Y, suffix="_XZ", **kwargs, )
    U_save(zj, 'zj', folder_address,
           is_save, is_save_txt,
           z=zj[-1], **kwargs, )
    # U_name = U_XZ_name.replace("_XZ", '')
    # suffix = "_zj"
    # U_save(zj, U_name + suffix, folder_address,
    #        is_save, is_save_txt,
    #        z=zj[-1], suffix=suffix, **kwargs, )

    if kwargs.get("is_colorbar_log", 0) == -1:
        return 0, 0, 0, 0
    else:
        return U_YZ_XZ_amp_max, U_YZ_XZ_amp_min, U_YZ_XZ_phase_max, U_YZ_XZ_phase_min


# %%

def U_selects_plot_save(folder_address,
                        U_1, U_1_name,
                        U_2, U_2_name,
                        U_f, U_f_name,
                        U_e, U_e_name,
                        img_name_extension,
                        is_save_txt,
                        # %%
                        sample, size_PerPixel,
                        is_save, dpi, size_fig,
                        # %%
                        cmap_2d, ticks_num, is_contourf,
                        is_title_on, is_axes_on, is_mm,
                        fontsize, font,
                        # %%
                        is_colorbar_on, is_energy, is_show_structure_face,
                        # %%
                        z_1, z_2, z_f, z_e,
                        **kwargs, ):  # kwargs 是 is_save_txt、is_no_data_save

    if kwargs.get("is_colorbar_log", 0) == -1:
        v_kwargs = {}
    else:
        U_1_amp = np.abs(U_1) if is_energy != 1 else np.abs(U_1) ** 2
        U_2_amp = np.abs(U_2) if is_energy != 1 else np.abs(U_2) ** 2
        U_f_amp = np.abs(U_f) if is_energy != 1 else np.abs(U_f) ** 2
        U_e_amp = np.abs(U_e) if is_energy != 1 else np.abs(U_e) ** 2
        if is_show_structure_face == 1:
            U_amps_max = np.max([np.max(U_1_amp), np.max(U_2_amp),
                                 np.max(U_f_amp), np.max(U_e_amp)])
            U_amps_min = np.min([np.min(U_1_amp), np.min(U_2_amp),
                                 np.min(U_f_amp), np.min(U_e_amp)])
        else:
            U_amps_max = np.max([np.max(U_1_amp), np.max(U_2_amp)])
            U_amps_min = np.min([np.min(U_1_amp), np.min(U_2_amp)])
        v_kwargs = {
            "vmax": U_amps_max,
            "vmin": U_amps_min,
        }

    is_no_data_save = kwargs.get("is_no_data_save", 0)
    kwargs["is_no_data_save"] = 1
    U_amp_plot_save(folder_address,
                    np.abs(U_1), U_1_name,  # 不能是 U_1_amp，因为 不能包含平方 np.abs(U_1) ** 2，因为 plot_2d 里还会平方
                    img_name_extension,
                    is_save_txt,
                    # %%
                    [], sample, size_PerPixel,
                    is_save, dpi, size_fig,
                    # %%
                    cmap_2d, ticks_num, is_contourf,
                    is_title_on, is_axes_on, is_mm, 0,
                    fontsize, font,
                    # %%
                    0, is_colorbar_on, is_energy,
                    **v_kwargs,
                    # %%
                    z=z_1, **kwargs, )

    U_amp_plot_save(folder_address,
                    np.abs(U_2), U_2_name,
                    img_name_extension,
                    is_save_txt,
                    # %%
                    [], sample, size_PerPixel,
                    is_save, dpi, size_fig,
                    # %%
                    cmap_2d, ticks_num, is_contourf,
                    is_title_on, is_axes_on, is_mm, 0,
                    fontsize, font,
                    # %%
                    0, is_colorbar_on, is_energy,
                    **v_kwargs,
                    # %%
                    z=z_2, **kwargs, )

    if is_show_structure_face == 1:
        U_amp_plot_save(folder_address,
                        np.abs(U_f), U_f_name,
                        img_name_extension,
                        is_save_txt,
                        # %%
                        [], sample, size_PerPixel,
                        is_save, dpi, size_fig,
                        # %%
                        cmap_2d, ticks_num, is_contourf,
                        is_title_on, is_axes_on, is_mm, 0,
                        fontsize, font,
                        # %%
                        0, is_colorbar_on, is_energy,
                        **v_kwargs,
                        # %%
                        z=z_f, **kwargs, )

        U_amp_plot_save(folder_address,
                        np.abs(U_e), U_e_name,
                        img_name_extension,
                        is_save_txt,
                        # %%
                        [], sample, size_PerPixel,
                        is_save, dpi, size_fig,
                        # %%
                        cmap_2d, ticks_num, is_contourf,
                        is_title_on, is_axes_on, is_mm, 0,
                        fontsize, font,
                        # %%
                        0, is_colorbar_on, is_energy,
                        **v_kwargs,
                        # %%
                        z=z_e, **kwargs, )

    if kwargs.get("is_colorbar_log", 0) == -1:
        v_kwargs = {}
    else:
        U_1_phase = np.angle(U_1)
        U_2_phase = np.angle(U_2)
        U_f_phase = np.angle(U_f)
        U_e_phase = np.angle(U_e)
        if is_show_structure_face == 1:
            U_phases_max = np.max([np.max(U_1_phase), np.max(U_2_phase),
                                   np.max(U_f_phase), np.max(U_e_phase)])
            U_phases_min = np.min([np.min(U_1_phase), np.min(U_2_phase),
                                   np.min(U_f_phase), np.min(U_e_phase)])
        else:
            U_phases_max = np.max([np.max(U_1_phase), np.max(U_2_phase)])
            U_phases_min = np.min([np.min(U_1_phase), np.min(U_2_phase)])
        v_kwargs = {
            "vmax": U_phases_max,
            "vmin": U_phases_min,
        }

    U_phase_plot_save(folder_address,
                      np.angle(U_1), U_1_name,
                      img_name_extension,
                      is_save_txt,
                      # %%
                      [], sample, size_PerPixel,
                      is_save, dpi, size_fig,
                      # %%
                      cmap_2d, ticks_num, is_contourf,
                      is_title_on, is_axes_on, is_mm, 0,
                      fontsize, font,
                      # %%
                      0, is_colorbar_on,
                      **v_kwargs,
                      # %%
                      z=z_1, **kwargs, )

    U_phase_plot_save(folder_address,
                      np.angle(U_2), U_2_name,
                      img_name_extension,
                      is_save_txt,
                      # %%
                      [], sample, size_PerPixel,
                      is_save, dpi, size_fig,
                      # %%
                      cmap_2d, ticks_num, is_contourf,
                      is_title_on, is_axes_on, is_mm, 0,
                      fontsize, font,
                      # %%
                      0, is_colorbar_on,
                      **v_kwargs,
                      # %%
                      z=z_2, **kwargs, )

    if is_show_structure_face == 1:
        U_phase_plot_save(folder_address,
                          np.angle(U_f), U_f_name,
                          img_name_extension,
                          is_save_txt,
                          # %%
                          [], sample, size_PerPixel,
                          is_save, dpi, size_fig,
                          # %%
                          cmap_2d, ticks_num, is_contourf,
                          is_title_on, is_axes_on, is_mm, 0,
                          fontsize, font,
                          # %%
                          0, is_colorbar_on,
                          **v_kwargs,
                          # %%
                          z=z_f, **kwargs, )

        U_phase_plot_save(folder_address,
                          np.angle(U_e), U_e_name,
                          img_name_extension,
                          is_save_txt,
                          # %%
                          [], sample, size_PerPixel,
                          is_save, dpi, size_fig,
                          # %%
                          cmap_2d, ticks_num, is_contourf,
                          is_title_on, is_axes_on, is_mm, 0,
                          fontsize, font,
                          # %%
                          0, is_colorbar_on,
                          **v_kwargs,
                          # %%
                          z=z_e, **kwargs, )
    kwargs["is_no_data_save"] = is_no_data_save
    U_save(U_1, U_1_name, folder_address,
           is_save, is_save_txt,
           z=z_1, **kwargs, )
    U_save(U_2, U_2_name, folder_address,
           is_save, is_save_txt,
           z=z_2, **kwargs, )
    U_save(U_f, U_f_name, folder_address,
           is_save, is_save_txt,
           z=z_f, **kwargs, )
    U_save(U_e, U_e_name, folder_address,
           is_save, is_save_txt,
           z=z_e, **kwargs, )

    if kwargs.get("is_colorbar_log", 0) == -1:
        return 0, 0, 0, 0
    else:
        return U_amps_max, U_amps_min, U_phases_max, U_phases_min


# %%

def U_amps_z_plot_save(folder_address,
                       U, U_name,
                       img_name_extension,
                       is_save_txt,
                       # %%
                       sample, size_PerPixel,
                       is_save, dpi, size_fig,
                       # %%
                       cmap_2d, ticks_num, is_contourf,
                       is_title_on, is_axes_on, is_mm,
                       fontsize, font,
                       # %%
                       is_colorbar_on, is_energy,  # 默认无法 外界设置 vmax 和 vmin，默认 自动统一 colorbar
                       # %%
                       z_stored, is_animated,
                       duration, fps, loop,
                       z, **kwargs, ):  # 必须要传 z 序列、is_animated 进来；kwargs 是 is_save_txt, is_no_data_save、is_colorbar_log
    # 其实不用传 z 进来，直接用 z_stored[-1] 就行，不过这样保险点
    if kwargs.get("is_colorbar_log", 0) == -1:
        v_kwargs = {}
    else:
        U_amp_max = np.max(U) if is_energy != 1 else np.max(U) ** 2  # U 已经是 amp 了
        U_amp_min = np.min(U) if is_energy != 1 else np.min(U) ** 2
        v_kwargs = {
            "vmax": U_amp_max,
            "vmin": U_amp_min,
        }
    # global imgs_address_list, titles_list
    imgs_address_list = []
    titles_list = []
    is_no_data_save = kwargs.get("is_no_data_save", 0)
    kwargs["is_no_data_save"] = 1
    for sheet_stored_th in range(U.shape[2]):
        U_amp_plot_address, U_amp_title = U_amp_plot_save(folder_address,
                                                          # 因为 要返回的话，太多了；返回一个 又没啥意义，而且 返回了 基本也用不上
                                                          U[:, :, sheet_stored_th], U_name,
                                                          img_name_extension,
                                                          is_save_txt,
                                                          # %%
                                                          [], sample, size_PerPixel,
                                                          is_save, dpi, size_fig,
                                                          # %%
                                                          cmap_2d, ticks_num, is_contourf,
                                                          is_title_on, is_axes_on, is_mm, 0,
                                                          fontsize, font,
                                                          # %%
                                                          0, is_colorbar_on, is_energy,
                                                          **v_kwargs,
                                                          # 默认无法 外界设置 vmax 和 vmin，默认 自动统一 colorbar
                                                          # %%
                                                          z=z_stored[sheet_stored_th], **kwargs, )
        imgs_address_list.append(U_amp_plot_address)
        titles_list.append(U_amp_title)  # 每张图片都用单独list的形式加入到图片序列中
    kwargs["is_no_data_save"] = is_no_data_save

    if is_save == 1:  # 只有 储存后，才能根据 储存的图片 生成 gif

        """ plot2d 无法多线程，因为会挤占 同一个 fig 这个 全局的画布资源？ 注释了 plt.show() 也没用，应该不是它的锅。
        不过其实可以在 U_amp_plot 里面搞多线程，因为 获取 address 和 title 不是全局的 """
        # def fun1(for_th, fors_num, *arg, **kwargs, ):
        #     U_amp_plot_address, U_amp_title = U_amp_plot_save(U0_name, folder_address, is_auto_seq_and_z,
        #                                                  # 因为 要返回的话，太多了；返回一个 又没啥意义，而且 返回了 基本也用不上
        #                                                  U[:, :, for_th], U_name, method,
        #                                                  img_name_extension,
        #                                                  # %%
        #                                                  [], sample, size_PerPixel,
        #                                                  is_save, dpi, size_fig,
        #                                                  # %%
        #                                                  cmap_2d, ticks_num, is_contourf,
        #                                                  is_title_on, is_axes_on, is_mm, 0,
        #                                                  fontsize, font,
        #                                                  # %%
        #                                                  0, is_colorbar_on,  # is_self_colorbar = 0，统一 colorbar
        #                                                  is_energy, U_amp_max, U_amp_min,
        #                                                  # 默认无法 外界设置 vmax 和 vmin，默认 自动统一 colorbar
        #                                                  # %%
        #                                                  z_stored[for_th], )
        #     return U_amp_plot_address, U_amp_title
        #
        # def fun2(for_th, fors_num, U_amp_plot_address, U_amp_title, *args, **kwargs, ):
        #     global imgs_address_list, titles_list
        #     imgs_address_list.append(U_amp_plot_address)
        #     titles_list.append(U_amp_title)  # 每张图片都用单独list的形式加入到图片序列中
        #
        # my_thread(10, U.shape[2],
        #           fun1, fun2, noop,
        #           is_ordered=1, is_print=0, )

        if fps > 0: duration = 1 / fps  # 如果传入了 fps，则可 over write duration
        gif_address = imgs_address_list[-1].replace(img_name_extension, ".gif")
        if is_animated == 0:
            imgs2gif_imgio(imgs_address_list, gif_address,
                           duration, fps, loop, )
        elif is_animated == -1:
            imgs2gif_PIL(imgs_address_list, gif_address,
                         duration, fps, loop, )
        else:
            imgs2gif_art(imgs_address_list, gif_address, dpi,
                         duration, fps, loop, )

        if kwargs.get("is_no_data_save", 0) == 0:
            suffix = "_amp"
            U_address, ugHGU = U_save(U, U_name + suffix, folder_address,
                                      is_save, is_save_txt,
                                      z=z, suffix=suffix, **kwargs, )

            suffix = '_z_stored'
            U_address, ugHGU = U_save(z_stored, U_name + suffix, folder_address,
                                      is_save, is_save_txt,
                                      z=z, suffix=suffix, **kwargs, )

        return gif_address


# %%

def U_phases_z_plot_save(folder_address,
                         U, U_name,
                         img_name_extension,
                         is_save_txt,
                         # %%
                         sample, size_PerPixel,
                         is_save, dpi, size_fig,
                         # %%
                         cmap_2d, ticks_num, is_contourf,
                         is_title_on, is_axes_on, is_mm,
                         fontsize, font,
                         # %%
                         is_colorbar_on,  # 默认无法 外界设置 vmax 和 vmin，默认 自动统一 colorbar
                         # %%
                         z_stored, is_animated,
                         duration, fps, loop,
                         z,
                         **kwargs, ):  # 必须要传 z 序列、is_animated 进来， # args 是 is_save_txt、is_no_data_save、is_colorbar_log
    if kwargs.get("is_colorbar_log", 0) == -1:
        v_kwargs = {}
    else:
        U_phase_max = np.max(U)  # U 已经是 phase 了
        U_phase_min = np.min(U)
        v_kwargs = {
            "vmax": U_phase_max,
            "vmin": U_phase_min,
        }
    # global imgs_address_list, titles_list
    imgs_address_list = []
    titles_list = []
    is_no_data_save = kwargs.get("is_no_data_save", 0)
    kwargs["is_no_data_save"] = 1
    for sheet_stored_th in range(U.shape[2]):
        U_phase_plot_address, U_phase_title = U_phase_plot_save(folder_address,
                                                                U[:, :, sheet_stored_th], U_name,
                                                                img_name_extension,
                                                                is_save_txt,
                                                                # %%
                                                                [], sample, size_PerPixel,
                                                                is_save, dpi, size_fig,
                                                                # %%
                                                                cmap_2d, ticks_num, is_contourf,
                                                                is_title_on, is_axes_on, is_mm, 0,
                                                                fontsize, font,
                                                                # %%
                                                                0, is_colorbar_on,  # is_self_colorbar = 0，统一 colorbar
                                                                # %%
                                                                **v_kwargs,
                                                                z=z_stored[sheet_stored_th], **kwargs, )
        imgs_address_list.append(U_phase_plot_address)
        titles_list.append(U_phase_title)  # 每张图片都用单独list的形式加入到图片序列中
    kwargs["is_no_data_save"] = is_no_data_save

    if is_save == 1:  # 只有 储存后，才能根据 储存的图片 生成 gif

        """ plot2d 无法多线程，因为会挤占 同一个 fig 这个 全局的画布资源？ 注释了 plt.show() 也没用，应该不是它的锅。
        不过其实可以在 U_amp_plot 里面搞多线程，因为 获取 address 和 title 不是全局的 """
        # def fun1(for_th, fors_num, *arg, **kwargs, ):
        #     U_phase_plot_address, U_phase_title = U_phase_plot_save(U0_name, folder_address, is_auto_seq_and_z,
        #                                                        U[:, :, for_th], U_name, method,
        #                                                        img_name_extension,
        #                                                        # %%
        #                                                        [], sample, size_PerPixel,
        #                                                        is_save, dpi, size_fig,
        #                                                        # %%
        #                                                        cmap_2d, ticks_num, is_contourf,
        #                                                        is_title_on, is_axes_on, is_mm, 0,
        #                                                        fontsize, font,
        #                                                        # %%
        #                                                        0, is_colorbar_on,  # is_self_colorbar = 0，统一 colorbar
        #                                                        U_phase_max, U_phase_min,
        #                                                        # %%
        #                                                        z_stored[for_th], )
        #     return U_phase_plot_address, U_phase_title
        #
        # def fun2(for_th, fors_num, U_phase_plot_address, U_phase_title, *args, **kwargs, ):
        #     global imgs_address_list, titles_list
        #     imgs_address_list.append(U_phase_plot_address)
        #     titles_list.append(U_phase_title)  # 每张图片都用单独list的形式加入到图片序列中
        #
        # my_thread(10, U.shape[2],
        #           fun1, fun2, noop,
        #           is_ordered=1, is_print=0, )

        if fps > 0: duration = 1 / fps  # 如果传入了 fps，则可 over write duration
        gif_address = imgs_address_list[-1].replace(img_name_extension, ".gif")
        if is_animated == 0:
            imgs2gif_imgio(imgs_address_list, gif_address,
                           duration, fps, loop, )
        elif is_animated == -1:
            imgs2gif_PIL(imgs_address_list, gif_address,
                         duration, fps, loop, )
        else:
            imgs2gif_art(imgs_address_list, gif_address, dpi,
                         duration, fps, loop, )

        if kwargs.get("is_no_data_save", 0) == 0:
            suffix = "_phase"
            U_address, ugHGU = U_save(U, U_name + suffix, folder_address,
                                      is_save, is_save_txt,
                                      z=z, suffix=suffix, **kwargs, )

            suffix = '_z_stored'
            U_address, ugHGU = U_save(z_stored, U_name + suffix, folder_address,
                                      is_save, is_save_txt,
                                      z=z, suffix=suffix, **kwargs, )

        return gif_address


# %%

def U_amp_plot_save_3d_XYz(folder_address,
                           U, U_name,
                           img_name_extension,
                           is_save_txt,
                           # %%
                           sample, size_PerPixel,
                           is_save, dpi, size_fig,
                           elev, azim, alpha,
                           # %%
                           cmap_3d, ticks_num,
                           is_title_on, is_axes_on, is_mm,
                           fontsize, font,
                           # %%
                           is_colorbar_on, is_energy,
                           # %%
                           zj, z_stored, **kwargs, ):
    # args 是 z 或 ()，但 z 可从 z_stored 中 提取，所以这里 省略了 *args，外面不用传 z 进来（得保证 z 是最后一个）
    # kwargs 是 is_no_data_save， is_save_txt， is_colorbar_log

    U_amp_plot_address, U_amp_title = U_amp_plot_address_and_title(U_name, folder_address, img_name_extension,
                                                                   z=z_stored[-1], )

    plot_3d_XYz(zj, sample, size_PerPixel,
                U, z_stored,
                U_amp_plot_address, U_amp_title,
                is_save, dpi, size_fig,
                cmap_3d, elev, azim, alpha,
                ticks_num, is_title_on, is_axes_on, is_mm,
                fontsize, font,
                0, is_colorbar_on, is_energy, )

    if kwargs.get("is_no_data_save", 0) == 0:
        suffix = "_amp"
        U_address, ugHGU = U_save(U, U_name + suffix, folder_address,
                                  is_save, is_save_txt,
                                  z=z_stored[-1], suffix=suffix, **kwargs, )

        suffix = '_zj'
        U_address, ugHGU = U_save(zj, U_name + suffix, folder_address,
                                  is_save, is_save_txt,
                                  z=z_stored[-1], suffix=suffix, **kwargs, )

        suffix = '_z_stored'
        U_address, ugHGU = U_save(z_stored, U_name + suffix, folder_address,
                                  is_save, is_save_txt,
                                  z=z_stored[-1], suffix=suffix, **kwargs, )

    return U_amp_plot_address


# %%

def U_phase_plot_save_3d_XYz(folder_address,
                             U, U_name,
                             img_name_extension,
                             is_save_txt,
                             # %%
                             sample, size_PerPixel,
                             is_save, dpi, size_fig,
                             elev, azim, alpha,
                             # %%
                             cmap_3d, ticks_num,
                             is_title_on, is_axes_on, is_mm,
                             fontsize, font,
                             # %%
                             is_colorbar_on,
                             # %%
                             zj, z_stored, **kwargs, ):
    # args 是 z 或 ()，但 z 可从 z_stored 中 提取，所以这里 省略了 *args，外面不用传 z 进来

    U_phase_plot_address, U_phase_title = U_phase_plot_address_and_title(U_name, folder_address, img_name_extension,
                                                                         z=z_stored[-1], )

    plot_3d_XYz(zj, sample, size_PerPixel,
                U, z_stored,
                U_phase_plot_address, U_phase_title,
                is_save, dpi, size_fig,
                cmap_3d, elev, azim, alpha,
                ticks_num, is_title_on, is_axes_on, is_mm,
                fontsize, font,
                0, is_colorbar_on, 0, )  # 相位 不能有 is_energy = 1

    if kwargs.get("is_no_data_save", 0) == 0:
        suffix = "_phase"
        U_address, ugHGU = U_save(U, U_name + suffix, folder_address,
                                  is_save, is_save_txt,
                                  z=z_stored[-1], suffix=suffix, **kwargs, )

        suffix = '_zj'
        U_address, ugHGU = U_save(zj, U_name + suffix, folder_address,
                                  is_save, is_save_txt,
                                  z=z_stored[-1], suffix=suffix, **kwargs, )

        suffix = '_z_stored'
        U_address, ugHGU = U_save(z_stored, U_name + suffix, folder_address,
                                  is_save, is_save_txt,
                                  z=z_stored[-1], suffix=suffix, **kwargs, )

    return U_phase_plot_address


# %%

def U_amp_plot_save_3d_XYZ(folder_address,
                           U_name,
                           U_YZ, U_XZ,
                           U_1, U_2,
                           U_f, U_e,
                           th_X, th_Y,
                           th_1, th_2,
                           th_f, th_e,
                           img_name_extension,
                           is_save_txt,
                           # %%
                           sample, size_PerPixel,
                           is_save, dpi, size_fig,
                           elev, azim, alpha,
                           # %%
                           cmap_3d, ticks_num,
                           is_title_on, is_axes_on, is_mm,
                           fontsize, font,
                           # %%
                           is_colorbar_on, is_energy, is_show_structure_face,
                           # %%
                           zj, **kwargs, ):  # args 是 z 或 ()
    # kwargs 是 is_no_data_save， is_save_txt

    U_amp_plot_address, U_amp_title = U_amp_plot_address_and_title(U_name, folder_address, img_name_extension,
                                                                   **kwargs, )

    plot_3d_XYZ(zj, sample, size_PerPixel,
                U_YZ, U_XZ,
                U_1, U_2,
                U_f, U_e, is_show_structure_face,
                U_amp_plot_address, U_amp_title,
                th_X, th_Y,
                th_1, th_2,
                th_f, th_e,
                is_save, dpi, size_fig,
                cmap_3d, elev, azim, alpha,
                ticks_num, is_title_on, is_axes_on, is_mm,
                fontsize, font,
                0, is_colorbar_on, is_energy,
                **kwargs, )

    if kwargs.get("is_no_data_save", 0) == 0:
        suffix = "_amp"
        U_address, ugHGU = U_save(np.array([U_YZ, U_XZ, U_1, U_2, U_f, U_e, 0], dtype=object), U_name + suffix,
                                  folder_address,
                                  is_save, is_save_txt,
                                  suffix=suffix, **kwargs, )

        suffix = '_th_XY12fe'
        U_address, ugHGU = U_save(np.array([th_X, th_Y, th_1, th_2, th_f, th_e]), U_name + suffix, folder_address,
                                  is_save, is_save_txt,
                                  suffix=suffix, **kwargs, )

        suffix = '_zj'
        U_address, ugHGU = U_save(zj, U_name + suffix, folder_address,
                                  is_save, is_save_txt,
                                  suffix=suffix, **kwargs, )  # 似乎不必储存 z； z 从外面传进来，只是为了名字

        suffix = '_vmax_vmin'
        U_address, ugHGU = U_save(np.array([kwargs.get("vmax", 1), kwargs.get("vmin", 0)]), U_name + suffix,
                                  folder_address,
                                  is_save, is_save_txt,
                                  suffix=suffix, **kwargs, )

    return U_amp_plot_address


# %%

def U_phase_plot_save_3d_XYZ(folder_address,
                             U_name,
                             U_YZ, U_XZ,
                             U_1, U_2,
                             U_f, U_e,
                             th_X, th_Y,
                             th_1, th_2,
                             th_f, th_e,
                             img_name_extension,
                             is_save_txt,
                             # %%
                             sample, size_PerPixel,
                             is_save, dpi, size_fig,
                             elev, azim, alpha,
                             # %%
                             cmap_3d, ticks_num,
                             is_title_on, is_axes_on, is_mm,
                             fontsize, font,
                             # %%
                             is_colorbar_on, is_show_structure_face,
                             # %%
                             zj, **kwargs, ):  # args 是 z 或 ()

    U_phase_plot_address, U_phase_title = U_phase_plot_address_and_title(U_name, folder_address, img_name_extension,
                                                                         **kwargs, )

    plot_3d_XYZ(zj, sample, size_PerPixel,
                U_YZ, U_XZ,
                U_1, U_2,
                U_f, U_e, is_show_structure_face,
                U_phase_plot_address, U_phase_title,
                th_X, th_Y,
                th_1, th_2,
                th_f, th_e,
                is_save, dpi, size_fig,
                cmap_3d, elev, azim, alpha,
                ticks_num, is_title_on, is_axes_on, is_mm,
                fontsize, font,
                0, is_colorbar_on, 0,
                **kwargs, )  # 相位 不能有 is_energy = 1

    if kwargs.get("is_no_data_save", 0) == 0:
        suffix = "_phase"
        U_address, ugHGU = U_save(np.array([U_YZ, U_XZ, U_1, U_2, U_f, U_e, 0], dtype=object), U_name + suffix,
                                  folder_address,
                                  is_save, is_save_txt,
                                  suffix=suffix, **kwargs, )

        suffix = '_th_XY12fe'
        U_address, ugHGU = U_save(np.array([th_X, th_Y, th_1, th_2, th_f, th_e]), U_name + suffix, folder_address,
                                  is_save, is_save_txt,
                                  suffix=suffix, **kwargs, )

        suffix = '_zj'
        U_address, ugHGU = U_save(zj, U_name + suffix, folder_address,
                                  is_save, is_save_txt,
                                  suffix=suffix, **kwargs, )  # 似乎不必储存 z； z 从外面传进来，只是为了名字

        suffix = '_vmax_vmin'
        U_address, ugHGU = U_save(np.array([kwargs.get("vmax", 1), kwargs.get("vmin", 0)]), U_name + suffix,
                                  folder_address,
                                  is_save, is_save_txt,
                                  suffix=suffix, **kwargs, )

    return U_phase_plot_address


# %%

def U_EVV_plot(G_stored, G_name,
               U_stored, U_name,
               img_name_extension,
               is_save_txt,
               # %%
               sample, size_PerPixel,
               is_save, dpi, size_fig,
               elev, azim, alpha,
               # %%
               cmap_2d, cmap_3d,
               ticks_num, is_contourf,
               is_title_on, is_axes_on, is_mm,
               fontsize, font,
               # %%
               is_colorbar_on, is_energy,
               # %%
               plot_group, is_animated,
               loop, duration, fps,
               # %%
               is_plot_3d_XYz,
               # %%
               zj, z_stored, z,
               # %%
               **kwargs, ):  # kwargs 是 is_no_data_save， is_save_txt， is_colorbar_log
    p_dir = 'GU_XY(z)'
    # -------------------------
    if ("G" in plot_group and "a" in plot_group):
        folder_address = U_dir(G_name + "_XY_amp", is_save,
                               z=z, p_dir=p_dir, **kwargs)
        gif_address = U_amps_z_plot_save(folder_address,
                                         np.abs(G_stored), G_name,
                                         img_name_extension,
                                         is_save_txt,
                                         # %%
                                         sample, size_PerPixel,
                                         is_save, dpi, size_fig,
                                         # %%
                                         cmap_2d, ticks_num, is_contourf,
                                         is_title_on, is_axes_on, is_mm,
                                         fontsize, font,
                                         # %%
                                         is_colorbar_on, is_energy,  # 默认无法 外界设置 vmax 和 vmin，因为 同时画 振幅 和 相位 得 传入 2*2 个 v
                                         # %%                          何况 一般默认 is_self_colorbar = 1...
                                         z_stored, is_animated,
                                         duration, fps, loop,
                                         z, **kwargs, )  # 传 z 是为了 储存时，给 G_stored 命名
    if ("G" in plot_group and "p" in plot_group):
        folder_address = U_dir(G_name + "_XY_phase", is_save,
                               z=z, p_dir=p_dir, **kwargs)
        gif_address = U_phases_z_plot_save(folder_address,
                                           np.angle(G_stored), G_name,
                                           img_name_extension,
                                           is_save_txt,
                                           # %%
                                           sample, size_PerPixel,
                                           is_save, dpi, size_fig,
                                           # %%
                                           cmap_2d, ticks_num, is_contourf,
                                           is_title_on, is_axes_on, is_mm,
                                           fontsize, font,
                                           # %%
                                           is_colorbar_on,  # 默认无法 外界设置 vmax 和 vmin，默认 自动统一 colorbar
                                           # %%
                                           z_stored, is_animated,
                                           duration, fps, loop,
                                           z, **kwargs, )

    # -------------------------
    if ("U" in plot_group and "a" in plot_group):
        folder_address = U_dir(U_name + "_XY_amp", is_save,
                               z=z, p_dir=p_dir, **kwargs)
        gif_address = U_amps_z_plot_save(folder_address,
                                         np.abs(U_stored), U_name,
                                         img_name_extension,
                                         is_save_txt,
                                         # %%
                                         sample, size_PerPixel,
                                         is_save, dpi, size_fig,
                                         # %%
                                         cmap_2d, ticks_num, is_contourf,
                                         is_title_on, is_axes_on, is_mm,
                                         fontsize, font,
                                         # %%
                                         is_colorbar_on, is_energy,  # 默认无法 外界设置 vmax 和 vmin，因为 同时画 振幅 和 相位 得 传入 2*2 个 v
                                         # %%                          何况 一般默认 is_self_colorbar = 1...
                                         z_stored, is_animated,
                                         duration, fps, loop,
                                         z, **kwargs, )

    if ("U" in plot_group and "p" in plot_group):
        folder_address = U_dir(U_name + "_XY_phase", is_save,
                               z=z, p_dir=p_dir, **kwargs)
        gif_address = U_phases_z_plot_save(folder_address,
                                           np.angle(U_stored), U_name,
                                           img_name_extension,
                                           is_save_txt,
                                           # %%
                                           sample, size_PerPixel,
                                           is_save, dpi, size_fig,
                                           # %%
                                           cmap_2d, ticks_num, is_contourf,
                                           is_title_on, is_axes_on, is_mm,
                                           fontsize, font,
                                           # %%
                                           is_colorbar_on,  # 默认无法 外界设置 vmax 和 vmin，默认 自动统一 colorbar
                                           # %%
                                           z_stored, is_animated,
                                           duration, fps, loop,
                                           z, **kwargs, )

    # %%
    p_dir = 'GU_XYz'
    # %%
    # 这 XY_stored_num 层 也可以 画成 3D，就是太丑了，所以只 整个 U0_amp 示意一下即可

    if ("U" in plot_group and "a" in plot_group) and is_plot_3d_XYz == 1:
        suffix = "_XYz"
        folder_address = U_dir(G_name + suffix + "_amp", is_save,
                               z=z, p_dir=p_dir, **kwargs)
        U_amp_plot_address = U_amp_plot_save_3d_XYz(folder_address,
                                                    np.abs(U_stored), U_name + suffix,
                                                    img_name_extension,
                                                    is_save_txt,
                                                    # %%
                                                    sample, size_PerPixel,
                                                    is_save, dpi, size_fig,
                                                    elev, azim, alpha,
                                                    # %%
                                                    cmap_3d, ticks_num,
                                                    is_title_on, is_axes_on, is_mm,
                                                    fontsize, font,
                                                    # %%
                                                    is_colorbar_on, is_energy,
                                                    # %%
                                                    zj, z_stored, **kwargs, )


# %%

def U_SSI_plot(G_stored, G_name,
               U_stored, U_name,
               G_YZ, G_XZ,
               U_YZ, U_XZ,
               G_1, G_2,
               G_f, G_e,
               U_1, U_2,
               U_f, U_e,
               th_X, th_Y,
               th_1, th_2,
               th_f, th_e,
               img_name_extension,
               is_no_data_save, is_save_txt,
               # %%
               sample, size_PerPixel,
               is_save, dpi, size_fig,
               elev, azim, alpha,
               # %%
               cmap_2d, cmap_3d,
               ticks_num, is_contourf,
               is_title_on, is_axes_on, is_mm,
               fontsize, font,
               # %%
               is_colorbar_on, is_colorbar_log,
               is_energy, is_show_structure_face,
               # %%
               plot_group, is_animated,
               loop, duration, fps,
               # %%
               is_plot_EVV, is_plot_3d_XYz, is_plot_selective,
               is_plot_YZ_XZ, is_plot_3d_XYZ,
               # %%
               X, Y,
               z_1, z_2,
               z_f, z_e,
               zj, z_stored, z, ):
    # %%

    if is_plot_EVV == 1:
        U_EVV_plot(G_stored, G_name,
                   U_stored, U_name,
                   img_name_extension,
                   is_save_txt,
                   # %%
                   sample, size_PerPixel,
                   is_save, dpi, size_fig,
                   elev, azim, alpha,
                   # %%
                   cmap_2d, cmap_3d,
                   ticks_num, is_contourf,
                   is_title_on, is_axes_on, is_mm,
                   fontsize, font,
                   # %%
                   is_colorbar_on, is_energy,
                   # %%
                   plot_group, is_animated,
                   loop, duration, fps,
                   # %%
                   is_plot_3d_XYz,
                   # %%
                   zj, z_stored, z,
                   # %%
                   is_no_data_save=is_no_data_save,
                   is_colorbar_log=is_colorbar_log, )

    # %%
    p_dir = "GU_XYs"
    # %%

    if is_plot_selective == 1:

        if "G" in plot_group:
            folder_address = U_dir(G_name + "_XYs", is_save,
                                   z=z, p_dir=p_dir, is_no_data_save=is_no_data_save, )

            # ------------------------- 储存 G1_section_1_shift_amp、G1_section_1_shift_amp、G1_structure_frontface_shift_amp、G1_structure_endface_shift_amp
            # ------------------------- 储存 G1_section_1_shift_phase、G1_section_1_shift_phase、G1_structure_frontface_shift_phase、G1_structure_endface_shift_phase

            G_amps_max, G_amps_min, G_phases_max, G_phases_min = \
                U_selects_plot_save(folder_address,
                                    G_1, G_name + "_sec1",
                                    G_2, G_name + "_sec2",
                                    G_f, G_name + "_front",
                                    G_e, G_name + "_end",
                                    img_name_extension,
                                    is_save_txt,
                                    # %%
                                    sample, size_PerPixel,
                                    is_save, dpi, size_fig,
                                    # %%
                                    cmap_2d, ticks_num, is_contourf,
                                    is_title_on, is_axes_on, is_mm,
                                    fontsize, font,
                                    # %%
                                    is_colorbar_on, is_energy, is_show_structure_face,
                                    # %%
                                    z_1, z_2, z_f, z_e,
                                    # %%
                                    is_no_data_save=is_no_data_save,
                                    is_colorbar_log=is_colorbar_log, )

        # %%

        if "U" in plot_group:
            folder_address = U_dir(U_name + "_XYs", is_save,
                                   z=z, p_dir=p_dir, is_no_data_save=is_no_data_save, )

            # ------------------------- 储存 U0_section_1_amp、U0_section_1_amp、U0_structure_frontface_amp、U0_structure_endface_amp
            # ------------------------- 储存 U0_section_1_phase、U0_section_1_phase、U0_structure_frontface_phase、U0_structure_endface_phase

            U_amps_max, U_amps_min, U_phases_max, U_phases_min = \
                U_selects_plot_save(folder_address,
                                    U_1, U_name + "_sec1",
                                    U_2, U_name + "_sec2",
                                    U_f, U_name + "_front",
                                    U_e, U_name + "_end",
                                    img_name_extension,
                                    is_save_txt,
                                    # %%
                                    sample, size_PerPixel,
                                    is_save, dpi, size_fig,
                                    # %%
                                    cmap_2d, ticks_num, is_contourf,
                                    is_title_on, is_axes_on, is_mm,
                                    fontsize, font,
                                    # %%
                                    is_colorbar_on, is_energy, is_show_structure_face,
                                    # %%
                                    z_1, z_2, z_f, z_e,
                                    # %%
                                    is_no_data_save=is_no_data_save,
                                    is_colorbar_log=is_colorbar_log, )

    # %%

    if is_plot_YZ_XZ == 1:

        # %%
        p_dir = "GU_X(Y)Z"
        # %%
        # ========================= G1_shift_YZ_stored_amp、G1_shift_XZ_stored_amp
        # ------------------------- G1_shift_YZ_stored_phase、G1_shift_XZ_stored_phase

        if "G" in plot_group:
            folder_address = U_dir(G_name + "_X(Y)Z", is_save,
                                   z=z, p_dir=p_dir, is_no_data_save=is_no_data_save, )
            G_YZ_XZ_amp_max, G_YZ_XZ_amp_min, G_YZ_XZ_phase_max, G_YZ_XZ_phase_min = \
                U_slices_plot_save(folder_address,
                                   G_YZ, G_name + "_YZ",
                                   G_XZ, G_name + "_XZ",
                                   img_name_extension,
                                   is_save_txt,
                                   # %%
                                   zj, sample, size_PerPixel,
                                   is_save, dpi, size_fig,
                                   # %%
                                   cmap_2d, ticks_num, is_contourf,
                                   is_title_on, is_axes_on, is_mm,
                                   fontsize, font,
                                   # %%
                                   is_colorbar_on, is_energy,
                                   # %%
                                   X, Y,
                                   # %%
                                   is_no_data_save=is_no_data_save,
                                   is_colorbar_log=is_colorbar_log, )

        # %%

        # ========================= U0_YZ_stored_amp、U0_XZ_stored_amp
        # ------------------------- U0_YZ_stored_phase、U0_XZ_stored_phase

        if "U" in plot_group:
            folder_address = U_dir(U_name + "_X(Y)Z", is_save,
                                   z=z, p_dir=p_dir, is_no_data_save=is_no_data_save, )
            U_YZ_XZ_amp_max, U_YZ_XZ_amp_min, U_YZ_XZ_phase_max, U_YZ_XZ_phase_min = \
                U_slices_plot_save(folder_address,
                                   U_YZ, U_name + "_YZ",
                                   U_XZ, U_name + "_XZ",
                                   img_name_extension,
                                   is_save_txt,
                                   # %%
                                   zj, sample, size_PerPixel,
                                   is_save, dpi, size_fig,
                                   # %%
                                   cmap_2d, ticks_num, is_contourf,
                                   is_title_on, is_axes_on, is_mm,
                                   fontsize, font,
                                   # %%
                                   is_colorbar_on, is_energy,
                                   # %%
                                   X, Y,
                                   # %%
                                   is_no_data_save=is_no_data_save,
                                   is_colorbar_log=is_colorbar_log, )

        if is_plot_3d_XYZ == 1:
            # %%
            p_dir = "GU_XYZ"
            # %%
            # 绘制 G1_amp 的 侧面 3D 分布图，以及 初始 和 末尾的 G1_amp（现在 可以 任选位置 了）

            if ("G" in plot_group and "a" in plot_group):
                if is_colorbar_log == -1:
                    v_kwargs = {}
                else:
                    v_kwargs = {
                        "vmax": np.max([G_YZ_XZ_amp_max, G_amps_max]),
                        "vmin": np.min([G_YZ_XZ_amp_min, G_amps_min]),
                    }

                suffix = "_XYZ"
                folder_address = U_dir(G_name + suffix + "_amp", is_save,
                                       z=z, p_dir=p_dir, is_no_data_save=is_no_data_save, )
                U_amp_plot_address = U_amp_plot_save_3d_XYZ(folder_address,
                                                            G_name + suffix,
                                                            np.abs(G_YZ), np.abs(G_XZ),
                                                            np.abs(G_1), np.abs(G_2),
                                                            np.abs(G_f), np.abs(G_e),
                                                            th_X, th_Y,
                                                            th_1, th_2,
                                                            th_f, th_e,
                                                            img_name_extension,
                                                            is_save_txt,
                                                            # %%
                                                            sample, size_PerPixel,
                                                            is_save, dpi, size_fig,
                                                            elev, azim, alpha,
                                                            # %%
                                                            cmap_3d, ticks_num,
                                                            is_title_on, is_axes_on, is_mm,
                                                            fontsize, font,
                                                            # %%
                                                            is_colorbar_on, is_energy, is_show_structure_face,
                                                            # %%
                                                            zj, z=z,
                                                            is_no_data_save=is_no_data_save,
                                                            is_colorbar_log=is_colorbar_log,
                                                            # %%
                                                            **v_kwargs, )

            # %%
            # 绘制 G1_phase 的 侧面 3D 分布图，以及 初始 和 末尾的 G1_phase

            if ("G" in plot_group and "p" in plot_group):
                if is_colorbar_log == -1:
                    v_kwargs = {}
                else:
                    v_kwargs = {
                        "vmax": np.max([G_YZ_XZ_phase_max, G_phases_max]),
                        "vmin": np.min([G_YZ_XZ_phase_min, G_phases_min]),
                    }

                suffix = "_XYZ"
                folder_address = U_dir(G_name + suffix + "_phase", is_save,
                                       z=z, p_dir=p_dir, is_no_data_save=is_no_data_save, )
                U_phase_plot_address = U_phase_plot_save_3d_XYZ(folder_address,
                                                                G_name + suffix,
                                                                np.angle(G_YZ), np.angle(G_XZ),
                                                                np.angle(G_1), np.angle(G_2),
                                                                np.angle(G_f), np.angle(G_e),
                                                                th_X, th_Y,
                                                                th_1, th_2,
                                                                th_f, th_e,
                                                                img_name_extension,
                                                                is_save_txt,
                                                                # %%
                                                                sample, size_PerPixel,
                                                                is_save, dpi, size_fig,
                                                                elev, azim, alpha,
                                                                # %%
                                                                cmap_3d, ticks_num,
                                                                is_title_on, is_axes_on, is_mm,
                                                                fontsize, font,
                                                                # %%
                                                                is_colorbar_on, is_show_structure_face,
                                                                # %%
                                                                zj, z=z,
                                                                is_no_data_save=is_no_data_save,
                                                                is_colorbar_log=is_colorbar_log,
                                                                # %%
                                                                **v_kwargs, )

            # %%
            # 绘制 U0_amp 的 侧面 3D 分布图，以及 初始 和 末尾的 U0_amp

            if ("U" in plot_group and "a" in plot_group):
                if is_colorbar_log == -1:
                    v_kwargs = {}
                else:
                    v_kwargs = {
                        "vmax": np.max([U_YZ_XZ_amp_max, U_amps_max]),
                        "vmin": np.min([U_YZ_XZ_amp_min, U_amps_min]),
                    }

                suffix = "_XYZ"
                folder_address = U_dir(U_name + suffix + "_amp", is_save,
                                       z=z, p_dir=p_dir, is_no_data_save=is_no_data_save, )
                U_amp_plot_address = U_amp_plot_save_3d_XYZ(folder_address,
                                                            U_name + suffix,
                                                            np.abs(U_YZ), np.abs(U_XZ),
                                                            np.abs(U_1), np.abs(U_2),
                                                            np.abs(U_f), np.abs(U_e),
                                                            th_X, th_Y,
                                                            th_1, th_2,
                                                            th_f, th_e,
                                                            img_name_extension,
                                                            is_save_txt,
                                                            # %%
                                                            sample, size_PerPixel,
                                                            is_save, dpi, size_fig,
                                                            elev, azim, alpha,
                                                            # %%
                                                            cmap_3d, ticks_num,
                                                            is_title_on, is_axes_on, is_mm,
                                                            fontsize, font,
                                                            # %%
                                                            is_colorbar_on, is_energy, is_show_structure_face,
                                                            # %%
                                                            zj, z=z,
                                                            is_no_data_save=is_no_data_save,
                                                            is_colorbar_log=is_colorbar_log,
                                                            # %%
                                                            **v_kwargs, )

            # %%
            # 绘制 U0_phase 的 侧面 3D 分布图，以及 初始 和 末尾的 U0_phase

            if ("U" in plot_group and "p" in plot_group):
                if is_colorbar_log == -1:
                    v_kwargs = {}
                else:
                    v_kwargs = {
                        "vmax": np.max([U_YZ_XZ_phase_max, U_phases_max]),
                        "vmin": np.min([U_YZ_XZ_phase_min, U_phases_min]),
                    }

                suffix = "_XYZ"
                folder_address = U_dir(U_name + suffix + "_phase", is_save,
                                       z=z, p_dir=p_dir, is_no_data_save=is_no_data_save, )
                U_phase_plot_address = U_phase_plot_save_3d_XYZ(folder_address,
                                                                U_name + suffix,
                                                                np.angle(U_YZ), np.angle(U_XZ),
                                                                np.angle(U_1), np.angle(U_2),
                                                                np.angle(U_f), np.angle(U_e),
                                                                th_X, th_Y,
                                                                th_1, th_2,
                                                                th_f, th_e,
                                                                img_name_extension,
                                                                is_save_txt,
                                                                # %%
                                                                sample, size_PerPixel,
                                                                is_save, dpi, size_fig,
                                                                elev, azim, alpha,
                                                                # %%
                                                                cmap_3d, ticks_num,
                                                                is_title_on, is_axes_on, is_mm,
                                                                fontsize, font,
                                                                # %%
                                                                is_colorbar_on, is_show_structure_face,
                                                                # %%
                                                                zj, z=z,
                                                                is_no_data_save=is_no_data_save,
                                                                is_colorbar_log=is_colorbar_log,
                                                                # %%
                                                                **v_kwargs, )


# %%

def attr_set(item_attr_name, item_attr_value):
    index = Get("item_attr_name_loc_dict_save")[item_attr_name]
    Get("item_attr_value_list_save")[index] = item_attr_value


def attr_auto_set(item_attr_name):
    index = Get("item_attr_name_loc_dict_save")[item_attr_name]
    Get("item_attr_value_list_save")[index] = globals()[item_attr_name]


def attr_Auto_Set(locals):
    # print(locals)
    for item_attr_name in Get("item_attr_name_loc_dict_save"):
        # print(locals[item_attr_name])
        index = Get("item_attr_name_loc_dict_save")[item_attr_name]
        Get("item_attr_value_list_save")[index] = str(locals[item_attr_name])  # 储存的 全转为 字符串了，所以之前没转 也没问题
        # print(locals[item_attr_name])
        # Get("item_attr_value_list_save")[index] = globals()[item_attr_name]
        # 这个 写这才有用：globals() 只能获取 当前 py 文件下的，调用这里的这个的话，只能得到 这个 py 文件中的 globals
        # 额，也没用，globals() 无法获取到没有用 global 声明的局部变量


def attr_get_from_list(item_attr_name):
    index = Get("item_attr_name_loc_dict_save")[item_attr_name]
    return Get("item_attr_value_list_save")[index]


def attr_line_get(line, item_attr_name):  # from line
    index = Get("item_attr_name_loc_dict_save")[item_attr_name]
    if len(line.split(Get("attr_separator"))) >= index + 1:
        return line.split(Get("attr_separator"))[index]
    else:
        return None  # 等价于 不写 return 即没有 返回值


def attrs_line_get(attr_line, *item_attr_names):
    attr_values = []
    for attr_name in item_attr_names:
        attr_values.append(attr_line_get(attr_line, attr_name))
    return attr_values  # attr_values 的顺序 等于 attr_names 的顺序
    # 也就是 attr_names.index("attr_name") = attr_values.index("attr_value")


# %%

def gan_Data_Seq(txt, folder_address):
    txt.seek(0)  # 光标移到 txt 开头
    whole_text = txt.read()  # 这句话后，光标 已经 移到末尾
    txt.seek(0)  # 光标再移到 txt 开头（这个是真的坑）
    lines = txt.readlines()
    # txt.seek(2)  # 光标移到 txt 末尾（不必了，其实 已经移到 末尾了）

    folder_address_relative = folder_address.replace(Get("root_dir") + "\\", "")
    # 相对路径中，将只剩下 kwargs["p_dir"] + "\\" + folder_name 或 folder_name
    dirs = folder_address_relative.split("\\")
    dirs = [(DIR.replace(DIR.split(' ')[0] + ' ', "") if len(DIR.split(' ')) > 1 and
                                                         set(find_NOT_nums(DIR.split(' ')[0])) == {"."} else DIR)
            for DIR in dirs]  # 有空格 则 取第一部分，若其中 非数字只有 '.' 的话，取 第二部分
    # print(dirs)
    level = len(dirs)  # 桌面上的 folder 内的东西 就是 1，内部的 就是 2...诸如此类
    # print(level)
    level_seq = [Get("level_min")] * level  # [0,0,0,...]
    level_seq_max = [Get("level_min")] * level  # [0,0,0,...] 这个 只有 l=0 才有用
    dir_repeat_times = [0] * level
    # dir_repeat_line_i = [[]] * level  # [[],[],[],...] # dirs[l] 重复时 所对应的 line 行序数 i
    # 这个 只有 l>0 才有用，其实不用记录 line 的 行序数 i，只需 记录 符合条件的 line 数，所以 [] * level 更省内存
    data_seq = Get("level_min")
    dir_seq_max = Get("level_min")
    for i in range(len(lines)):
        line = lines[i]
        line = line[:-1]
        item_Level_Seq = attr_line_get(line, "Level_Seq")
        item_level_seq = item_Level_Seq.split('.')
        folder_address_line, root_dir_line = attrs_line_get(line, "folder_address", "root_dir")
        folder_address_line_relative = folder_address_line.replace(root_dir_line + "\\", "")
        # print(folder_address_line_relative)
        dirs_line = folder_address_line_relative.split("\\")
        dirs_line = [(DIR_line.replace(DIR_line.split(' ')[0] + ' ', "") if len(DIR_line.split(' ')) > 1 and
                                                                            set(find_NOT_nums(
                                                                                DIR_line.split(' ')[0])) == {
                                                                                '.'} else DIR_line)
                     for DIR_line in dirs_line]  # 把序号 扔了
        # print(dirs_line)
        ex_dir_is_in = 0
        for l in range(level):  # 遍历 被 "\\" 分隔出的 每个 dir，储存其 每次出现，所在的 行序数 i
            if l > 0:  # 如果 l>0 则必须 额外条件：前一个 dirs[l-1] 在 line_folder_address 中，才记录
                if ex_dir_is_in == 1:
                    if len(item_level_seq) >= l + 1:  # 如果长度 足够被取
                        if level_seq_max[l] < int(item_level_seq[l]): level_seq_max[l] = int(item_level_seq[l])
                    if dirs[l] == dirs_line[l]:
                        dir_repeat_times[l] += 1
                        # dir_repeat_line_i[l].append(i)
                        level_seq[l] = int(item_level_seq[l])  # 保持 该层的 level 不变
                        # print(dir_repeat_times,level_seq)
                        ex_dir_is_in = 1
                    else:
                        ex_dir_is_in = 0
                else:
                    ex_dir_is_in = 0
            else:
                if len(item_level_seq) >= l + 1:  # 如果长度 足够被取
                    if level_seq_max[l] < int(item_level_seq[l]): level_seq_max[l] = int(item_level_seq[l])
                if dirs[l] == dirs_line[l]:
                    # print(dir_repeat_times)
                    dir_repeat_times[l] += 1
                    # dir_repeat_line_i[l].append(i) # 傻逼 python 会把 dir_repeat_line_i 内的所有 [] 都 append
                    # print(dir_repeat_times)
                    level_seq[l] = int(item_level_seq[l])  # 保持 该层的 level 不变
                    ex_dir_is_in = 1
                else:
                    ex_dir_is_in = 0
            # print(dir_repeat_line_i)

        Data_Seq = attr_line_get(line, "Data_Seq")
        dir_seq_line = Data_Seq.split('.')[0]
        if dir_seq_max < int(dir_seq_line): dir_seq_max = int(dir_seq_line)
        if folder_address in folder_address_line:  # 从上往下，获得 记录中 第一次出现，所在行 的 dir_seq
            data_seq += 1  # 依据：不会有 2 个 数据，储存在同一个 python 生成的 mat 文件中，txt 倒是可能。。。
            dir_seq = dir_seq_line  # 保持 dir_seq 不变
        # elif data_seq > 0:  # 如果 line 里没有 folder_address，但 data_seq 又 > 0，
        #     # 说明 曾有过 folder_address 但结束了，所以后续 不会再有了，所以 直接退出。（）
        #     # 如果 line 里没有 folder_address，但 data_seq 又 = 0，说明还没到，继续 for 循环，不 break
        #     break # 若 特殊情况，间隔一段 不同后，后续 还有 folder_address 相同，则 for 循环 必须执行到 末尾

    if data_seq == Get("level_min"):  # 如果 folder_address 在以前的 记录中 没出现过
        if len(lines) > 0:  # 如果 folder_address 在以前的 记录中 没出现过，但已经有数据记录
            dir_seq = str(int(dir_seq_max) + 1)  # 把 dir_seq_max 加 1，作为 序数
        else:
            dir_seq = str(Get("level_min"))  # str(0) 也行
    Data_Seq = dir_seq + '.' + str(data_seq)  # 更新 Data_Seq

    # print(level_seq)
    # print(dir_repeat_line_i)
    Level_Seq = ''
    for l in range(level):
        if dir_repeat_times[l] == 0:  # 如果 dirs[l] 在以前 从没出现过 len(dir_repeat_line_i[l]) == 0
            if l == 0:  # （出现过的话，值已经定好了：保留原值）
                level_seq[l] = (level_seq_max[l] + 1) if len(lines) > 0 else Get("level_min")
            else:
                level_seq[l] = (level_seq_max[l] + 1) if dir_repeat_times[l - 1] > 0 else Get("level_min")
        Level_Seq += str(level_seq[l])  # 更新 Level_Seq
        Level_Seq += ('.' if l != level - 1 else '')
    # print(Level_Seq)
    data_th = len(lines) + Get("level_min")
    return data_th, Data_Seq, Level_Seq


def auto_gan_attr_line():
    attr_line = ''
    for index in range(len(Get("item_attr_value_list_save"))):
        attr_line += Get("item_attr_value_list_save")[index]
        attr_line += (Get("attr_separator") if index != len(Get("item_attr_value_list_save")) - 1 else "\n")
    return attr_line


def U_save(U, U_name, folder_address,
           is_save, is_save_txt, **kwargs, ):
    U_address, ugHGU = gan_Uz_save_address(U_name, folder_address, is_save_txt,
                                           **kwargs)
    if is_save == 1:
        # print(ugHGU, U)
        ugHGU = ugHGU if ugHGU != 'χ' else 'X'  # "χ".encode("utf-8").decode("latin1") 这玩意 不能作为 字典名...
        np.savetxt(U_address, U) if is_save_txt else savemat(U_address, {ugHGU: U})

        main_py_name = Get("main_py_name")
        is_data_saved = 1
        kwargs_seq = Get("kwargs_seq")
        root_dir_boot_times = Get("root_dir_boot_times")
        saver_name = inspect.stack()[1][3]
        z_str = str(kwargs['z']) if 'z' in kwargs else 'z'
        U_name_no_suffix = U_name.replace(kwargs['suffix'], '') if 'suffix' in kwargs else 'U_name_no_suffix'
        root_dir = Get("root_dir")

        txt_address = Get("root_dir") + "\\" + "all_data_info.txt"
        with open(txt_address, "a+") as txt:  # 追加模式；如果没有 该文件，则 创建之；+ 表示 除了 写 之外，还可 读
            data_th, Data_Seq, Level_Seq = gan_Data_Seq(txt, folder_address)
            attr_Auto_Set(locals())  # 定义完 所有 attr 后，就写入 记录之
            attr_line = auto_gan_attr_line()
            txt.write(attr_line)

        txt_address = folder_address + "\\" + "data_info.txt"
        with open(txt_address, "a+") as txt:  # 追加模式；如果没有 该文件，则 创建之；+ 表示 除了 写 之外，还可 读
            txt.write(attr_line)

    return U_address, ugHGU


# %%

def get_Data_info(Data_Seq):
    txt_address = Get("root_dir") + "\\" + "all_data_info.txt"
    with open(txt_address, "r") as txt:
        lines = txt.readlines()  # 注意是 readlines 不是 readline，否则 只读了 一行，而不是 所有行 构成的 列表
        # lines = lines[:-1] # 把 最后一行 的 换行 去掉（不用去了，每个 \n 包含在上一行了）
    Data_Seq = str(Data_Seq) + (("." + str(Get("level_min"))) if '.' not in str(Data_Seq) else '')  # 不加括号 有问题，也是醉了
    attr_list = []
    for line in lines:
        line = line[:-1]
        # print(Data_Seq, attr_line_get(line, "Data_Seq"))
        if Data_Seq == attr_line_get(line, "Data_Seq"):
            attr_list = line.split(Get("attr_separator"))
            break
    # return attr_list
    return line  # python 中的 for 循环 的 内部变量 可以 外部调用：break 后还能用


def get_Data_attrs(Data_Seq, *attr_names):
    attr_line = get_Data_info(Data_Seq)
    return attrs_line_get(attr_line, *attr_names)
    # attr_values = []
    # for attr_name in attr_names:
    #     attr_values.append(attr_line_get(attr_line, attr_name))
    # return attr_values  # attr_values 的顺序 等于 attr_names 的顺序
    # # 也就是 attr_names.index("attr_name") = attr_values.index("attr_value")


def get_Data_new_root_dir(Data_Seq):
    root_dir, folder_address, U_address = get_Data_attrs(Data_Seq, "root_dir", "folder_address", "U_address")
    folder_new_address = folder_address.replace(root_dir, Get("root_dir"))  # 用新的 root_dir 去覆盖 旧的 root_dir
    U_new_address = U_address.replace(root_dir, Get("root_dir"))  # 用新的 root_dir 去覆盖 旧的 root_dir
    return Get("root_dir"), folder_new_address, U_new_address


def get_Data_new_attrs(Data_Seq, *attr_names):
    attr_values = get_Data_attrs(Data_Seq, *attr_names)
    if "root_dir" in attr_names:
        attr_values[attr_names.index("root_dir")] = Get("root_dir")  # attr_values 的索引 等于 attr_names 的索引
    if "folder_address" in attr_names or "U_address" in attr_names:
        new_root_dir, folder_new_address, U_new_address = get_Data_new_root_dir(Data_Seq)
        if "folder_address" in attr_names:
            attr_values[attr_names.index("folder_address")] = folder_new_address
        if "U_address" in attr_names:
            attr_values[attr_names.index("U_address")] = U_new_address
    return attr_values


def get_items_new_attr(Data_Seq, is_save_txt, is_print, ):
    # %% 分析 all_data_info.txt

    new_root_dir, folder_new_address, U_new_address = get_Data_new_root_dir(Data_Seq)
    # U_new_address 没用，可用 *_ 代替其解包

    # %% 分析 data_info.txt

    txt_address = folder_new_address + "\\" + "data_info.txt"
    with open(txt_address, "r") as txt:
        lines = txt.readlines()

    Data_Seq_list, ugHGU_list, U_name_list, U_address_list, U_list, z_list, U_name_no_suffix_list = \
        [], [], [], [], [], [], []
    is_end = [0] * (len(lines) - 1) + [1]
    add_level = [-1] + [0] * (len(lines) - 1)
    for i in range(len(lines)):
        line = lines[i]
        line = line[:-1]  # 把 每一行的 换行 去掉

        Data_Seq_line, ugHGU, U_name, U_address, root_dir, z, U_name_no_suffix = \
            attrs_line_get(line, "Data_Seq", "ugHGU", "U_name", "U_address",
                           "root_dir", "z_str", "U_name_no_suffix")  # 防重名
        U_new_address = U_address.replace(root_dir, new_root_dir)  # 用新的 root_dir 去覆盖 旧的 root_dir
        U = np.loadtxt(U_new_address, dtype=np.float64()) if is_save_txt == 1 else loadmat(U_new_address)[ugHGU]
        # print(U.shape[0])
        if U.shape[0] == 1:  # savemat 会使 1维 数组 变成 2维，也就是 会在外面 多加个 [], 但 2维 数组 保持不变
            U = U if is_save_txt == 1 else U[0]
        # print(U)
        # print(U_name_no_suffix)

        is_print and print(tree_print(is_end[i], add_level=add_level[i]) + "U_name = {}".format(U_name))

        Data_Seq_list.append(Data_Seq_line)  # 防重名
        ugHGU_list.append(ugHGU)
        U_name_list.append(U_name)
        U_address_list.append(U_new_address)

        U_list.append(U)
        z_list.append(float(z))  # z 不能是 str
        U_name_no_suffix_list.append(U_name_no_suffix)

    Data_Seq = str(Data_Seq) + (("." + str(Get("level_min"))) if '.' not in str(Data_Seq) else '')  # 先转成 str
    index = Data_Seq_list.index(Data_Seq)  # 找到 相应 Data_Seq 的 索引，然后往下读

    return folder_new_address, index, U_list, U_name_list, U_name_no_suffix_list, z_list


# %%

def U_energy_plot(folder_address,
                  U, U_name,
                  img_name_extension,
                  # %%
                  zj, sample, size_PerPixel,
                  is_save, dpi, size_fig_x, size_fig_y,
                  color_1d, ticks_num, is_title_on, is_axes_on, is_mm,
                  fontsize, font,  # 默认无法 外界设置，只能 自动设置 y 轴 max 和 min 了（不是 但 类似 colorbar），还有 is_energy
                  # %%
                  **kwargs, ):
    # %%
    # 绘制 U_amp
    suffix = kwargs.get("suffix", "_energy(z)")
    kwargs.pop("suffix", None)  # 及时删除 "suffix" 键，以使之后 不重复
    # %%
    # 生成 要储存的 图片名 和 地址
    U_energy_full_name, U_energy_plot_address = gan_Uz_plot_address(folder_address, img_name_extension,
                                                                    U_name, suffix, **kwargs)
    # %%
    # 生成 图片中的 title
    U_energy_title = gan_Uz_title(U_name, suffix,
                                  **kwargs)  # 增加 后缀 "_evolution" （才怪，suffix 只 help 辅助 加 5.1 这种序号，原 U_name 里已有 _energy 了）
    # %%

    plot_1d(zj, sample, size_PerPixel,
            U, U_energy_plot_address, U_energy_title,
            is_save, dpi, size_fig_x, size_fig_y,
            color_1d, ticks_num, is_title_on, is_axes_on, is_mm, 1,
            fontsize, font, 0,
            # %%
            **kwargs, )

    return U_energy_plot_address


def U_energy_plot_save(U, U_name,
                       img_name_extension,
                       is_save_txt,
                       # %%
                       zj, sample, size_PerPixel,
                       is_save, dpi, size_fig_x, size_fig_y,
                       color_1d, ticks_num, is_title_on, is_axes_on, is_mm,
                       fontsize, font,  # 默认无法 外界设置，只能 自动设置 y 轴 max 和 min 了（不是 但 类似 colorbar），还有 is_energy
                       # %%
                       z, **kwargs, ):
    # %% G
    suffix = "_energy(z)"
    folder_address = U_dir(U_name + suffix, is_save,
                           z=z, **kwargs)
    U_energy_plot_address = U_energy_plot(folder_address,
                                          U, U_name + suffix,
                                          img_name_extension,
                                          # %%
                                          zj, sample, size_PerPixel,
                                          is_save, dpi, size_fig_x, size_fig_y,
                                          color_1d, ticks_num,
                                          is_title_on, is_axes_on, is_mm,
                                          fontsize, font,
                                          # %%
                                          z=z, )
    U_address, ugHGU = U_save(U, U_name + suffix, folder_address,
                              is_save, is_save_txt,
                              z=z, suffix=suffix, **kwargs, )
    suffix = "_" + "zj"
    U_address, ugHGU = U_save(zj, U_name + suffix, folder_address,
                              is_save, is_save_txt,
                              z=z, suffix=suffix, **kwargs, )


# %%

def U_error_energy_plot_save(U, l2, l3, U_name,
                             img_name_extension, is_save_txt,
                             # %%
                             zj, ax2_xticklabel, sample, size_PerPixel,
                             is_save, dpi, size_fig_x, size_fig_y,
                             # %%
                             color_1d, color_1d2,
                             ticks_num, is_title_on, is_axes_on, is_mm,
                             fontsize, font,  # 默认无法 外界设置，只能 自动设置 y 轴 max 和 min 了（不是 但 类似 colorbar），还有 is_energy
                             # %%
                             z, **kwargs, ):
    kwargs['p_dir'] = 'GU_error(dk)'
    # %%
    title_suffix = '_distribution_error'

    if is_save == 2:
        is_save = 1
    folder_address = U_dir(U_name + title_suffix, is_save,
                           z=z, **kwargs, )

    label1 = "SSI_energy"
    label2 = "NLA_energy"
    label3 = "distribution_error"
    U_energy_plot(folder_address,
                  U, U_name,
                  img_name_extension,
                  # %%
                  zj, sample, size_PerPixel,
                  is_save, dpi, size_fig_x, size_fig_y,
                  color_1d, ticks_num,
                  is_title_on, is_axes_on, is_mm,
                  fontsize, font,
                  # %%
                  z=z, suffix=title_suffix,
                  # %%
                  l2=l2, label2=label2,
                  l3=l3, color_1d2=color_1d2,
                  label=label1, ax1_xticklabel=zj,  # 强迫 ax1 的 x 轴标签 保持原样
                  label3=label3, ax2_xticklabel=ax2_xticklabel, **kwargs, )

    suffix = "_" + label1
    U_address, ugHGU = U_save(U, U_name + suffix, folder_address,
                              is_save, is_save_txt,
                              z=z, suffix=suffix, **kwargs, )

    suffix = "_" + label2
    U_address, ugHGU = U_save(l2, U_name + suffix, folder_address,
                              is_save, is_save_txt,
                              z=z, suffix=suffix, **kwargs, )

    suffix = "_" + label3
    U_address, ugHGU = U_save(l3, U_name + suffix, folder_address,
                              is_save, is_save_txt,
                              z=z, suffix=suffix, **kwargs, )

    suffix = "_" + "dkQ"
    U_address, ugHGU = U_save(zj, U_name + suffix, folder_address,
                              is_save, is_save_txt,
                              z=z, suffix=suffix, **kwargs, )

    suffix = "_" + "Tz"
    U_address, ugHGU = U_save(ax2_xticklabel, U_name + suffix, folder_address,
                              is_save, is_save_txt,
                              z=z, suffix=suffix, **kwargs, )


def U_twin_energy_error_plot_save(U, l2, U_name,
                                  img_name_extension, is_save_txt,
                                  # %%
                                  zj, zj2, sample, size_PerPixel,
                                  is_save, dpi, size_fig_x, size_fig_y,
                                  # %%
                                  color_1d, color_1d2,
                                  ticks_num, is_title_on, is_axes_on, is_mm,
                                  fontsize, font,  # 默认无法 外界设置，只能 自动设置 y 轴 max 和 min 了（不是 但 类似 colorbar），还有 is_energy
                                  # %%
                                  z, **kwargs, ):
    kwargs['p_dir'] = 'GU_energy_error(z)'
    # %%
    if kwargs.get("is_energy_normalized", False) == 1:
        U_plot = U / np.max(U)
        l2_plot = l2 / np.max(l2)
        title_suffix = '_energy_normalized - compare'
    elif kwargs.get("is_energy_normalized", False) == 2:
        U_plot = U
        l2_plot = l2 / l2[-1] * U[-1]
        title_suffix = '_energy_sync - compare'
    else:
        U_plot = U
        l2_plot = l2
        title_suffix = '_energy - compare'

    if is_save == 2:
        is_save = 1
    folder_address = U_dir(U_name + title_suffix, is_save,
                           z=z, **kwargs, )

    label1 = "SSI_energy"
    label2 = "EVV_energy"
    U_energy_plot(folder_address,
                  U_plot, U_name,
                  img_name_extension,
                  # %%
                  zj, sample, size_PerPixel,
                  is_save, dpi, size_fig_x, size_fig_y,
                  color_1d, ticks_num,
                  is_title_on, is_axes_on, is_mm,
                  fontsize, font,
                  # %%
                  z=z, suffix=title_suffix,
                  # %%
                  l2=l2_plot, color_1d2=color_1d2,
                  label=label1, label2=label2,
                  zj2=zj2, **kwargs, )

    suffix = "_" + label1
    U_address, ugHGU = U_save(U, U_name + suffix, folder_address,
                              is_save, is_save_txt,
                              z=z, suffix=suffix, **kwargs, )

    suffix = "_" + label2
    U_address, ugHGU = U_save(l2, U_name + suffix, folder_address,
                              is_save, is_save_txt,
                              z=z, suffix=suffix, **kwargs, )

    suffix = "_" + "zj_SSI"
    U_address, ugHGU = U_save(zj, U_name + suffix, folder_address,
                              is_save, is_save_txt,
                              z=z, suffix=suffix, **kwargs, )

    suffix = "_" + "zj_EVV"
    U_address, ugHGU = U_save(zj2, U_name + suffix, folder_address,
                              is_save, is_save_txt,
                              z=z, suffix=suffix, **kwargs, )


def U_twin_error_energy_plot_save(U, l2, l3, U_name,
                                  img_name_extension, is_save_txt,
                                  # %%
                                  zj, zj2, sample, size_PerPixel,
                                  is_save, dpi, size_fig_x, size_fig_y,
                                  # %%
                                  color_1d, color_1d2,
                                  ticks_num, is_title_on, is_axes_on, is_mm,
                                  fontsize, font,  # 默认无法 外界设置，只能 自动设置 y 轴 max 和 min 了（不是 但 类似 colorbar），还有 is_energy
                                  # %%
                                  z, **kwargs, ):
    kwargs['p_dir'] = 'GU_error(z)'
    # %%
    # print(U[-1])
    if kwargs.get("is_energy_normalized", False) == 1:
        U_plot = U / np.max(U)
        l2_plot = l2 / np.max(l2)
        title_suffix = '_energy_normalized & error - compare'
    elif kwargs.get("is_energy_normalized", False) == 2:
        U_plot = U
        l2_plot = l2 / l2[-1] * U[-1]
        title_suffix = '_energy_sync & error - compare'
    else:
        U_plot = U
        l2_plot = l2
        title_suffix = '_energy & error - compare'

    if is_save == 2:
        is_save = 1
    folder_address = U_dir(U_name + title_suffix, is_save,
                           z=z, **kwargs, )

    label1 = "SSI_energy"
    label2 = "EVV_energy"
    label3 = "distribution_error"
    U_energy_plot(folder_address,
                  U_plot, U_name,
                  img_name_extension,
                  # %%
                  zj, sample, size_PerPixel,
                  is_save, dpi, size_fig_x, size_fig_y,
                  color_1d, ticks_num,
                  is_title_on, is_axes_on, is_mm,
                  fontsize, font,
                  # %%
                  z=z, suffix=title_suffix,
                  # %%
                  l2=l2_plot, color_1d2=color_1d2,
                  label=label1, label2=label2,
                  l3=l3, label3=label3,
                  zj2=zj2, **kwargs, )

    suffix = "_" + label1
    U_address, ugHGU = U_save(U, U_name + suffix, folder_address,
                              is_save, is_save_txt,
                              z=z, suffix=suffix, **kwargs, )

    suffix = "_" + label2
    U_address, ugHGU = U_save(l2, U_name + suffix, folder_address,
                              is_save, is_save_txt,
                              z=z, suffix=suffix, **kwargs, )

    suffix = "_" + label3
    U_address, ugHGU = U_save(l3, U_name + suffix, folder_address,
                              is_save, is_save_txt,
                              z=z, suffix=suffix, **kwargs, )

    suffix = "_" + "zj_SSI"
    U_address, ugHGU = U_save(zj, U_name + suffix, folder_address,
                              is_save, is_save_txt,
                              z=z, suffix=suffix, **kwargs, )

    suffix = "_" + "zj_EVV"
    U_address, ugHGU = U_save(zj2, U_name + suffix, folder_address,
                              is_save, is_save_txt,
                              z=z, suffix=suffix, **kwargs, )


# %%

def Info_img(img_full_name):
    img_name = os.path.splitext(img_full_name)[0]
    img_name_extension = os.path.splitext(img_full_name)[1]
    img_address = get_cd() + "\\" + img_full_name  # 默认 在 相对路径下 读，只需要 文件名 即可：读于内

    folder_name = 'BASE - img_source'
    folder_address = U_dir(folder_name, 1, is_no_data_save=1)

    img_squared_full_name = "1. " + img_name + "_squared" + img_name_extension  # 除 原始文件 以外，生成的文件 均放在桌面：写出于外
    img_squared_bordered_full_name = "2. " + img_name + "_squared" + "_bordered" + img_name_extension
    img_squared_address = folder_address + '\\' + img_squared_full_name
    img_squared_bordered_address = folder_address + '\\' + img_squared_bordered_full_name

    return img_name, img_name_extension, img_address, folder_address, img_squared_address, img_squared_bordered_address


# %%

def img_squared_Read(img_full_name, U_size, **kwargs, ):
    img_name, img_name_extension, img_address, folder_address, img_squared_address, img_squared_bordered_address \
        = Info_img(img_full_name)
    img_squared = cv2.imdecode(np.fromfile(img_squared_address, dtype=np.uint8), 0)  # 按 相对路径 + 灰度图 读取图片

    # 更新逻辑：无论是 U_read 还是 img_squared_boardered_Read，U_size 都以最大尺寸为主
    # if kwargs.get("is_U_size_x_structure_side_y", 0) == 1:
    #     size_PerPixel = U_size / img_squared.shape[1]  # 如果 由图的 x 向 列数（宽度）与 U_size 决定 像素点 的 尺寸
    #     # size_PerPixel = size_PerPixel_x
    # else:
    #     size_PerPixel = U_size / img_squared.shape[0]  # Unit: mm / 个 每个 像素点 的 尺寸，相当于 △x = △y = △z
    #     # size_PerPixel = size_PerPixel_y
    # # Size_PerPixel 统一以 图片 y 行向 为准

    init_Set("img_name_extension", img_name_extension)

    return img_name, img_name_extension, img_address, folder_address, \
           img_squared_address, img_squared_bordered_address, \
           img_squared


# %%
# 导入 方形，以及 加边框 的 图片

def img_squared_bordered_Read(img_full_name,
                              U_size, dpi,
                              is_phase_only, **kwargs, ):
    img_name, img_name_extension, img_address, folder_address, \
    img_squared_address, img_squared_bordered_address, \
    img_squared = img_squared_Read(img_full_name, U_size, **kwargs, )

    img_squared_bordered = cv2.imdecode(np.fromfile(img_squared_bordered_address, dtype=np.uint8),
                                        0)  # 按 相对路径 + 灰度图 读取图片
    Ix, Iy = img_squared_bordered.shape[0], img_squared_bordered.shape[1]

    # 不覆盖 Ix 和 size_fig、size_PerPixel 等，因为 结构是 参照 U_size 的 尺度来生成的，而 U_size 最好不要大到 全图。
    # 额 no no no，U_size 本来就没大到全图：它在 img_squared_Read 中已经决定了 只与 img_squared 相关。
    # 但之后 要给出 矩形化后的 U 的 另一条边 U_size_y 和 U_size_x 的长度，以供 外部 调用
    # 且 Ix, Iy 本来就是 squared 后的 变大了的 尺寸，这里 调整的也是 变大后的，最终的尺寸
    # 还有，得与 U_read 同步：U_size 干脆都以最大尺寸为主
    from fun_img_Resize import U_resize
    img_squared_bordered = U_resize(img_squared_bordered, kwargs.get("U_pixels_x", 0), kwargs.get("U_pixels_y", 0),
                                    Ix, Iy)
    Ix, Iy = img_squared_bordered.shape[0], img_squared_bordered.shape[1]  # 覆盖旧的 Ix, Iy

    img_squared_bordered_resize_full_name = "3. " + img_name + "_squared" + "_bordered" + "_resize" + img_name_extension
    img_squared_bordered_resize_address = folder_address + "\\" + img_squared_bordered_resize_full_name
    cv2.imencode(img_name_extension, img_squared_bordered)[1].tofile(img_squared_bordered_resize_address)

    if is_phase_only == 1:
        U = np.power(math.e, (img_squared_bordered.astype(np.complex128()) / 255 * 2 * math.pi - math.pi) * 1j)  # 变成相位图
    else:
        U = img_squared_bordered.astype(np.complex128)

    # 更新逻辑：无论是 U_read 还是 img_squared_boardered_Read，U_size 都以最大尺寸为主
    if kwargs.get("is_U_size_x_structure_side_y", 0) == 1:
        size_fig = Iy / dpi  # 由 x 向 列数 决定
        size_PerPixel = U_size / Iy
        U_size_y = size_PerPixel * Ix  # U_size_y 等于 U_size_x = img_squared 对应的 U_size
        init_Set("U_side", U_size_y)
    else:
        size_fig = Ix / dpi  # size_fig 默认 也由 y 向 行数 决定。
        # U_size != size_PerPixel * Ix
        # 而有 U_size == size_PerPixel * img_squared.shape[0]，已经是 squared 之后的了，所以直接
        size_PerPixel = U_size / Ix
        U_size_x = size_PerPixel * Iy  # 以致于 从图片 img_squared_bordered_Read 里 读到的 U 总是 方的，但走 U_Read 就不是了
        init_Set("U_side", U_size_x)

    init_Set("Ix", Ix)
    init_Set("Iy", Iy)
    init_Set("size_PerPixel", size_PerPixel)
    init_Set("size_fig", size_fig)
    init_Set("size_fig_x", size_fig * Get("size_fig_x_scale"))
    init_Set("size_fig_y", size_fig * Get("size_fig_y_scale"))

    return img_name, img_name_extension, img_squared, size_PerPixel, size_fig, Ix, Iy, U


# %%

def U_read_only(U_name, is_save_txt):
    if len(U_name.split('.')) == 2 and \
            len(find_NOT_nums(U_name.split('.')[0])) == 0 and len(find_NOT_nums(U_name.split('.')[1])) == 0:
        # 如果 U_name 完全符合 Data_Seq 的 语法规范
        ugHGU, U_address = get_Data_new_attrs(U_name, "ugHGU", "U_address")  # 变量数 不等，右边会 自动解包
    else:
        if ".txt" in U_name or ".mat" in U_name:
            U_full_name = U_name
        else:
            U_full_name = U_name + (is_save_txt and ".txt" or ".mat")
        U_address = Get("root_dir") + "\\" + U_full_name
        U_name_no_seq, method_and_way, Part_2, ugHGU, ray_seq = split_parts(U_name)

    U = np.loadtxt(U_address, dtype=np.complex128()) if is_save_txt == 1 else loadmat(U_address)[ugHGU]  # 加载 复振幅场

    return U


# %%
# 导入 方形 图片，以及 U

def U_Read(U_name, img_full_name,
           U_size, dpi,
           is_save_txt, **kwargs, ):
    img_name, img_name_extension, img_address, folder_address, \
    img_squared_address, img_squared_bordered_address, \
    img_squared = img_squared_Read(img_full_name, U_size, **kwargs, )

    U = U_read_only(U_name, is_save_txt)
    Ix, Iy = U.shape[0], U.shape[1]

    from fun_img_Resize import U_resize
    U = U_resize(U, kwargs.get("U_pixels_x", 0), kwargs.get("U_pixels_y", 0), Ix, Iy)
    Ix, Iy = U.shape[0], U.shape[1]  # 覆盖旧的 Ix, Iy

    U_squared_bordered_resize_full_name = "3. " + U_name + "_squared" + "_bordered" + "_resize" + img_name_extension
    U_squared_bordered_resize_address = folder_address + "\\" + U_squared_bordered_resize_full_name
    cv2.imencode(img_name_extension, U)[1].tofile(U_squared_bordered_resize_address)

    if kwargs.get("is_U_size_x_structure_side_y", 0) == 1:
        size_fig = Iy / dpi  # 由 x 向 列数 决定
        size_PerPixel = U_size / Iy  # size_PerPixel = size_PerPixel_x
        U_size_y = size_PerPixel * Ix  # U_size == size_PerPixel * Ix
        init_Set("U_side", U_size_y)
    else:
        size_fig = Ix / dpi  # size_fig、size_PerPixel 默认 由 y 向 行数 决定。
        size_PerPixel = U_size / Ix  # Unit: mm / 个 每个 像素点 的 尺寸，相当于 △x = △y = △z
        # Size_PerPixel 统一以 图片 y 行向 为准： size_PerPixel = size_PerPixel_y
        # 覆盖 img_squared_Read 所得到的 size_PerPixel
        U_size_x = size_PerPixel * Iy  # U_size == size_PerPixel * Ix
        init_Set("U_side", U_size_x)

    init_Set("Ix", Ix)
    init_Set("Iy", Iy)
    init_Set("size_PerPixel", size_PerPixel)
    init_Set("size_fig", size_fig)
    init_Set("size_fig_x", size_fig * Get("size_fig_x_scale"))
    init_Set("size_fig_y", size_fig * Get("size_fig_y_scale"))

    return img_name, img_name_extension, img_squared, size_PerPixel, size_fig, Ix, Iy, U
