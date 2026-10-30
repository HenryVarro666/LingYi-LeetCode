---
title: "2640. 一个数组所有前缀的分数"
aliases: ["yiduobo的每日leetcode 2640.一个数组所有前缀的分数"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/646650851"
zhihu_id: "646650851"
zhihu_title: "yiduobo的每日leetcode 2640.一个数组所有前缀的分数"
question_id: "2640"
question: "一个数组所有前缀的分数"
problem_url: "https://leetcode.cn/problems/find-the-score-of-all-prefixes-of-an-array/"
difficulty: "Medium"
created: "2023-07-29T03:06:50+08:00"
updated: "2023-07-29T03:06:50+08:00"
upvotes: 0
comments: 0
---

# 2640. 一个数组所有前缀的分数

> **[yiduobo的每日leetcode 2640.一个数组所有前缀的分数](https://zhuanlan.zhihu.com/p/646650851) · 知乎 · 2023-07-29 · 赞同 0**
> 力扣：[2640. 一个数组所有前缀的分数](https://leetcode.cn/problems/find-the-score-of-all-prefixes-of-an-array/) · Medium · 灵茶山艾府：[一边遍历，一边计算](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2640.一个数组所有前缀的分数

[力扣](https://leetcode.cn/problems/find-the-score-of-all-prefixes-of-an-array/)

按照题目描述对nums进行一趟遍历，计算出conver数组，然后再对conver数组一趟遍历，计算出该数组的前缀和作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def findPrefixScore(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        ma = 0
        conver = []
        for v in nums:
            ma = max(ma, v)
            conver.append(v + ma)
        
        res = []
        for v in conver:
            if not res:
                res.append(v)
            else:
                res.append(res[-1] + v)
        
        return res
```
