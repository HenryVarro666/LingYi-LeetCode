---
title: "3370. 仅含置位位的最小整数"
aliases: ["yiduobo的每日leetcode 3370.仅含置位位的最小整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/28244041201"
zhihu_id: "28244041201"
zhihu_title: "yiduobo的每日leetcode 3370.仅含置位位的最小整数"
question_id: "3370"
question: "仅含置位位的最小整数"
problem_url: "https://leetcode.cn/problems/smallest-number-with-all-set-bits/"
difficulty: "Easy"
rating: 1199
created: "2025-03-05T23:51:44+08:00"
updated: "2025-03-05T23:51:44+08:00"
upvotes: 1
comments: 0
---

# 3370. 仅含置位位的最小整数

> **[yiduobo的每日leetcode 3370.仅含置位位的最小整数](https://zhuanlan.zhihu.com/p/28244041201) · 知乎 · 2025-03-05 · 赞同 1**
> 力扣：[3370. 仅含置位位的最小整数](https://leetcode.cn/problems/smallest-number-with-all-set-bits/) · Easy · 灵茶山艾府：[O(1) 做法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3370.仅含置位位的最小整数

[3370. 仅含置位位的最小整数 - 力扣（LeetCode）](https://leetcode.cn/problems/smallest-number-with-all-set-bits/description/)

题目给出一个整数n，要求找出大于等于n的，且二进制位全都是1的最小整数x。

对于某个符合题目要求的整数x，不妨设其二进制表示为k个1，那么下一个符合题目要求的整数的二进制表示就是k + 1个1，相当于将x左移一位，再加上1，换成十进制就是将x乘以2再加上1。换言之，题目中满足条件的元素增长速度是指数级的，因此在这里就可以从res \= 1开始暴力向上枚举答案，每一轮都将res更新为res \* 2 + 1，直到res大于等于n为止。

最后附上python代码：

```python
class Solution(object):
    def smallestNumber(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        res = 1
        while res < n:
            res = res * 2 + 1
        return res
```
