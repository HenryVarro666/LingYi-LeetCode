---
title: "2485. 找出中枢整数"
aliases: ["yiduobo的每日leetcode 2485.找出中枢整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/589500503"
zhihu_id: "589500503"
zhihu_title: "yiduobo的每日leetcode 2485.找出中枢整数"
question_id: "2485"
question: "找出中枢整数"
problem_url: "https://leetcode.cn/problems/find-the-pivot-integer/"
difficulty: "Easy"
created: "2022-12-06T01:34:50+08:00"
updated: "2022-12-06T01:34:50+08:00"
upvotes: 0
comments: 0
---

# 2485. 找出中枢整数

> **[yiduobo的每日leetcode 2485.找出中枢整数](https://zhuanlan.zhihu.com/p/589500503) · 知乎 · 2022-12-06 · 赞同 0**
> 力扣：[2485. 找出中枢整数](https://leetcode.cn/problems/find-the-pivot-integer/) · Easy · 灵茶山艾府：[两种 O(1) 做法：数学公式 / 打表（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2485.找出中枢整数

[力扣](https://leetcode.cn/problems/find-the-pivot-integer/)

根据题目的描述，1到x之间所有整数的和为(1 + x) \* x / 2，而x到n之间所有整数的和可以写成1到n的和减去1到(x - 1)的和，也就是(1 + n) \* n / 2 - (1 + x - 1) \* (x - 1) / 2。

这两部分相等，就有

x^2 + x \= (1 + n) \* n - x^2 + x

整理后就有

x^2 \= (1 + n) \* n / 2

接下来只需检测x是否存在整数解就行了

最后附上python代码：

```python
class Solution(object):
    def pivotInteger(self, n):
        """
        :type n: int
        :rtype: int
        """

        c = n * (n + 1) / 2
        x = int(sqrt(c))
        if x * x == c:
            return x
        
        return -1
```
