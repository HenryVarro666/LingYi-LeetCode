---
title: "4062. 成对操作转化数组"
aliases: ["yiduobo的每日leetcode 4062.成对操作转化数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2088382958885512432"
zhihu_id: "2088382958885512432"
zhihu_title: "yiduobo的每日leetcode 4062.成对操作转化数组"
question_id: "4062"
question: "成对操作转化数组"
problem_url: "https://leetcode.cn/problems/transform-array-using-pair-operations/"
difficulty: "Medium"
created: "2026-09-29T21:51:10+08:00"
updated: "2026-09-29T21:51:10+08:00"
upvotes: 2
comments: 0
---

# 4062. 成对操作转化数组

> **[yiduobo的每日leetcode 4062.成对操作转化数组](https://zhuanlan.zhihu.com/p/2088382958885512432) · 知乎 · 2026-09-29 · 赞同 2**
> 力扣：[4062. 成对操作转化数组](https://leetcode.cn/problems/transform-array-using-pair-operations/) · Medium · 灵茶山艾府：[不变量（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4062.成对操作转化数组

<https://leetcode.cn/problems/transform-array-using-pair-operations/description/>

题目给出两个整数数组source和target。

在一次操作中，可以选择source中两个不同的下标i和j，以及任意整数delta，将source[i]变为source[i] + source[j] - delta，同时将source[j]变为delta。

现在可以执行任意次操作，问能否使得source变为target。

首先，由于delta可以任意选择，因此每次操作可以在无视其中一个元素的前提下，使得另一个元素变为想要的目标元素。另一方面，注意到原始的source[i]与source[j]之和，与分配后的source[i] + source[j] - delta与delta之和相同，因此无论执行多少次操作，都不会影响source中元素之和。

更进一步的，不妨设当前完成了n - 1个元素的分配，那么最后剩下的这个元素必然等于source中元素之和减去target中对应的这n - 1个元素之和。若最后剩下的这个元素与target中对应的元素相同，那么就意味着source与target之和恰好相同。

因此只需检测两个数组之和是否相同，就能判断能否使得source变为target了。

最后附上python代码：

```python
class Solution(object):
    def canTransform(self, source, target):
        """
        :type source: List[int]
        :type target: List[int]
        :rtype: bool
        """
        
        return sum(source) == sum(target)
```
