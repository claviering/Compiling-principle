# coding=utf-8

import DFA, sys, getopt

class lex_analyzer:
    def __init__(self, string, pro):
        self.string = string
        self.program_file = pro
        self.DFA_list = DFA.DFA(string)
        self.open_file()
        print self.DFA_list

    def open_file(self):
        try:
            file_open = open(self.program_file, "r")
        except:
            print ("open file error")
        else:
            sr = file_open.read()


def main(argv):
    st = ""
    pro = ""
    try:
        opts, args = getopt.getopt(argv, "hs:p:", ["st=", "program="])
    except getopt.GetoptError:
        print ("DFA.py -s \"string\" -p program file")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print ("DFA.py -s \"string\" -p program file")
            sys.exit()
        elif opt in ("-s", "--st"):
            st = arg
        elif opt in ("-p", "--program"):
            pro = arg
    if st == "" or pro == "":
        print ("lex_analyzer.py -s \"string\" -p program file")
        sys.exit(2)
    a = lex_analyzer(st, pro)

if __name__ == "__main__":
    main(sys.argv[1:])