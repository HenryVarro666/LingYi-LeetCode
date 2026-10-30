---
title: "900. RLE迭代器"
aliases: ["yiduobo的每日leetcode 900.RLE迭代器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/353378727"
zhihu_id: "353378727"
zhihu_title: "yiduobo的每日leetcode 900.RLE迭代器"
question_id: "900"
question: "RLE迭代器"
problem_url: "https://leetcode.cn/problems/rle-iterator/"
created: "2021-02-27T17:49:07+08:00"
updated: "2021-02-27T17:49:07+08:00"
upvotes: 0
comments: 0
---

# 900. RLE迭代器

> **[yiduobo的每日leetcode 900.RLE迭代器](https://zhuanlan.zhihu.com/p/353378727) · 知乎 · 2021-02-27 · 赞同 0**
> 力扣：[900. RLE迭代器](https://leetcode.cn/problems/rle-iterator/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

900.RLE迭代器

[力扣](https://leetcode-cn.com/problems/rle-iterator/)

直接按照题目意思进行模拟即可。使用两个变量now和used_num分别表示当前处于A数组的哪个下标，以及当前下标对应的数已经使用了多少个，那么对于一个输入的n：

若当前的now小于len(A)，且used_num + n >\= A[now]，说明剩下的A[now + 1]的数量不够，因此需要将n减去A[now] - used_num，同时将user_num置0，now往后移动两位。重复此过程直到now等于len(A)或者used_num + n \< A[now]

当now等于len(A)时，说明此时数量已经不够了，返回-1。

否则表示剩下的A[now + 1]数量足够，因此需要将used_num应该加上n，表示对于当前的A[now + 1]而言又使用了n个，然后返回A[now + 1]即可。

最后附上python代码：

```python
class RLEIterator(object):

    def __init__(self, A):
        """
        :type A: List[int]
        """
        self.A = A[:]
        self.used_num = 0
        self.now = 0

    def next(self, n):
        """
        :type n: int
        :rtype: int
        """
        while self.now < len(self.A) and self.used_num + n > self.A[self.now]:
            n -= self.A[self.now] - self.used_num
            self.used_num = 0
            self.now += 2
        
        if self.now == len(self.A):
            return -1
        
        self.used_num += n
        return self.A[self.now + 1]

# Your RLEIterator object will be instantiated and called as such:
# obj = RLEIterator(A)
# param_1 = obj.next(n)
```
