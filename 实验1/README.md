                                       实验一：预编译系统的实现----打造具有个人风格的C++语言（词法分析）


# 实验内容及要求：

## 功能：实现具有个人风格C++源代码的预编译系统，即扫描程序把具有个人风格的单词重新改写为传统C++单词。
   改写的单词至少应该有：
原C++语言的单词   具有个人风格的C++语言的单词 
    int                 integer
    float               real 
    cin                 read
    cout                write
    ==                   =
    =                   :=
    !=                  <>
    {                   begin
    }                   end
    /*   */             (*    *)   

## 打开一个具有个人风格的C++源文件，把具有个人风格的单词重新改写为传统C++的单词，并存盘。(预编译)
## 对改写好的C++程序进行编译并执行。
## 要求应用程序应为Windows界面。
## 应该书写完善的软件文档。

# 完成时间：4周

# 上交方法：
    由各班班长或学习委员将每个同学的实验源程序、测试文件、可执行程序、文档刻录成光盘。

# 完成方式：每个学生自行独立完成。


# 运行效果样本

具有个人风格的C++源程序：

Test-in.cpp
```c++
#include<iostream.h>
(* This is a test file *)
main()
begin
   integer i;
   read>>i;
   i:=i+1
   if (i<>3) write<<“ok”;
end
```



改写后的C++源程序：
Test-out.cpp
```C++
#include<iostream.h>
/* This is a test file */
main()
{
   int i;
   cin>>i;
   i=i+1; 
   if (i!=3) cout<<“ok”;
}
```







