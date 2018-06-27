# coding=utf-8
import sys, getopt

# 文法规则的文法规则
# G[A]:
# A->U "->" C
# U->[A-Z]
# C->D{"|"D}
# D->{a-zA-Z}

# Example 
# A->Ba|c
# B->d

class LL_1_Analyzer:

    # @param file_name 文件名
    def __init__(self, file_name):
        self.file_name = file_name
        self.rule_list = []  #保存规则 A->a
        self.non_term = []  # 非终结符号集合
        self.term = []  # 终结符号集合
        self.first_left_char = []  # 第一个字母集合
        self.first_set = []  # first集合[[A,a,d,c],....]
        self.follow_set = []  # follow集合[[A,a,d,c],....]
        self.open_file()

    # 打开文件
    def open_file(self):
        f = open(self.file_name, "r")
        self.get_token(f)
        f.close()

    # @param file 文件对象
    def get_token(self, file):
        f_line = file.readlines() 
        for x in f_line:
            print (x)
        for x in f_line:
            self.get_rule(x)
            self.A(x)
        print (self.rule_list)
        for n in self.rule_list:
            self.A(n)
        
    # 把一条规则分割为产生式，保存在self.rule_list里
    # A->a|b 分割为 A->a 和 A->b
    # @param x 一条文法规则
    def get_rule(self, x):
        if x[-1] == "\n":  # 删除换行符
            x = x[:-1]
        l_x = x.split("->")  #根据 -> 分割字符串
        s = l_x[0] + "->"
        r_string = l_x[1].split("|")  # 根据 | 分割->右边的字符串
        for r in r_string:
            l_string = s
            l_string = l_string + r
            self.rule_list.append(l_string)

    def error(self):
        print("error")

    # 求 First 集合
    # @param ch 要求的符号
    def first(self, ch):
        tmp = []
        for n in self.rule_list:
            if n[0] == ch and c[3] >= "a" and c[3] <= "z":
                tmp.append(n[3])
            elif n[0] == ch and c[3] >= "A" and c[3] <= "Z":
                self.first(c[3])
        self.first_set.append(tmp)

    # 返回ch的first集合
    # @param ch 要返回的字符
    def get_first(self, ch):
        for n in self.first_set:
            if len(self.first_set) > 0 and len(n) > 0:
                if n[0] == ch:
                    return n[1:]

    # 返回ch的follow集合
    # @param ch 要返回的字符
    def get_follow(self, ch):
        for n in self.follow_set:
            if n[0] == ch:
                return n[1:]


    # 求 Follow 集合
    # @param ch 要求的符号
    def follow(self, ch):
        start = "*"
        tmp = []
        tmp.append("$")
        for n in self.rule_list:
            n = n + "$"
            index = n.rfind(ch)
            if n[index + 1] >= "a" and n[index + 1] <= "z":
                tmp.append(n[index])
            if n[index + 1] >= "A" and n[index + 1] <= "Z":
                get_first = self.get_first(n[index])
                get_follow = self.get_follow(n[index])
                if get_first != None:
                    if "*" not in get_first and get_first:
                        tmp = tmp + get_first

                    if "*" in get_first or n[index + 1] == "$":
                        tmp = tmp + get_follow
        self.follow_set.append(tmp)




    # @param c 匹配的字符串
    def match(self, c):
        if c == "->":
            a = 1
        elif c == "|":
            a = 1

    # 非终结符号A
    # @param ch 一条规则 比如 A->Ba|c
    def A(self, ch):
        self.U(ch.split("->")[0])
        self.match("->")
        self.C(ch.split("->")[1])

    # 非终结符号U
    # @param ch 一条规则的左边的非终结符号
    def U(self, ch):
        self.non_term.append(ch)  # 保存非终结符号
        # do something
        a = 1

    # 非终结符号C
    # @param ch 一条规则的->右边的string
    def C(self, ch):
        # do something
        save_n = []
        for n in ch.split("|"):
            save_n.append(n)
            r = self.D(n)

        if 1 in r:  # 消除左公因子
            a = r[0] + "("
            b = ""
            for n in ch.split("|"):
                if n[0] == r[0]:
                    a = a + n[1:] + "|"
                else:
                    b = b + n + "|"
            a = a + b + ")"
            print ("delete left public factor")
            print (a)

        elif 2 in r:  # 消除左递归
            b = ""
            for n in ch.split("|"):
                if n[0] == r[0]:
                    a = n[1:]
                else:
                    b = b + n + "|"
            a = "{" + b + "}" + a
            print ("delete left recursion")
            print (a)



    # 非终结符号D
    # @param ch 一条规则的->右边的{a-zA-Z}
    def D(self, ch):
        # 判断左公因子
        self.first_left_char = []
        if ch[0] in self.first_left_char:
            print ("left public factor")
            return [ch[0],1]

        # 判断左递归
        if ch[0] in self.non_term:
            print ("left recursion")
            return [ch[0],2] 

        self.first_left_char.append(ch[0])

        for c in ch:
            if c >= "A" and c <= "Z":
                self.non_term.append(c)
                self.first(c)  # 求first集合
                self.follow(c)  # 求follow集合
            elif c >= "a" and c <= "z":
                self.term.append(c)

        return ["$",3]

def main(argv):
    file_name = ""
    try:
        opts, args = getopt.getopt(argv, "hf:", ["file_name="])
    except getopt.GetoptError:
        print ("main.py -f \"file_name\"")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print ("main.py -f \"file_name\"")
            sys.exit()
        elif opt in ("-f", "--f"):
            file_name = arg
    if file_name == "":
        print ("main.py -f \"file_name\"")

    ob = LL_1_Analyzer(file_name)


if __name__ == "__main__":
    main(sys.argv[1:])