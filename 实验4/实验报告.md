#<center>实验四：LL(1)分析器的生成 实验报告</center>
<center>20152100121林伟业</center>

## 用法
python main.py -f "test.txt"

## first集合求法
1. 直接收取：对形如U－>a…的产生式(其中a是终结符)，把a收入到First(U)中 
2. 反复传送：对形入U－>P…的产生式(其中P是非终结符)，应把First(P)中的全部内容传送到First(U)中，当First(P)包含 $\epsilon$ 需要再往后考虑一个字符

## follow集合求法
1. 将\$放到follow(S)中，其中S是开始符号，而\$是输入右端的结束标记
2. A $\to$ aBC，那么first(C)中没有 $\epsilon$ ,first(C)的所有符号都在follow(B)中。
3. A $\to$ aB，或者A $\to$ aBC，first(C)有$\epsilon$，follow(A)的所有符号都在follow(B)中。

## 用户输入文法的文法规则
G[A]:
A->U "->" C
U->[A-Z]
C->D{"|"D}
D->{a-zA-Z}

## 自顶向下分析方法

非终结符号作函数调用，终结符号作字符串的匹配
```
def A(self, ch)
def U(self, ch)
def C(self, ch)
def D(self, ch)
```

## LL(1)分析表的构造步骤

为每个非终结符号A和产生式A->a重复以下两个步骤：
1. 对于First(A)中的每个记号a，都将A->a添加到项目M[A,a]中
2. A->BCD，若$\epsilon$在First(B)中，则对于Follow(B)的每个元素a或者$，都将A->a添加到M[A,a]中。

## 程序

程序没有测试，first集合和follow集合求出来了，差不多了。