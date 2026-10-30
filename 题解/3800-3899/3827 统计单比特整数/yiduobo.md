---
title: "3827. 统计单比特整数"
aliases: ["yiduobo的每日leetcode 3827.统计单比特整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/math", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2002147806933186039"
zhihu_id: "2002147806933186039"
zhihu_title: "yiduobo的每日leetcode 3827.统计单比特整数"
question_id: "3827"
question: "统计单比特整数"
problem_url: "https://leetcode.cn/problems/count-monobit-integers/"
difficulty: "Easy"
created: "2026-02-03T22:52:50+08:00"
updated: "2026-02-03T22:52:51+08:00"
upvotes: 1
comments: 0
---

# 3827. 统计单比特整数

> **[yiduobo的每日leetcode 3827.统计单比特整数](https://zhuanlan.zhihu.com/p/2002147806933186039) · 知乎 · 2026-02-03 · 赞同 1**
> 力扣：[3827. 统计单比特整数](https://leetcode.cn/problems/count-monobit-integers/) · Easy · 灵茶山艾府：[O(1) 一行代码（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3827.统计单比特整数

<https://leetcode.cn/problems/count-monobit-integers/description/>

题目给出一个整数n。

若一个整数的二进制表示中所有的位都相同，则称其为单比特数。

问0到n之间有多少个单比特数。

单比特数的二进制表示要么全0，要么全1。

对于全0的情况，只有0这唯一一个数满足条件。

而对于全1的情况，则可以是1、11、111这些恰好等于2^k - 1的数。

对于v \= 2^k - 1，只需将其乘以2再加上1，就可以变为2^(k + 1) - 1。于是可以从1开始向上迭代，每次将当前元素乘以2再加上1，直到大于n为止，迭代的轮次就是在0到n之间的全1单比特整数的数目，再加上1即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def countMonobit(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        res = 1
        v = 1
        while v <= n:
            res += 1
            v = v + v + 1
        
        return res
```
