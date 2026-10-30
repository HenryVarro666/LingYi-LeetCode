---
title: "2177. 找到和为给定整数的三个连续整数"
aliases: ["yiduobo的每日leetcode 2177.找到和为给定整数的三个连续整数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/534641022"
zhihu_id: "534641022"
zhihu_title: "yiduobo的每日leetcode 2177.找到和为给定整数的三个连续整数"
question_id: "2177"
question: "找到和为给定整数的三个连续整数"
problem_url: "https://leetcode.cn/problems/find-three-consecutive-integers-that-sum-to-a-given-number/"
difficulty: "Medium"
created: "2022-06-28T00:16:40+08:00"
updated: "2022-06-28T00:16:40+08:00"
upvotes: 0
comments: 0
---

# 2177. 找到和为给定整数的三个连续整数

> **[yiduobo的每日leetcode 2177.找到和为给定整数的三个连续整数](https://zhuanlan.zhihu.com/p/534641022) · 知乎 · 2022-06-28 · 赞同 0**
> 力扣：[2177. 找到和为给定整数的三个连续整数](https://leetcode.cn/problems/find-three-consecutive-integers-that-sum-to-a-given-number/) · Medium · 灵茶山艾府：[简单数学](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2177.找到和为给定整数的三个连续整数

[力扣](https://leetcode.cn/problems/find-three-consecutive-integers-that-sum-to-a-given-number/)

不是很懂leetcode给题目标记难度是按什么标准来的，这个题居然是中等难度。。。

设三个连续整数正中间那个为x，那么三个整数的和就是3x。只需判断num是否为3的倍数，如果是，那么num / 3就是x，另外两个数就是x - 1和x + 1；如果不是，那么直接返回空数组。

最后附上python代码：

```python
class Solution(object):
    def sumOfThree(self, num):
        """
        :type num: int
        :rtype: List[int]
        """

        if num % 3 == 0:
            return [num / 3 - 1, num / 3, num / 3 + 1]
        
        return []
```
