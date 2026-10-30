---
title: "3484. 设计电子表格"
aliases: ["yiduobo的每日leetcode 3484.设计电子表格"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/design", "leetcode/hash-table", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1897406468321440446"
zhihu_id: "1897406468321440446"
zhihu_title: "yiduobo的每日leetcode 3484.设计电子表格"
question_id: "3484"
question: "设计电子表格"
problem_url: "https://leetcode.cn/problems/design-spreadsheet/"
difficulty: "Medium"
created: "2025-04-22T21:37:51+08:00"
updated: "2025-04-22T21:37:51+08:00"
upvotes: 1
comments: 0
---

# 3484. 设计电子表格

> **[yiduobo的每日leetcode 3484.设计电子表格](https://zhuanlan.zhihu.com/p/1897406468321440446) · 知乎 · 2025-04-22 · 赞同 1**
> 力扣：[3484. 设计电子表格](https://leetcode.cn/problems/design-spreadsheet/) · Medium · 灵茶山艾府：[哈希表模拟，简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3484.设计电子表格

[3484. 设计电子表格 - 力扣（LeetCode）](https://leetcode.cn/problems/design-spreadsheet/description/)

题目需要设计一个电子表格，这个表格由rows行以及'A'到'Z'一共26列，表格中的每个单元格可以储存一个0到10^5之间的整数。

现在要求实现一个电子表格类Spreadsheet，包含：

1、构造函数Spreadsheet(rows)：初始化一个具有rows行的电子表格，初始情况下所有单元格的值都为0

2、setCell(cell, value)：将指定单元格的值设置为value。其中cell的格式为列字符加上行号的形式给出，例如'A1', 'B10'。行号从1开始编号。

3、resetCell(cell)：将指定单元格的值重置为0。

4、getValue(formula)：需要计算一个公式的值，格式为\=X+Y，其中X和Y要么是单元格的引用，要么是非负整数值。

题目中的各个操作都比较直观，可以直接模拟。具体来说：

1、Spreadsheet(rows)：直接初始化一个值全为0的数组就行了

2、setCell(cell, value)：通过分离cell[0]以及cell[1:]得到列号以及行号，然后将数组中对应的位置值设置为value即可

3、resetCell(cell)：直接调用setCell(cell, 0)即可

4、getValue(formula)：先通过加号分离X和Y，然后对于X和Y分别检测。若首字符为数字，那么说明当前的部分就是一个数字，应该将其转化为数字累加到答案中；若首字符为字母，那么说明是一个单元格的引用，此时应该分离出首字符以及后续的字符作为列号以及行号，然后取数组中对应的位置上的元素值累加到答案中。

在具体实现上，我没有使用二维数组，而是将其压扁成一个rows \* 26的一维数组，然后通过row \* 26 + col来计算在二维数组中位于(row, col)的元素在这个一维数组中的下标。

最后附上python代码：

```python
class Spreadsheet(object):

    def __init__(self, rows):
        """
        :type rows: int
        """

        self.values = [0] * (rows * 26)

    def getIndex(self, cell):
        row = int(cell[1:]) - 1
        return row * 26 + ord(cell[0]) - 65

    def setCell(self, cell, value):
        """
        :type cell: str
        :type value: int
        :rtype: None
        """
        
        index = self.getIndex(cell)
        self.values[index] = value

    def resetCell(self, cell):
        """
        :type cell: str
        :rtype: None
        """
        
        self.setCell(cell, 0)

    def getValue(self, formula):
        """
        :type formula: str
        :rtype: int
        """
        
        exp_list = formula[1:].split('+')
        res = 0
        for exp in exp_list:
            if exp.isdigit():
                res += int(exp)
            else:
                res += self.values[self.getIndex(exp)]
        
        return res

# Your Spreadsheet object will be instantiated and called as such:
# obj = Spreadsheet(rows)
# obj.setCell(cell,value)
# obj.resetCell(cell)
# param_3 = obj.getValue(formula)
```
