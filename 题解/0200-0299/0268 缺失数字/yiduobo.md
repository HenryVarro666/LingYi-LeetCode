---
title: "268. 缺失数字"
aliases: ["yiduobo的每日leetcode 268.缺失数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/151849187"
zhihu_id: "151849187"
zhihu_title: "yiduobo的每日leetcode 268.缺失数字"
question_id: "268"
question: "缺失数字"
problem_url: "https://leetcode.cn/problems/missing-number/"
created: "2020-06-29T22:24:19+08:00"
updated: "2020-06-29T22:24:19+08:00"
upvotes: 0
comments: 0
---

# 268. 缺失数字

> **[yiduobo的每日leetcode 268.缺失数字](https://zhuanlan.zhihu.com/p/151849187) · 知乎 · 2020-06-29 · 赞同 0**
> 力扣：[268. 缺失数字](https://leetcode.cn/problems/missing-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

268.缺失数字<https://leetcode-cn.com/problems/missing-number/>

比较简单的数学题。首先我们知道0加到n的和为n \* (n + 1) / 2，那么在这里我们只需要计算出nums的和，然后使用n \* (n + 1) / 2减去这个和，就能得到缺失的那个数了。

最后附上python代码：

```python
class Solution(object):
    def missingNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        return (1 + len(nums)) * len(nums) / 2 - sum(nums)
```
