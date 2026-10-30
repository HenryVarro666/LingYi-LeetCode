---
title: "631. 设计Excel求和公式"
aliases: ["yiduobo的每日leetcode 631.设计Excel求和公式"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/602417910"
zhihu_id: "602417910"
zhihu_title: "yiduobo的每日leetcode 631.设计Excel求和公式"
question_id: "631"
question: "设计Excel求和公式"
problem_url: "https://leetcode.cn/problems/design-excel-sum-formula/"
created: "2023-02-01T02:23:58+08:00"
updated: "2023-02-01T02:23:58+08:00"
upvotes: 0
comments: 0
---

# 631. 设计Excel求和公式

> **[yiduobo的每日leetcode 631.设计Excel求和公式](https://zhuanlan.zhihu.com/p/602417910) · 知乎 · 2023-02-01 · 赞同 0**
> 力扣：[631. 设计Excel求和公式](https://leetcode.cn/problems/design-excel-sum-formula/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

631.设计Excel求和公式

[力扣](https://leetcode.cn/problems/design-excel-sum-formula/)

题目涉及到按照拓扑序更新单元格，以及动态二维区间求和这两种问题。

对于后者，可以使用二维树状数组来处理，不过更新的顺序必须严格按照拓扑序来做。在极限情况下，可以构造出一张m \* n个点，(m \* n)^2条边的图，而拓扑排序的复杂度为点的数量加上边的数量。也就是说，在最坏情况下这个时间复杂度与暴力枚举单元格，配合上记忆化搜索的算法其实是一致的，因此在这里没有必要使用上面这两种方法，直接对于每次求值操作，都枚举所有单元格并执行记忆化搜索就行了。

理论上的时间复杂度为O(K \* (mn)^2)，其中K为总的操作次数。不过由于在这里必须先通过set操作为单元格赋值，然后通过sum给单元格一个复杂的求解关系，才能使得最终有一个较高的求解复杂度，因此在总共只有100次操作的情况下并不需要担心时间复杂度的问题。

最后附上python代码：

```python
class Excel(object):

    def __init__(self, height, width):
        """
        :type height: int
        :type width: str
        """
        self.m = height
        self.n = ord(width) - 64
        self.mat = [[["0"] for j in range(self.n + 1)] for i in range(self.m + 1)]
        self.v = [[None] * (self.n + 1) for _ in range(self.m + 1)]

    def set(self, row, column, val):
        """
        :type row: int
        :type column: str
        :type val: int
        :rtype: None
        """
        x = row
        y = ord(column) - 64
        self.mat[x][y] = [str(val)]

    def calc(self, x, y):
        if self.v[x][y] is None:
            if self.mat[x][y][0][0] == '-' or '0' <= self.mat[x][y][0][0] <= '9':
                self.v[x][y] = int(self.mat[x][y][0])
            else:
                s = 0
                for part in self.mat[x][y]:
                    p = part.find(':')
                    if p == -1:
                        next_y = ord(part[0]) - 64
                        next_x = int(part[1:])
                        s += self.calc(next_x, next_y)
                    else:
                        
                        y1 = ord(part[0]) - 64
                        x1 = int(part[1: p])
                        y2 = ord(part[p + 1]) - 64
                        x2 = int(part[p + 2:])
                        for i in range(x1, x2 + 1):
                            for j in range(y1, y2 + 1):
                                s += self.calc(i, j)
                self.v[x][y] = s
        
        return self.v[x][y]

    def get(self, row, column):
        """
        :type row: int
        :type column: str
        :rtype: int
        """
        x = row
        y = ord(column) - 64
        self.v = [[None] * (self.n + 1) for _ in range(self.m + 1)]
        return self.calc(x, y)

    def sum(self, row, column, numbers):
        """
        :type row: int
        :type column: str
        :type numbers: List[str]
        :rtype: int
        """
        x = row
        y = ord(column) - 64
        self.mat[x][y] = numbers[:]
        self.v = [[None] * (self.n + 1) for _ in range(self.m + 1)]
        return self.calc(x, y)

# Your Excel object will be instantiated and called as such:
# obj = Excel(height, width)
# obj.set(row,column,val)
# param_2 = obj.get(row,column)
# param_3 = obj.sum(row,column,numbers)
```
