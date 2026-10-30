---
title: "251. 展开二维向量"
aliases: ["yiduobo的每日leetcode 251.展开二维向量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/592627350"
zhihu_id: "592627350"
zhihu_title: "yiduobo的每日leetcode 251.展开二维向量"
question_id: "251"
question: "展开二维向量"
problem_url: "https://leetcode.cn/problems/flatten-2d-vector/"
created: "2022-12-18T03:33:12+08:00"
updated: "2022-12-18T03:33:12+08:00"
upvotes: 0
comments: 0
---

# 251. 展开二维向量

> **[yiduobo的每日leetcode 251.展开二维向量](https://zhuanlan.zhihu.com/p/592627350) · 知乎 · 2022-12-18 · 赞同 0**
> 力扣：[251. 展开二维向量](https://leetcode.cn/problems/flatten-2d-vector/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

251.展开二维向量

[力扣](https://leetcode.cn/problems/flatten-2d-vector/)

可以按照题目所说的，在初始化的时候就将这个二维数组展开成一维数组，然后使用一个变量记录当前访问的数字，或者不进行展开，而是使用两个变量vec_p和iter_p分别记录当前访问到哪个子数组的第几个元素，然后逐渐向后移动。

我在这里采用的是第二种做法。具体实现也比较简单，不过需要注意的是，题目中可能存在空的子数组，因此在向后移动vec_p和iter_p时需要注意跳过这些空的子数组。

最后附上python代码：

```python
class Vector2D(object):

    def __init__(self, vec):
        """
        :type vec: List[List[int]]
        """
        self.vec = vec[:]
        self.vec_p = 0
        self.iter_p = 0
        while self.vec_p < len(self.vec) and self.iter_p == len(self.vec[self.vec_p]):
            self.vec_p += 1

    def next(self):
        """
        :rtype: int
        """
        res = self.vec[self.vec_p][self.iter_p]
        self.iter_p += 1
        while self.vec_p < len(self.vec) and self.iter_p == len(self.vec[self.vec_p]):
            self.iter_p = 0
            self.vec_p += 1
        return res

    def hasNext(self):
        """
        :rtype: bool
        """
        return self.vec_p != len(self.vec)

# Your Vector2D object will be instantiated and called as such:
# obj = Vector2D(vec)
# param_1 = obj.next()
# param_2 = obj.hasNext()
```
