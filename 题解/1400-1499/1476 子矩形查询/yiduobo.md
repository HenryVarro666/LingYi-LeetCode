---
title: "1476. 子矩形查询"
aliases: ["yiduobo的每日leetcode 1476.子矩形查询"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/415164634"
zhihu_id: "415164634"
zhihu_title: "yiduobo的每日leetcode 1476.子矩形查询"
question_id: "1476"
question: "子矩形查询"
problem_url: "https://leetcode.cn/problems/subrectangle-queries/"
created: "2021-09-28T23:15:54+08:00"
updated: "2021-09-28T23:15:54+08:00"
upvotes: 0
comments: 0
---

# 1476. 子矩形查询

> **[yiduobo的每日leetcode 1476.子矩形查询](https://zhuanlan.zhihu.com/p/415164634) · 知乎 · 2021-09-28 · 赞同 0**
> 力扣：[1476. 子矩形查询](https://leetcode.cn/problems/subrectangle-queries/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1476.子矩形查询

[力扣](https://leetcode-cn.com/problems/subrectangle-queries/)

对于查询操作(x, y)而言，其对应的值应该是最近一次被矩形更新后的值。在这里没有必要针对更新操作修改具体具体的矩形，而是只需要使用一个list记录下来更新的记录。对于一起询问，从list的末尾向前进行扫描，若当前询问的(x, y)是否处于更新矩形当中，那么答案就是这里更新的值。若(x, y)不处于任何更新矩形当中，那么答案就是初始值。

最后附上python代码：

```python
class SubrectangleQueries(object):

    def __init__(self, rectangle):
        """
        :type rectangle: List[List[int]]
        """
        self.origin = rectangle[:]
        self.update_his = []

    def updateSubrectangle(self, row1, col1, row2, col2, newValue):
        """
        :type row1: int
        :type col1: int
        :type row2: int
        :type col2: int
        :type newValue: int
        :rtype: None
        """
        self.update_his.append([row1, col1, row2, col2, newValue])

    def getValue(self, row, col):
        """
        :type row: int
        :type col: int
        :rtype: int
        """
        for index in range(len(self.update_his) - 1, -1, -1):
            row1, col1, row2, col2, value = self.update_his[index]
            if row1 <= row <= row2 and col1 <= col <= col2:
                return value
        
        return self.origin[row][col]

# Your SubrectangleQueries object will be instantiated and called as such:
# obj = SubrectangleQueries(rectangle)
# obj.updateSubrectangle(row1,col1,row2,col2,newValue)
# param_2 = obj.getValue(row,col)
```
