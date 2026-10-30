---
title: "364. 加权嵌套序列和II"
aliases: ["yiduobo的每日leetcode 364.加权嵌套序列和II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/598116238"
zhihu_id: "598116238"
zhihu_title: "yiduobo的每日leetcode 364.加权嵌套序列和II"
question_id: "364"
question: "加权嵌套序列和II"
problem_url: "https://leetcode.cn/problems/nested-list-weight-sum-ii/"
created: "2023-01-10T23:05:57+08:00"
updated: "2023-01-10T23:05:57+08:00"
upvotes: 0
comments: 0
---

# 364. 加权嵌套序列和II

> **[yiduobo的每日leetcode 364.加权嵌套序列和II](https://zhuanlan.zhihu.com/p/598116238) · 知乎 · 2023-01-10 · 赞同 0**
> 力扣：[364. 加权嵌套序列和II](https://leetcode.cn/problems/nested-list-weight-sum-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

364.加权嵌套序列和II

[力扣](https://leetcode.cn/problems/nested-list-weight-sum-ii/)

之前339题的变种版本。

[yiduobo：yiduobo的每日leetcode 339.嵌套列表权重和](https://zhuanlan.zhihu.com/p/596646200)

与之前的区别是计算深度的方法刚好相反，那么可以利用逆向思维，按照之前的计算方法计算原始版本的权重和，同时在这个过程中计算总深度以及不加权的数值总和，然后使用这二者的乘积减去原始版本的权重和，就得到了本题要求的权重和了。

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
    def depthSumInverse(self, nestedList):
        """
        :type nestedList: List[NestedInteger]
        :rtype: int
        """

        global max_depth, s
        max_depth = s = 0

        def calc(now, depth):
            if not now:
                return 0

            global max_depth, s
            max_depth = max(max_depth, depth)

            cnt = 0
            for part in now:
                if part.isInteger():
                    num = part.getInteger()
                    s += num
                    cnt += num * depth
                else:
                    cnt += calc(part.getList(), depth + 1)
            
            return cnt
        
        res = calc(nestedList, 1)
        return s * (max_depth + 1) - res
```
