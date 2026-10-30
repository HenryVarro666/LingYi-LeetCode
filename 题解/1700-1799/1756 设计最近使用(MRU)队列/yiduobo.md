---
title: "1756. 设计最近使用(MRU)队列"
aliases: ["yiduobo的每日leetcode 1756.设计最近使用(MRU)队列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/620881717"
zhihu_id: "620881717"
zhihu_title: "yiduobo的每日leetcode 1756.设计最近使用(MRU)队列"
question_id: "1756"
question: "设计最近使用(MRU)队列"
problem_url: "https://leetcode.cn/problems/design-most-recently-used-queue/"
created: "2023-04-10T21:55:38+08:00"
updated: "2023-04-10T21:55:38+08:00"
upvotes: 1
comments: 0
---

# 1756. 设计最近使用(MRU)队列

> **[yiduobo的每日leetcode 1756.设计最近使用(MRU)队列](https://zhuanlan.zhihu.com/p/620881717) · 知乎 · 2023-04-10 · 赞同 1**
> 力扣：[1756. 设计最近使用(MRU)队列](https://leetcode.cn/problems/design-most-recently-used-queue/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1756.设计最近使用(MRU)队列

[力扣](https://leetcode.cn/problems/design-most-recently-used-queue/)

对于这类排队问题，如果每次将第k个元素移除之后都将后续的元素提上来补位，就必须使用链表相关的操作，否则时间复杂度就太高了。一种常见的处理方法是先在当前队列的末尾额外开辟若干个坑位，数量与询问的次数相同。接下来对于每次操作，将第k个元素移除之后并不移动后续的元素，而是将其重新插入在末尾对应的坑位中，从而达到改变顺序的目的。简单来说，就是对于这n个元素，第一次fetch操作将对应的数移动到队列的第n个位置，第二次fetch操作将对应的数移动到队列的第n + 1个位置，以此类推。

到了这里，问题就变成了动态的第k小元素。对于这个问题，王道做法自然是平衡树，不过本题的数据规模不大，使用线段树或者树状数组配合二分都是可行的，我在这里采用的是线段树。

最后附上python代码：

```python
class MRUQueue(object):

    def __init__(self, n):
        """
        :type n: int
        """
        self.f = [0] * 8192
        self.v = [0] * 4096
        self.order = n
        for v in range(n):
            self.insert(v, v)

    def insert(self, p, v):
        now = 0
        left = 0
        right = 4095
        while left < right:
            self.f[now] += 1
            mid = (left + right) >> 1
            if p <= mid:
                now = now + now + 1
                right = mid
            else:
                now = now + now + 2
                left = mid + 1
        
        self.f[now] = 1
        self.v[p] = v

    def fetch(self, k):
        """
        :type k: int
        :rtype: int
        """

        now = 0
        left = 0
        right = 4095
        while left < right:
            mid = (left + right) >> 1
            if k > self.f[now + now + 1]:
                k -= self.f[now + now + 1]
                self.f[now] -= 1
                now = now + now + 2
                left = mid + 1
            else:
                self.f[now] -= 1
                now = now + now + 1
                right = mid
        
        res = self.v[left]
        self.f[now] -= 1

        self.insert(self.order, res)
        self.order += 1
        return res + 1

# Your MRUQueue object will be instantiated and called as such:
# obj = MRUQueue(n)
# param_1 = obj.fetch(k)
```
