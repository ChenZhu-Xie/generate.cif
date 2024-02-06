![fig](https://raw.githubusercontent.com/ChenZhu-Xie/generate.cif/master/img/cover1.png "Generate a single『1D PPLN』at the wafer level")

# Generate ".cif" file (for L-edit)

## About
* This project 👉 [generate.cif](https://github.com/ChenZhu-Xie/generate.cif) serves for
    * Automatic, Batch, Custom designs of electrode patterns
    * Translate the pattern into coordinate points and generate .cif
    * eventually for photolithography on material surfaces

## Description
* Usage: Generate hologram (e.g. PPLN) → .cif file
* Features: Automation, Batch, Customization, and Multi-thread
    * Automation: Just input key parameters such as quantum number $l$, number of pixels, etc.
    * Batch: 12 different 1D,2D PPLNs can be orderly integrated on a wafer
    * Customization: Each PPLN can be individually customized with its own pattern
    * Multi-thread: Accelerating (edge extraction, drawing, and .cif generation processes)

* Extract the closed curves of the positive/negative domain edges of irregular holograms separately, and provide the clockwise/counterclockwise sequential coordinates of the connected closed curves
    * ![fig](https://github.com/ChenZhu-Xie/generate.cif/raw/master/img/l=1.png "Extract closed curve arrays corresponding to polygon arrays")
* More than 12 pieces of 1D,2D PPLNs can be customized on a 3-inch wafer
    * ![fig](https://raw.githubusercontent.com/ChenZhu-Xie/generate.cif/master/img/cover2.png "Generate 12 different『1D & 2D PPLN arrays』at the wafer level")

## Inplementation
1. Run any .py file that does not start with "fun" to see the effect.
2. The approximate order of the call chain is .py files starting with "d <-- c <-- b <-- a <-- fun".

## History
* This project 👉 [generate.cif](https://github.com/ChenZhu-Xie/generate.cif) was mainly maintained during
    * (World time) 2021.08 - 2022.11
    * (Personal stage) summer vacation in the second semester - the fifth semester (of postgraduate studies)
    * (Personal stage) the (0.9 - 2.2) / 5.0 year of PhD Program
    * (Personal time) 23 years & 4 months - 24 years & 7 months

<!-- ## Software Architecture
Software architecture description

## Installation

1.  xxxx
2.  xxxx
3.  xxxx

## Instructions

1.  xxxx
2.  xxxx
3.  xxxx

## Contribution

1.  Fork the repository
2.  Create Feat_xxx branch
3.  Commit your code
4.  Create Pull Request


## Gitee Feature

1.  You can use Readme\_XXX.md to support different languages, such as Readme\_en.md, Readme\_zh.md
2.  Gitee blog [blog.gitee.com](https://blog.gitee.com)
3.  Explore open source project [https://gitee.com/explore](https://gitee.com/explore)
4.  The most valuable open source project [GVP](https://gitee.com/gvp)
5.  The manual of Gitee [https://gitee.com/help](https://gitee.com/help)
6.  The most popular members  [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/) -->
