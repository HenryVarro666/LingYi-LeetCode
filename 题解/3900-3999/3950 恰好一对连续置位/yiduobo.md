---
title: "3950. 恰好一对连续置位"
aliases: ["yiduobo的每日leetcode 3950.恰好一对连续置位"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2047108290828558636"
zhihu_id: "2047108290828558636"
zhihu_title: "yiduobo的每日leetcode 3950.恰好一对连续置位"
question_id: "3950"
question: "恰好一对连续置位"
problem_url: "https://leetcode.cn/problems/exactly-one-consecutive-set-bits-pair/"
difficulty: "Easy"
created: "2026-06-08T00:14:43+08:00"
updated: "2026-06-08T00:15:00+08:00"
upvotes: 1
comments: 0
---

# 3950. 恰好一对连续置位

> **[yiduobo的每日leetcode 3950.恰好一对连续置位](https://zhuanlan.zhihu.com/p/2047108290828558636) · 知乎 · 2026-06-08 · 赞同 1**
> 力扣：[3950. 恰好一对连续置位](https://leetcode.cn/problems/exactly-one-consecutive-set-bits-pair/) · Easy · 灵茶山艾府：[O(1) 时间做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3950.恰好一对连续置位

<https://leetcode.cn/problems/exactly-one-consecutive-set-bits-pair/description/>

题目给出一个整数n。

若n的二进制表示中，恰好仅包含一对连续的置位，即二进制表示中，两个连续的1恰好仅出现一次，那么就返回true，否则返回false。

直接通过模2除以2的方法将n转换为二进制，同时使用一个变量pre记录上一位的值，另外使用一个变量cnt记录连续1出现的次数。

对于当前位，若值为1，且pre为1，那么就将cnt加上1。无论当前位是多少，都需要更新pre。

转换完成后，判断cnt是否恰好等于1即可。

最后附上python代码：

```python
class Solution(object):
    def consecutiveSetBits(self, n):
        """
        :type n: int
        :rtype: bool
        """
        
        pre = 0
        cnt = 0
        while n:
            if n % 2 == 1 and pre == 1:
                cnt += 1
            pre = n % 2
            n //= 2
        
        return cnt == 1
```
