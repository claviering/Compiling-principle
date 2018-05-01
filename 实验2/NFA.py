# coding=utf-8
# 输入正则表达式
# 输出NFA，结果保存在NFA_list

# 机器的开始和结束状态
class Condition:
    def __init__(self, start_condition, end_condition):
        self.start_condition = start_condition
        self.end_condition = end_condition

class Node:

    # 一个机器的开始和结束状态
    # @param start_condition 开始状态
    # @param ch 字符
    # @param end_condition 结束状态
    def __init__(self, start_condition, ch, end_condition):
        self.start_condition = start_condition
        self.ch = ch
        self.end_condition = end_condition

class Reg_To_NFA:

    # 构造函数，初始化正则表达式为字符串
    def __init__(self):
        self.string = ""  # 正则表达式
        self.condition = 0  # 状态，从零开始，不重复使用
        self.condition_list = [] # 保存Condition节点, 01位置保存整台机器的，23位置保存最新加入的
        self.oper_list = []  # 运算符列表
        self.latest_list = [0,1]  # 保存最新机械的开始结束状态
        self.NFA_list = []  # NFA表

    # 返回整台机器的开始结束状态
    def return_NFA_condition(self):
        return [self.condition_list[0].start_condition, self.condition_list[0].end_condition]
    # 对正则表达式预处理，加入连接符号&
    def pre_string(self):
        if len(self.string) == 0:
            return
        index = 0;
        tmp_string = self.string[index]
        lenght = len(self.string)
        index += 1
        while lenght > index:
            tmp = self.string[index]
            index += 1
            # ab a*b a*() ()() ()a a()
            if tmp_string[-1] >= "a" and tmp_string[-1] <= "z" and tmp >= "a" and tmp <= "z": 
                tmp_string += "&"
                tmp_string += tmp
            elif tmp_string[-1] >= "a" and tmp_string[-1] <= "z" and tmp == "(": 
                tmp_string += "&"
                tmp_string += tmp
            elif tmp_string[-1] == "*" and tmp >= "a" and tmp <= "z":
                tmp_string += "&"
                tmp_string += tmp
            elif tmp_string[-1] == "*" and tmp == "(":
                tmp_string += "&"
                tmp_string += tmp 
            elif tmp_string[-1] == ")" and tmp == "(":
                tmp_string += "&"
                tmp_string += tmp 
            elif tmp_string[-1] == ")" and tmp >= "a" and tmp <= "z":
                tmp_string += "&"
                tmp_string += tmp
            else:
                tmp_string += tmp
        self.string = tmp_string


    def print_NFA(self):
        print ("NFA:")
        for tmp in self.NFA_list:
            print (str(tmp.start_condition) +  "->" + tmp.ch + "->" + str(tmp.end_condition))
        print ("-------------------------")
            
    # 添加一个机器到list
    # @param start_condition 机器是开始状态
    # @param ch 字符
    # @param end_condition 机器的结束状态
    def add_to_NFA(self, start_condition, ch, end_condition):
        tmp_n = Node(start_condition, ch, end_condition)
        self.NFA_list.append(tmp_n)

    # 添加一个机器的状态到list
    # @param start_condition 机器是开始状态
    # @param end_condition 机器的结束状态
    def add_to_condition_list(self, start_condition, end_condition):
        tmp_c = Condition(start_condition, end_condition)
        self.condition_list.append(tmp_c)

    # 检测运算符列表，拿出一个运算
    def check_oper(self):
        if len(self.oper_list) > 0:
            one_oper = self.oper_list[-1]
            opered = 0  # 标记是否使用的运算符, 使用过就删除
            if one_oper == "&" and len(self.condition_list) > 1:
                # 取出两太机器
                one = self.condition_list.pop(0)
                two = self.condition_list.pop(0)
                self.latest_list[0] = two.start_condition
                self.latest_list[1] = two.end_condition
                # 加入连接的边
                self.add_to_NFA(one.end_condition, "*", two.start_condition)
                # 添加连接好的机器
                self.add_to_condition_list(one.start_condition, two.end_condition)
                opered = 1
            elif one_oper == "(":
                self.oper_list.pop(-1)
                tmp_string = ""
                one_oper = self.get_one_char()
                while one_oper !=  ")":
                    tmp_string += one_oper
                    one_oper = self.get_one_char()

                # 保存副本，递归结束后恢复
                save_old_condition_list = self.condition_list[:1]
                save_old_oper = self.oper_list
                save_old_string = self.string  # 保存()后面没有处理的
                self.oper_list = []  # 清空运算符
                self.condition_list = []  #清空状态列表

                # 递归处理
                other_cond_list = self.to_NFA(tmp_string)

                # 恢复
                self.condition_list = save_old_condition_list
                self.condition_list.append(other_cond_list[0])
                self.string = save_old_string
                self.oper_list = save_old_oper
                self.check_oper()

            elif one_oper == "|":
                save_old_condition = self.condition_list.pop(0) # 保存| 前面的机器状态
                self.oper_list.pop(-1)
                other_cond_list = self.to_NFA(self.string)
                a = other_cond_list[0]
                b = save_old_condition
                # 添加4条边到NFA
                self.add_to_NFA(self.condition, "*", a.start_condition)
                self.add_to_NFA(self.condition, "*", b.start_condition)
                self.add_to_NFA(a.end_condition, "*", self.condition + 1)
                self.add_to_NFA(b.end_condition, "*", self.condition + 1)

                # 更新机器的开始结束状态
                tmp_c = Condition(self.condition, self.condition + 1)

                # 更新最新添加的机械状态
                self.latest_list[0] = self.condition
                self.latest_list[1] = self.condition + 1

                self.condition_list[0] = tmp_c
                self.condition += 2
            elif one_oper == "*":
                one = self.latest_list[0]
                two = self.latest_list[1]
                self.add_to_NFA(two, "*", one)
                opered = 1
            if opered == 1:
                self.oper_list.pop(0)

    # 返回正则表达式的第一个字符，并且删除第一个字符
    def get_one_char(self):
        ch = self.string[:1]
        self.string = self.string[1:]
        return ch

    # NFA转化
    # 入口函数
    def to_NFA(self, string):
        self.string = string
        self.pre_string()
        while len(self.string) > 0:
            one_char = self.get_one_char()
            if one_char >= "a" and one_char <= "z":
                self.add_to_NFA(self.condition, one_char, self.condition + 1)
                self.add_to_condition_list(self.condition, self.condition + 1)

                self.latest_list[0] = self.condition
                self.latest_list[1] = self.condition + 1

                self.condition += 2
            else:
                self.oper_list.append(one_char)
            self.check_oper()

        if len(self.oper_list) > 0:
            self.check_oper()
        return self.condition_list[:1]

# 保存整台机器的开始结束状态
NFA_condition = [1,1]

# 外部调用接口
def NFA(string):
    st = string
    a = Reg_To_NFA()
    a.to_NFA(st)
    a.print_NFA()
    global NFA_condition
    NFA_condition = a.return_NFA_condition()
    return a.NFA_list

def get_NFA_condition():
    return NFA_condition


def main():
    st =  "(a|b)*abb"
    a = Reg_To_NFA()
    a.to_NFA(st)
    a.print_NFA()


if __name__ == "__main__":
    main()