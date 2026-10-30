---
title: "281. 锯齿迭代器"
aliases: ["yiduobo的每日leetcode 281.锯齿迭代器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/594535824"
zhihu_id: "594535824"
zhihu_title: "yiduobo的每日leetcode 281.锯齿迭代器"
question_id: "281"
question: "锯齿迭代器"
problem_url: "https://leetcode.cn/problems/zigzag-iterator/"
created: "2022-12-26T22:54:59+08:00"
updated: "2022-12-26T22:54:59+08:00"
upvotes: 0
comments: 0
---

# 281. 锯齿迭代器

> **[yiduobo的每日leetcode 281.锯齿迭代器](https://zhuanlan.zhihu.com/p/594535824) · 知乎 · 2022-12-26 · 赞同 0**
> 力扣：[281. 锯齿迭代器](https://leetcode.cn/problems/zigzag-iterator/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

281.锯齿迭代器

[力扣](https://leetcode.cn/problems/zigzag-iterator/)

使用两个变量分别记录当前的v1和v2迭代的进度，同时再使用一个变量flag表示下一次迭代应该在v1中进行还是在v2中进行。

接下来对于每次迭代，先通过flag以及当前v1和v2迭代的进度来确定本轮迭代应该在哪边进行，然后执行相应的迭代操作即可。

最后附上python代码：

```python
class ZigzagIterator(object):

    def __init__(self, v1, v2):
        """
        Initialize your data structure here.
        :type v1: List[int]
        :type v2: List[int]
        """
        self.v1 = v1[:]
        self.v2 = v2[:]
        self.p1 = self.p2 = 0
        self.flag = True

    def next(self):
        """
        :rtype: int
        """
        if (self.flag or self.p2 == len(self.v2)) and self.p1 < len(self.v1):
            res = self.v1[self.p1]
            self.p1 += 1
        else:
            res = self.v2[self.p2]
            self.p2 += 1
        
        self.flag = not self.flag
        return res

    def hasNext(self):
        """
        :rtype: bool
        """
        return self.p1 < len(self.v1) or self.p2 < len(self.v2)

# Your ZigzagIterator object will be instantiated and called as such:
# i, v = ZigzagIterator(v1, v2), []
# while i.hasNext(): v.append(i.next())
```
