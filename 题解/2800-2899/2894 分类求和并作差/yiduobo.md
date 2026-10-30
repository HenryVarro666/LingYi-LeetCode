---
title: "2894. 分类求和并作差"
aliases: ["yiduobo的每日leetcode 2894.分类求和并作差"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/662965906"
zhihu_id: "662965906"
zhihu_title: "yiduobo的每日leetcode 2894.分类求和并作差"
question_id: "2894"
question: "分类求和并作差"
problem_url: "https://leetcode.cn/problems/divisible-and-non-divisible-sums-difference/"
difficulty: "Easy"
created: "2023-10-23T23:17:27+08:00"
updated: "2023-10-23T23:17:27+08:00"
upvotes: 0
comments: 0
---

# 2894. 分类求和并作差

> **[yiduobo的每日leetcode 2894.分类求和并作差](https://zhuanlan.zhihu.com/p/662965906) · 知乎 · 2023-10-23 · 赞同 0**
> 力扣：[2894. 分类求和并作差](https://leetcode.cn/problems/divisible-and-non-divisible-sums-difference/) · Easy · 灵茶山艾府：[O(1) 数学公式（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2894.分类求和并作差

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/divisible-and-non-divisible-sums-difference/)

按照题目要求一趟遍历，就其中m的倍数从答案中减去，同时将其他数累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def differenceOfSums(self, n, m):
        """
        :type n: int
        :type m: int
        :rtype: int
        """

        res = 0
        for v in range(1, n + 1):
            if v % m == 0:
                res -= v
            else:
                res += v
        
        return res
```
