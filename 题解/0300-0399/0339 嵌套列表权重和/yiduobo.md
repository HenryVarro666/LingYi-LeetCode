---
title: "339. 嵌套列表权重和"
aliases: ["yiduobo的每日leetcode 339.嵌套列表权重和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/596646200"
zhihu_id: "596646200"
zhihu_title: "yiduobo的每日leetcode 339.嵌套列表权重和"
question_id: "339"
question: "嵌套列表权重和"
problem_url: "https://leetcode.cn/problems/nested-list-weight-sum/"
created: "2023-01-04T23:28:32+08:00"
updated: "2023-01-04T23:28:32+08:00"
upvotes: 0
comments: 0
---

# 339. 嵌套列表权重和

> **[yiduobo的每日leetcode 339.嵌套列表权重和](https://zhuanlan.zhihu.com/p/596646200) · 知乎 · 2023-01-04 · 赞同 0**
> 力扣：[339. 嵌套列表权重和](https://leetcode.cn/problems/nested-list-weight-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

339.嵌套列表权重和

[力扣](https://leetcode.cn/problems/nested-list-weight-sum/)

经典的递归问题。对于当前的列表，枚举其中的所有元素。对于当前元素part，若part是一个整数，那么就将其与当前深度相乘，然后将乘积累加到最终答案中。若part是一个list，那么就在深度加1的前提下递归求解part。

最后附上python代码：

```python
# """
# This is the interface that allows for creating nested lists.
# You should not implement it, or speculate about its implementation
# """
#class NestedInteger(object):
#    def __init__(self, value=None):
#        """
#        If value is not specified, initializes an empty list.
#        Otherwise initializes a single integer equal to value.
#        """
#
#    def isInteger(self):
#        """
#        @return True if this NestedInteger holds a single integer, rather than a nested list.
#        :rtype bool
#        """
#
#    def add(self, elem):
#        """
#        Set this NestedInteger to hold a nested list and adds a nested integer elem to it.
#        :rtype void
#        """
#
#    def setInteger(self, value):
#        """
#        Set this NestedInteger to hold a single integer equal to value.
#        :rtype void
#        """
#
#    def getInteger(self):
#        """
#        @return the single integer that this NestedInteger holds, if it holds a single integer
#        Return None if this NestedInteger holds a nested list
#        :rtype int
#        """
#
#    def getList(self):
#        """
#        @return the nested list that this NestedInteger holds, if it holds a nested list
#        Return None if this NestedInteger holds a single integer
#        :rtype List[NestedInteger]
#        """
class Solution(object):
    def depthSum(self, nestedList):
        """
        :type nestedList: List[NestedInteger]
        :rtype: int
        """

        global res
        res = 0

        def calc(now, depth):
            global res
            for part in now:
                if part.isInteger():
                    res += part.getInteger() * depth
                else:
                    calc(part.getList(), depth + 1)
        
        calc(nestedList, 1)
        return res
```
