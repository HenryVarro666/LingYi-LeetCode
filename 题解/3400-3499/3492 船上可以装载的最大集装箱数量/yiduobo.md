---
title: "3492. 船上可以装载的最大集装箱数量"
aliases: ["yiduobo的每日leetcode 3492.船上可以装载的最大集装箱数量"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1899507605950412364"
zhihu_id: "1899507605950412364"
zhihu_title: "yiduobo的每日leetcode 3492.船上可以装载的最大集装箱数量"
question_id: "3492"
question: "船上可以装载的最大集装箱数量"
problem_url: "https://leetcode.cn/problems/maximum-containers-on-a-ship/"
difficulty: "Easy"
created: "2025-04-26T17:01:45+08:00"
updated: "2025-04-26T17:01:45+08:00"
upvotes: 0
comments: 0
---

# 3492. 船上可以装载的最大集装箱数量

> **[yiduobo的每日leetcode 3492.船上可以装载的最大集装箱数量](https://zhuanlan.zhihu.com/p/1899507605950412364) · 知乎 · 2025-04-26 · 赞同 0**
> 力扣：[3492. 船上可以装载的最大集装箱数量](https://leetcode.cn/problems/maximum-containers-on-a-ship/) · Easy · 灵茶山艾府：[O(1) 公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3492.船上可以装载的最大集装箱数量

[3492. 船上可以装载的最大集装箱数量 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-containers-on-a-ship/description/)

题目给出一个正整数n，表示船上有一个n \* n的货物甲板，甲板上的每个单元格可以装载一个重量恰好为w的集装箱。另外，船的最大承载重连为maxWeight。问最多可以装载到船上的集装箱数量。

受空间限制，船上集装箱的数量不超过n \* n。另一方面，受重量限制，船上集装箱的数量不超过maxWeight // w。取二者的较小值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxContainers(self, n, w, maxWeight):
        """
        :type n: int
        :type w: int
        :type maxWeight: int
        :rtype: int
        """
        
        res = maxWeight // w
        if res > n * n:
            res = n * n
        return res
```
