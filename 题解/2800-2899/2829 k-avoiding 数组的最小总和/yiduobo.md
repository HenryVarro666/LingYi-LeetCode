---
title: "2829. k-avoiding数组的最小总和"
aliases: ["yiduobo的每日leetcode 2829.k-avoiding数组的最小总和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/math", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659175147"
zhihu_id: "659175147"
zhihu_title: "yiduobo的每日leetcode 2829.k-avoiding数组的最小总和"
question_id: "2829"
question: "k-avoiding 数组的最小总和"
problem_url: "https://leetcode.cn/problems/determine-the-minimum-sum-of-a-k-avoiding-array/"
difficulty: "Medium"
rating: 1347
created: "2023-09-30T22:23:23+08:00"
updated: "2023-09-30T22:23:23+08:00"
upvotes: 0
comments: 0
---

# 2829. k-avoiding数组的最小总和

> **[yiduobo的每日leetcode 2829.k-avoiding数组的最小总和](https://zhuanlan.zhihu.com/p/659175147) · 知乎 · 2023-09-30 · 赞同 0**
> 力扣：[2829. k-avoiding 数组的最小总和](https://leetcode.cn/problems/determine-the-minimum-sum-of-a-k-avoiding-array/) · Medium · 灵茶山艾府：[O(1) 公式（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2829.k-avoiding数组的最小总和

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/determine-the-minimum-sum-of-a-k-avoiding-array/)

首先考虑特殊情况。当k \<\= 2时，由于选择的数字互不相同，那么必然不会出现两个数字之和等于k，因此在这种情况下就应该选择最小的n个自然数，这些数的和就是(1 + n) \* n / 2。

接下来对于k > 2的情况，此时就存在若干组和等于k的数对。等k为奇数时，有(1, k - 1)、(2, k - 2)、...、(k / 2, k / 2 + 1)这些数对，而当k等于偶数时，则有(1, k - 1)、(2, k - 2)、(k / 2 - 1, k / 2 + 1)这些数对。

为了使得答案最小，无论是奇数还是偶数的情况，在小于k的数中都只能选择1到k / 2这些数，而k / 2 + 1到k - 1这些则必然会被丢弃。

记m \= k / 2，那么当n \<\= m时，依然是直接选择1到n这些数，于是此时的答案同样是(1 + n) \* n / 2。

当n > m时，就只能先选择1到m，然后对于剩下的n - m个数，则需要从k开始向上选择，也就是最终将选择1到m，以及k到k + n - m + 1这两段，此时的答案就是(1 + m) \* m / 2 + (k + k + n - m + 1) \* (n - m) / 2。

最后附上python代码：

```python
class Solution(object):
    def minimumSum(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """

        if k <= 2:
            return (1 + n) * n / 2

        m = k / 2
        if m >= n:
            return (1 + n) * n / 2
        else:
            return (1 + m) * m / 2 + (k + k + n - m - 1) * (n - m) / 2
```
