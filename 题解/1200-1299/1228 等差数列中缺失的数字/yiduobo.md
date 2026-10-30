---
title: "1228. 等差数列中缺失的数字"
aliases: ["yiduobo的每日leetcode 1228.等差数列中缺失的数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/613445088"
zhihu_id: "613445088"
zhihu_title: "yiduobo的每日leetcode 1228.等差数列中缺失的数字"
question_id: "1228"
question: "等差数列中缺失的数字"
problem_url: "https://leetcode.cn/problems/missing-number-in-arithmetic-progression/"
created: "2023-03-12T23:18:36+08:00"
updated: "2023-03-12T23:18:36+08:00"
upvotes: 0
comments: 2
---

# 1228. 等差数列中缺失的数字

> **[yiduobo的每日leetcode 1228.等差数列中缺失的数字](https://zhuanlan.zhihu.com/p/613445088) · 知乎 · 2023-03-12 · 赞同 0**
> 力扣：[1228. 等差数列中缺失的数字](https://leetcode.cn/problems/missing-number-in-arithmetic-progression/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1228.等差数列中缺失的数字

[力扣](https://leetcode.cn/problems/missing-number-in-arithmetic-progression/)

如果没有缺失数字，那么arr中各个数字的总和s就可以通过等差数列求和公式得到。只需使用s减去当前arr的和，就得到缺失的数值了。

最后附上python代码：

```python
class Solution(object):
    def missingNumber(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        return (arr[0] + arr[-1]) * (len(arr) + 1) / 2 - sum(arr)
```
