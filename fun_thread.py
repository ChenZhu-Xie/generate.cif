# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 14:41:11 2021

@author: Xcz
"""

import threading
import time
import inspect
from fun_built_in import var_or_tuple_to_list

#%%
# 一个接受 任何参数，并且啥也不做的 参数黑洞，垃圾桶（有点 linux bash 中的 那某命令 的 感觉：吞掉所有输出）

def noop(*args, **kwargs): pass


# %%
# 多线程 v1.1

def my_thread(threads_num, fors_num,
              fun_1, fun_2, fun_3,
              *args,
              is_ordered=1, is_print=1,
              **kwargs, ):

    from fun_global_var import init_tset, Set, Get, tree_print # 放在外面（上面）会报 循环引用 的错

    is_end, add_level = kwargs.get("is_end", 0), kwargs.get("add_level", 0)
    kwargs.pop("is_end", None); kwargs.pop("add_level", None)  # 该 def 子分支 后续默认 is_end = 0，如果 kwargs 还会被 继续使用 的话。
    
    thread_name = init_tset("thread", 0)[1] # 只取其名字
    for_name = init_tset("for", 0)[1] # 只取其名字

    con = threading.Condition()  # 锁不必定义为全局变量

    class Producer(threading.Thread):
        """线程 生产者"""

        def __init__(self, threads_num, fors_num):
            self.threads_num = threads_num
            self.fors_num = fors_num
            self.for_th = 0  # 生产出的 第几个 for_th，这个不必定义为全局变量
            super().__init__()

        def run(self):
            con.acquire()
            while True:

                if self.for_th >= self.fors_num and Get(for_name) == self.fors_num:  # 退出生产线程 的 条件：p 线程 完成 其母线程功能，且 最后一个 t 线程 完成其子线程功能
                    break
                else:
                    if Get(thread_name) >= self.threads_num or self.for_th == self.fors_num:  # 暂停生产线程 的 条件： 运行线程数 达到 设定，或 p 线程 完成 其母线程功能
                        con.notify()
                        con.wait()
                    else:
                        # print(self.for_th)
                        t = Customer('thread:%s' % Get(thread_name), self.for_th)
                        t.setDaemon(True)
                        t.start()

                        Set(thread_name, Get(thread_name) + 1)
                        # print('已生产了 共 {} 个 线程'.format(thread_th))
                        self.for_th += 1
                        # print('已算到了 第 {} 个 for_th'.format(self.for_th))
                        # time.sleep(1)
            con.release()

    class Customer(threading.Thread):
        """线程 消费者"""

        def __init__(self, name, for_th):
            self.thread_name = name
            self.for_th = for_th
            self.list = []
            super().__init__()

        def run(self):
            """----- your code begin 1 -----"""
            '''
            既然 python 你要这么为难我，我就直接让 函数返回的对象 丢弃其外层的 圆括号，并加方括号，
            使得方括号内 没有更多的方括号或圆括号，并且最外层的方括号不消失，
            这样无论如何都可以解包，且只需要解一次包，就直达内层
            '''
            List = var_or_tuple_to_list(fun_1(self.for_th, fors_num,
                                              **kwargs, ))  # 把 函数1 的 运行结果 强制转换 为 1 个 list
            self.list.append(List)  # 把这个 list 放入 外层 list 中
            # print(List)
            """----- your code end 1 -----"""

            con.acquire()  # 上锁

            if is_ordered == 1:

                while True:
                    if Get(for_name) == self.for_th:
                        # print(self.for_th)
                        """----- your code begin 2 -----"""
                        # print(self.list[0])
                        List = var_or_tuple_to_list(fun_2(self.for_th, fors_num, *self.list[0],
                                                          **kwargs, ))  # 取 外层 list 储存的 第 1 个 list，并对其 解包后，作为参数 传入 函数2
                        self.list.append(List)
                        """----- your code end 2 -----"""
                        Set(for_name, Get(for_name) + 1)
                        break
                    else:
                        con.notify()
                        con.wait()  # 但只有当 for_th 不等于 self.for_th， 才等待
            else:

                # print(self.for_th)
                """----- your code begin 2 -----"""
                List = var_or_tuple_to_list(fun_2(self.for_th, fors_num, *self.list[0],
                                                  **kwargs, ))
                self.list.append(List)
                """----- your code end 2 -----"""
                Set(for_name, Get(for_name) + 1)

            Set(thread_name, Get(thread_name) - 1)  # 在解锁之前 减少 1 个线程数量，以便 p 线程 收到消息后，生产 1 个 线程出来
            con.notify()  # 无论如何 都得通知一下 其他线程，让其别 wait() 了
            con.release()  # 解锁

            """----- your code begin 3 -----"""
            List = var_or_tuple_to_list(fun_3(self.for_th, fors_num, *self.list[1],
                                              **kwargs, ))
            self.list.append(List)
            """----- your code end 3 -----"""

    tick_start = time.time()

    p = Producer(threads_num, fors_num)
    p.setDaemon(True)
    p.start()
    p.join()  # 添加join使 p 线程执行完

    # if thread_name == "thread_0":  # 如果 调用该 my_thread 的 函数，其名字 不含 Fun
    if "Fun" not in inspect.stack()[1][3]:
        is_print and print(tree_print(is_end) + "{} --> consume time: {} s".format(inspect.stack()[1][3], time.time() - tick_start))

#%%
# 多线程 v1.0

# def my_thread(threads_num, fors_num,
#               fun_1, fun_2, fun_3,
#               *args,
#               is_ordered = 1, is_print = 1,
#               **kwargs, ):
#
#     global thread_th, for_th # 好怪，作为 被封装 和 被引用的 函数，还得在 这一层 声明 全局变量，光是在 内层 子线程 里声明 的话，没用。
#     thread_th = 0
#     for_th = 0
#
#     con = threading.Condition() # 锁不必定义为全局变量
#
#     class Producer(threading.Thread):
#         """线程 生产者"""
#         def __init__(self, threads_num, fors_num):
#             self.threads_num = threads_num
#             self.fors_num = fors_num
#             self.for_th = 0 # 生产出的 第几个 for_th，这个不必定义为全局变量
#             super().__init__()
#
#         def run(self):
#             global thread_th
#
#             con.acquire()
#             while True:
#
#                 if self.for_th >= self.fors_num and for_th == self.fors_num: # 退出生产线程 的 条件：p 线程 完成 其母线程功能，且 最后一个 t 线程 完成其子线程功能
#                     break
#                 else:
#                     if thread_th >= self.threads_num or self.for_th == self.fors_num : # 暂停生产线程 的 条件： 运行线程数 达到 设定，或 p 线程 完成 其母线程功能
#                         con.notify()
#                         con.wait()
#                     else:
#                         # print(self.for_th)
#                         t = Customer('thread:%s' % thread_th, self.for_th)
#                         t.setDaemon(True)
#                         t.start()
#
#                         thread_th += 1
#                         # print('已生产了 共 {} 个 线程'.format(thread_th))
#                         self.for_th += 1
#                         # print('已算到了 第 {} 个 for_th'.format(self.for_th))
#                         # time.sleep(1)
#             con.release()
#
#     class Customer(threading.Thread):
#         """线程 消费者"""
#         def __init__(self, name, for_th):
#             self.thread_name = name
#             self.for_th = for_th
#             self.list = []
#             super().__init__()
#
#         def run(self):
#             global thread_th, for_th
#             """----- 你 需累积的 全局变量，替换 最末一个 g3_z_plus_dz_shift -----"""
#
#             """----- your code begin 1 -----"""
#             # fun_1(self.for_th, fors_num, *arg[ : num_1 - 1 ]
#             # self.list.append(fun_1(self.for_th, fors_num))
#             # self.list.extend([fun_1(self.for_th, fors_num)])
#             # self.list.append([fun_1(self.for_th, fors_num)]) # 函数 返回多个变量时，默认返回的 是个元组，当返回单个变量时，加个中括号之后可解包————但返回多个变量时，加个中括号再解包，仍是个元组
#             # self.list.append((fun_1(self.for_th, fors_num))) # 所以 要用到 2 个元组 相抵消，以使得不论输出单个 变量，还是多个变量，都变成 单层 的 tuple————但单层的 tuple 遇上 单个输出，就又没 tuple 了，无语，这样之后 解包的时候 又出错
#             '''
#             既然 python 你要这么为难我，我就直接让 函数返回的对象 丢弃其外层的 圆括号，并加方括号，
#             使得方括号内 没有更多的方括号或圆括号，并且最外层的方括号不消失，
#             这样无论如何都可以解包，且只需要解一次包，就直达内层
#             '''
#             List = var_or_tuple_to_list(fun_1(self.for_th, fors_num,
#                                               **kwargs, )) # 把 函数1 的 运行结果 强制转换 为 1 个 list
#             self.list.append(List) # 把这个 list 放入 外层 list 中
#             # print(List)
#             """----- your code end 1 -----"""
#
#             con.acquire() # 上锁
#
#             if is_ordered == 1:
#
#                 while True:
#                     if for_th == self.for_th:
#                         # print(self.for_th)
#                         """----- your code begin 2 -----"""
#                         # fun_2(self.for_th, fors_num, *arg[ num_1: num_1 + num_2 - 1 ])
#                         # self.list.append(fun_2(self.for_th, fors_num, self.list[0])
#                         # self.list.append(fun_2(self.for_th, fors_num, *self.list[0]))
#                         # self.list.extend([fun_2(self.for_th, fors_num, *self.list[0])])
#                         # self.list.append([fun_2(self.for_th, fors_num, *self.list[0])])
#                         # self.list.append((fun_2(self.for_th, fors_num, *self.list[0]))) # 双层 tuple 等价于 单层 tuple，所以这里有一层 tuple 不用加；
#                         # print(self.list[0])
#                         List = var_or_tuple_to_list(fun_2(self.for_th, fors_num, *self.list[0],
#                                                           **kwargs, )) # 取 外层 list 储存的 第 1 个 list，并对其 解包后，作为参数 传入 函数2
#                         self.list.append(List)
#                         """----- your code end 2 -----"""
#                         for_th += 1
#                         break
#                     else:
#                         con.notify()
#                         con.wait() # 但只有当 for_th 不等于 self.for_th， 才等待
#             else:
#
#                 # print(self.for_th)
#                 """----- your code begin 2 -----"""
#                 # fun_2(self.for_th, fors_num, *arg[ num_1: num_1 + num_2 - 1 ])
#                 # self.list.append(fun_2(self.for_th, fors_num, self.list[0])
#                 # self.list.append(fun_2(self.for_th, fors_num, *self.list[0]))
#                 # self.list.extend([fun_2(self.for_th, fors_num, *self.list[0])])
#                 # self.list.append([fun_2(self.for_th, fors_num, *self.list[0])])
#                 # self.list.append((fun_2(self.for_th, fors_num, *self.list[0]))) # 当全是 多变量 输出，即全是 tuple 输出时，是可以正确算的
#                 List = var_or_tuple_to_list(fun_2(self.for_th, fors_num, *self.list[0],
#                                                   **kwargs, ))
#                 self.list.append(List)
#                 """----- your code end 2 -----"""
#                 for_th += 1
#
#             thread_th -= 1 # 在解锁之前 减少 1 个线程数量，以便 p 线程 收到消息后，生产 1 个 线程出来
#             con.notify() # 无论如何 都得通知一下 其他线程，让其别 wait() 了
#             con.release() # 解锁
#
#             """----- your code begin 3 -----"""
#             # fun_3(self.for_th, fors_num, *arg[ num_1 + num_2 : num_1 + num_2 + num_3 - 1 ])
#             # fun_3(self.for_th, fors_num, *arg[ num_1 + num_2 : ])
#             # self.list.append(fun_3(self.for_th, fors_num, *self.list[1]))
#             # self.list.extend([fun_3(self.for_th, fors_num, *self.list[1])])
#             # self.list.append([fun_3(self.for_th, fors_num, *self.list[1])])
#             # self.list.append((fun_3(self.for_th, fors_num, *self.list[1]))) # 当全是 多变量 输出，即全是 tuple 输出时，是可以正确算的
#             List = var_or_tuple_to_list(fun_3(self.for_th, fors_num, *self.list[1],
#                                               **kwargs, ))
#             self.list.append(List)
#             """----- your code end 3 -----"""
#
#     tick_start = time.time()
#
#     p = Producer(threads_num, fors_num)
#     p.setDaemon(True)
#     p.start()
#     p.join() # 添加join使 p 线程执行完
#
#     is_print and print("----- consume time: {} s -----".format(time.time() - tick_start))