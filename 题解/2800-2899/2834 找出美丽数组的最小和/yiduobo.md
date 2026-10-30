---
title: "2834. 找出美丽数组的最小和"
aliases: ["yiduobo的每日leetcode 2834.找出美丽数组的最小和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659572809"
zhihu_id: "659572809"
zhihu_title: "yiduobo的每日leetcode 2834.找出美丽数组的最小和"
question_id: "2834"
question: "找出美丽数组的最小和"
problem_url: "https://leetcode.cn/problems/find-the-minimum-possible-sum-of-a-beautiful-array/"
difficulty: "Medium"
rating: 1409
created: "2023-10-05T02:09:58+08:00"
updated: "2023-10-05T02:09:58+08:00"
upvotes: 0
comments: 0
---

# 2834. 找出美丽数组的最小和

> **[yiduobo的每日leetcode 2834.找出美丽数组的最小和](https://zhuanlan.zhihu.com/p/659572809) · 知乎 · 2023-10-05 · 赞同 0**
> 力扣：[2834. 找出美丽数组的最小和](https://leetcode.cn/problems/find-the-minimum-possible-sum-of-a-beautiful-array/) · Medium · 灵茶山艾府：[O(1) 数学公式（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

昨日外出漏更，今天补上

2834.找出美丽数组的最小和

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/find-the-minimum-possible-sum-of-a-beautiful-array/)

本题与之前的2829题相同，不过数据范围大了不少，但数据规模的变化对之前O(1)的算法不会产生任何影响，直接套用就行了。

[yiduobo：yiduobo的每日leetcode 2829.k-avoiding数组的最小总和](https://zhuanlan.zhihu.com/p/659175147)

最后附上python代码：

```python
class Solution(object):
    def minimumPossibleSum(self, n, target):
        """
        :type n: int
        :type target: int
        :rtype: int
        """

        if target <= 2:
            return (1 + n) * n / 2

        m = target / 2
        if m >= n:
            return (1 + n) * n / 2
        else:
            return (1 + m) * m / 2 + (target + target + n - m - 1) * (n - m) / 2
```
