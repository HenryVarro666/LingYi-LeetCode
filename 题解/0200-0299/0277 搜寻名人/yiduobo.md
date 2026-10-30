---
title: "277. 搜寻名人"
aliases: ["yiduobo的每日leetcode 277.搜寻名人"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/594295875"
zhihu_id: "594295875"
zhihu_title: "yiduobo的每日leetcode 277.搜寻名人"
question_id: "277"
question: "搜寻名人"
problem_url: "https://leetcode.cn/problems/find-the-celebrity/"
created: "2022-12-26T01:33:19+08:00"
updated: "2022-12-26T01:33:19+08:00"
upvotes: 0
comments: 0
---

# 277. 搜寻名人

> **[yiduobo的每日leetcode 277.搜寻名人](https://zhuanlan.zhihu.com/p/594295875) · 知乎 · 2022-12-26 · 赞同 0**
> 力扣：[277. 搜寻名人](https://leetcode.cn/problems/find-the-celebrity/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

277.搜寻名人

[力扣](https://leetcode.cn/problems/find-the-celebrity/)

题目给出一张有向图图，问图中是否存在入度为n - 1，出度为0的节点。直接遍历每一条边并统计入度和出度是可行的做法，但是时间复杂度为O(V + E)，高出了题目的要求。只能从knows操作入手看看有没有什么启发。

对于一组(x, y)，如果knows(x, y)为true，那么说明x不可能是名人，y未知。反过来，若knows(x, y)为false，那么说明y不可能是名人，x未知。

一般来说，我们检测的都是y是不是被x知道，重点都放在了y上，而忽略了knows(x, y)为true时，x不可能为名人这个讯息。更具体的，设最终答案为candidate，初始化为0，然后枚举candidate + 1到n - 1之间的每个p，检测knows(p, candidate)。若某一时刻knows(p, candidate)为false，那么说明candidate不是要找的答案，此时需要另找一个candidate。此时的隐藏条件就是，knows(candidate + 1, candidate)到knows(p - 1, candidate)全都为true，否则不会执行到knows(p, candidate)。更进一步的，就说明candidate + 1到p - 1这些人都不会是名人，因此下一个名人的候选者应该就是p，因此需要将candidate更新为p，然后重复上面的过程，从新的candidate + 1到n - 1逐个检测knows。

由于每次检测的起点都是当前candidate + 1，因此这一步总共会执行n次，同时将得到一个最终的candidate。接下来，遍历除candidate为的所有人，检测是否所有人都知道candidate，且candidate不知道任何人就行了，对knows的调用次数恰好是3n次。

最后附上python代码：

```python
# The knows API is already defined for you.
# @param a, person a
# @param b, person b
# @return a boolean, whether a knows b
# def knows(a, b):

class Solution(object):
    def findCelebrity(self, n):
        """
        :type n: int
        :rtype: int
        """

        candidate = 0
        flag = False

        while not flag:
            flag = True
            for p in range(candidate + 1, n):
                if knows(candidate, p):
                    candidate = p
                    flag = False
                    break
        
        for p in range(n):
            if p != candidate and (knows(candidate, p) or not knows(p, candidate)):
                return -1
        
        return candidate
```
