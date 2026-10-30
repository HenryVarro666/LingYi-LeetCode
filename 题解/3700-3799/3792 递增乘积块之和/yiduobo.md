---
title: "3792. 递增乘积块之和"
aliases: ["yiduobo的每日leetcode 3792.递增乘积块之和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bao-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1991710204333675408"
zhihu_id: "1991710204333675408"
zhihu_title: "yiduobo的每日leetcode 3792.递增乘积块之和"
question_id: "3792"
question: "递增乘积块之和"
problem_url: "https://leetcode.cn/problems/sum-of-increasing-product-blocks/"
difficulty: "Medium"
created: "2026-01-06T03:22:58+08:00"
updated: "2026-01-06T03:23:02+08:00"
upvotes: 0
comments: 0
---

# 3792. 递增乘积块之和

> **[yiduobo的每日leetcode 3792.递增乘积块之和](https://zhuanlan.zhihu.com/p/1991710204333675408) · 知乎 · 2026-01-06 · 赞同 0**
> 力扣：[3792. 递增乘积块之和](https://leetcode.cn/problems/sum-of-increasing-product-blocks/) · Medium · 灵茶山艾府：[O(n^2) 暴力](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3792.递增乘积块之和

[3792. 递增乘积块之和 - 力扣（LeetCode）](https://leetcode.cn/problems/sum-of-increasing-product-blocks/description/)

题目给出一个整数n，n的大小不超过1000。

另外存在以下数列

- 第一项的值为1
- 第二项的值为2 \* 3
- 第三项的值为4 \* 5 \* 6
- 以此类推，第index块是之后的index个连续整数的乘积

现在要求计算数列中前n项之和，对10^9 + 7取模后的结果是多少。

根据题目的描述，计算数列中第index项的时间复杂度是O(index)的。由于n的规模不大，因此在这里万千可以直接一趟遍历，计算出数列中的前n项对10^9 + 7取模的结果，然后将这些结果累加起来再取模，即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def sumOfBlocks(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        start = 1
        mod = 10 ** 9 + 7
        res = 0
        for index in range(1, n + 1):
            v = 1
            for x in range(start, start + index):
                v = v * x % mod
            res = (res + v) % mod
            start += index
        
        return res
```
