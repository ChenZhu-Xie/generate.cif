<!-- ![fig](https://raw.githubusercontent.com/ChenZhu-Xie/generate.cif/master/img/cover1.png "生成 晶圆级 单个『1 维 PPLN』的 .cif 文件") -->
![fig](https://gitee.com/ChenZhu-Xie/generate.cif/raw/master/img/cover1.png "生成 晶圆级 单个『1 维 PPLN』的 .cif 文件")

# 生成 ".cif" 文件 (再用 L-edit 打开)

## 关于
* 该项目 👉 [generate.cif](https://gitee.com/ChenZhu-Xie/generate.cif) 服务于
    * 全自动、批量化、自定义 设计电极图案
    * 将图案 “翻译为” 坐标点，并生成 .cif
    * 最终用于 在材料表面 光刻

## 介绍
* 用途：生成 全息图 (PPLN 等) → .cif 文件
* 特点：全自动、批量化、自定义、多线程
    * 全自动：只需输入 关键参数 如 量子数 l、像素数 size 等
    * 批量化：可在一片 晶圆上 订制化集成 12 块 不同的 1D,2D PPLN
    * 自定义：其中，每一块 PPLN 都可单独 定制其图案
    * 多线程：加速（边缘提取、绘图 和 .cif 生成过程）
    
* 提取 非规则全息图 正/负畴边沿 封闭曲线、每条曲线 正/逆时针顺序坐标
    * ![fig](https://gitee.com/ChenZhu-Xie/generate.cif/raw/master/img/l=1.png "提取 多边形阵列 对应的 封闭曲线阵列")
* 在一片 3 英寸晶圆上 批量定制 12 块 1D,2D PPLN
    * ![fig](https://gitee.com/ChenZhu-Xie/generate.cif/raw/master/img/cover2.png "直接生成 晶圆级『12 个不同的 1、2 维 PPLN 阵列』的 .cif 文件")
<!-- ![fig](https://raw.githubusercontent.com/ChenZhu-Xie/generate.cif/master/img/cover2.png "直接生成 晶圆级『12 个不同的 1、2 维 PPLN 阵列』的 .cif 文件") -->

## 实施
1. 运行任何一个不以 "fun" 开头的 .py 文件，即可查看效果。
2. 调用链 大致顺序 为以 "d <-- c <-- b <-- a <-- fun" 开头的 .py 文件。

## 历史
* 该项目 👉 [generate.cif](https://gitee.com/ChenZhu-Xie/generate.cif) 主要维护于
    * （世界时间）2021.08 - 2022.11
    * （个人阶段）研一下学期 暑假 —— 研三/博一 上学期
    * （个人阶段）直博生涯 的 第 (0.9 - 2.2) / 5.0 年
    * （个人时间）23 岁 4 月 - 24 岁 7 月

<!-- ## 软件架构
软件架构说明


## 安装教程

1.  xxxx
2.  xxxx
3.  xxxx

## 使用说明

1.  xxxx
2.  xxxx
3.  xxxx

## 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


## 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/) -->
