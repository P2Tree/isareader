# ISAReader

## Chinese version
这是一个能够简单的提取硬件给你的糟心 ISA 表格的小工具。它可以交互式的解析表格中的某一行或多行指令编码的十六进制格式，从而可以方便的将它们粘贴到你的测试用例中。

Python 水平有限，如果有人想重构请随意，但麻烦通知我去试用你的设计。

输入文件：

- 一个糟心的 ISA 表格。
- 一个配置文件。

使用：

1. 首先要用 python3 跑起来。
2. 输入一个号，选择 sheet。
3. 输入一个行号，比如 10，选择某条指令。
4. 或者输入两个行号，比如 10 20，选择这个区间内所有指令。

通过 `python isareader.py -h`，可以查看参数说明。

有问题请沟通。


## 英文版说明

A simple program to parse the ISA excel file and output encoding information interativly.

So you can get hexadecimal format encoding information with the instruction.

Input file:

- A ISA excel file.
- Configuration file.

Usage:

1. Use python3 to boot it.
2. Select a sheet in your excel file.
3. Input a line number ("10" .etc) to select instruction.
4. Or you can input two line number (begin one and end one, "10 20" .etc) to select range of instructions.

Try `python isareader.py -h` to see more arguments.

More knowledge you can connect with me in github.
