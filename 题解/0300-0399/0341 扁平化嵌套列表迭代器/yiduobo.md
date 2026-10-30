---
title: "341. 扁平化嵌套列表迭代器"
aliases: ["yiduobo的每日leetcode 341.扁平化嵌套列表迭代器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/163010000"
zhihu_id: "163010000"
zhihu_title: "yiduobo的每日leetcode 341.扁平化嵌套列表迭代器"
question_id: "341"
question: "扁平化嵌套列表迭代器"
problem_url: "https://leetcode.cn/problems/flatten-nested-list-iterator/"
created: "2020-07-22T21:55:15+08:00"
updated: "2020-07-22T21:55:15+08:00"
upvotes: 0
comments: 0
---

# 341. 扁平化嵌套列表迭代器

> **[yiduobo的每日leetcode 341.扁平化嵌套列表迭代器](https://zhuanlan.zhihu.com/p/163010000) · 知乎 · 2020-07-22 · 赞同 0**
> 力扣：[341. 扁平化嵌套列表迭代器](https://leetcode.cn/problems/flatten-nested-list-iterator/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

341.扁平化嵌套列表迭代器<https://leetcode-cn.com/problems/flatten-nested-list-iterator/>

我的做法是在初始化时将嵌套的list抽出来整理成标准的list，不过总感觉不够优美。

具体来说就是对于list中每个元素，如果其为整数，那么将其加入到标准list的尾部，否则递归处理该元素，然后将递归的结果extend到list尾部。

最后附上python代码：

```python
# """
# This is the interface that allows for creating nested lists.
# You should not implement it, or speculate about its implementation
# """
#class NestedInteger(object):
#    def isInteger(self):
#        """
#        @return True if this NestedInteger holds a single integer, rather than a nested list.
#        :rtype bool
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

class NestedIterator(object):

    def __init__(self, nestedList):
        """
        Initialize your data structure here.
        :type nestedList: List[NestedInteger]
        """
        self.num_list = self.split_list(nestedList)
        self.pos = 0

    def split_list(self, target_list):
        res = []
        for part in target_list:
            if part.isInteger():
                res.append(part.getInteger())
            else:
                res.extend(self.split_list(part.getList()))

        return res

    def next(self):
        """
        :rtype: int
        """
        self.pos += 1
        return self.num_list[self.pos - 1]

    def hasNext(self):
        """
        :rtype: bool
        """
        return self.pos < len(self.num_list)

# Your NestedIterator object will be instantiated and called as such:
# i, v = NestedIterator(nestedList), []
# while i.hasNext(): v.append(i.next())
```
