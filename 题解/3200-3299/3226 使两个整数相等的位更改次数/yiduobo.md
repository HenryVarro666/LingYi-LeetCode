---
title: "3226. 使两个整数相等的位更改次数"
aliases: ["yiduobo的每日leetcode 3226.使两个整数相等的位更改次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/719861047"
zhihu_id: "719861047"
zhihu_title: "yiduobo的每日leetcode 3226.使两个整数相等的位更改次数"
question_id: "3226"
question: "使两个整数相等的位更改次数"
problem_url: "https://leetcode.cn/problems/number-of-bit-changes-to-make-two-integers-equal/"
difficulty: "Easy"
rating: 1247
created: "2024-09-13T02:50:10+08:00"
updated: "2024-09-13T02:50:10+08:00"
upvotes: 2
comments: 0
---

# 3226. 使两个整数相等的位更改次数

> **[yiduobo的每日leetcode 3226.使两个整数相等的位更改次数](https://zhuanlan.zhihu.com/p/719861047) · 知乎 · 2024-09-13 · 赞同 2**
> 力扣：[3226. 使两个整数相等的位更改次数](https://leetcode.cn/problems/number-of-bit-changes-to-make-two-integers-equal/) · Easy · 灵茶山艾府：[O(1) 位运算做法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3226.使两个整数相等的位更改次数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-bit-changes-to-make-two-integers-equal/description/)

题目给出两个正整数n和k，每一轮都可以选择n的某一个二进制位，将这一位上的1变为0，问需要多少次操作才能将n变为k。如果无法将n变为k，则返回-1。

首先，若k的二进制表示中某一位为1，且n在这一位上为0，那么无论怎么操作都无法使得n这一位变为1，这种情况下答案就是-1。从位运算的角度来说，就是n & k !\= k。

接下来对于n&k \= k的情况，则只需将n中多余的1都变为0即可，也就是计算m \= n^k的二进制表示中1的数量。对于这个问题只需逐个分离m的二进制位然后进行计算即可。

最后附上python代码：

```python
class Solution(object):
    def minChanges(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """

        if (n & k) != k:
            return -1
        
        m = n ^ k
        res = 0
        while m:
            res += 1
            m &= m - 1
        
        return res
```
