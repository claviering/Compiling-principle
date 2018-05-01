# coding=utf-8
# 输入NFA
# 输出DFA

import NFA, sys, getopt

class Node():

    def __init__(self, start, ch, end):
        self.start_condition_list = start  # 开始状态的集合
        self.ch = ch  # 字符
        self.end_condition_list = end  # 结束状态的集合


class NFA_To_DFA:

    def __init__(self, string):
        # 两个链表保存NFA 0->a->2 start_map[0] = a end_map[0] = 2
        # NFA可能有一对多的关系，里面也保存为列表
        self.string = string  # 要处理的正则表达式
        self.alp = []  # 字符表
        self.start_map = []
        self.end_map = []  
        self.NFA_condition = []  # 保存机器的开始，结束状态
        self.condition_set = []  # 保存状态集合的列表[[],[],[]...]
        self.DFA_list = []  # 保存DFA

        self.pre_oper()
        self.get_alp_from_string()

    # 将NFA，映射为两个列表
    def pre_oper(self):
        return_list = NFA.NFA(self.string)
        self.NFA_condition = NFA.get_NFA_condition()
        # 根据开始状态数字排序
        sorted_NFA_list = sorted(return_list, key=lambda Node: Node.start_condition)

        index_list = 0
        for tmp in sorted_NFA_list:
            if index_list == tmp.start_condition:
                self.start_map.append([tmp.ch])
                self.end_map.append([tmp.end_condition])
                index_list += 1
            else:
                self.start_map[tmp.start_condition].append(tmp.ch)
                self.end_map[tmp.start_condition].append(tmp.end_condition)


    # 从字符串里找出不重复的字母
    def get_alp_from_string(self):
        index = 0
        while index < len(self.string):
            ch = self.string[index]
            index += 1
            if ch >= "a" and ch <= "z" and ch not in self.alp:
                self.alp.append(ch)


    # 从 开始状态经过ch字符到达的结束状态,只走一步
    # @param start = [] 开始状态列表
    # @param ch = char 转移字符
    # return 结束状态的列表
    def move(self, start, ch):
        end_pos = []  # 结束状态列表
        # 遍厉每个 开始状态
        for s in start:
            try:
                start_list = self.start_map[s]
            except:
                continue
            else:
                len_start_list = len(start_list)
                for index in range(len_start_list):
                    if start_list[index] == ch:
                        end_pos.append(self.end_map[s][index])

        return end_pos

    # 添加一个DFA到列表
    # @param start 开始状态的
    def add_DFA_list(self, start, ch, end):
        tmp = Node(start, ch, end)
        self.DFA_list.append(tmp)

    #输出DFA
    def print_DFA(self):
        print ("DFA:")
        for i in self.DFA_list:
            print (i.start_condition_list)
            print ("->" + i.ch + "->")
            print (i.end_condition_list)
            print ("--------------------")
            

    # Dstates 子集构造法
    def make_condition_set(self):
        Dstates = []
        first_pos = [self.NFA_condition[0]]  # 开始状态的集合
        # T就开始状态+进过*转化的集合
        T = first_pos
        # 找出所有从开始经过 * 字符到达的状态 保存在T中
        T += self.move(T, "*")

        Dstates.append(T)
        mark = 0  # 标记有多少个状态是用过的
        while mark < len(Dstates):
            for c in self.alp:
                all_ok = []
                # 转移多个字符和*
                tmp = Dstates[mark]
                while 1 == 1:
                    # 转化一个字符
                    t = self.move(tmp, c)
                    tmp = tmp + t
                    tmp = list(set(tmp))
                    # 加上*的转化
                    tmp += self.move(tmp, "*")
                    tmp = list(set(tmp))
                    all_ok = list(set(all_ok))
                    if all_ok == tmp:
                        break
                    else:
                        all_ok = tmp
                if tmp not in Dstates and len(tmp) > 0:
                    Dstates.append(tmp)
                    self.add_DFA_list(Dstates[mark], c, tmp)
            mark += 1

        self.condition_set = Dstates

def main(argv):
    st = ""
    try:
        opts, args = getopt.getopt(argv, "hs:", ["st="])
    except getopt.GetoptError:
        print ("DFA.py -s \"string\"")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print ("DFA.py -s \"string\"")
            sys.exit()
        elif opt in ("-s", "--st"):
            st = arg
    b = NFA_To_DFA(st)
    b.make_condition_set()
    b.print_DFA()

if __name__ == "__main__":
    main(sys.argv[1:])
