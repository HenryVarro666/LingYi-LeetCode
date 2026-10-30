---
title: "370. 区间加法"
aliases: ["yiduobo的每日leetcode 370.区间加法"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/598682561"
zhihu_id: "598682561"
zhihu_title: "yiduobo的每日leetcode 370.区间加法"
question_id: "370"
question: "区间加法"
problem_url: "https://leetcode.cn/problems/range-addition/"
created: "2023-01-13T04:43:04+08:00"
updated: "2023-01-13T04:43:04+08:00"
upvotes: 0
comments: 0
---

# 370. 区间加法

> **[yiduobo的每日leetcode 370.区间加法](https://zhuanlan.zhihu.com/p/598682561) · 知乎 · 2023-01-13 · 赞同 0**
> 力扣：[370. 区间加法](https://leetcode.cn/problems/range-addition/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

370.区间加法

[力扣](https://leetcode.cn/problems/range-addition/)

非常标准的差分数组的问题，具体实现上与之前的253题类似，不过在这里每次加减的值应该是inc而不是1。

[yiduobo：yiduobo的每日leetcode 253.会议室II](https://zhuanlan.zhihu.com/p/592765637)

最后附上python代码：

```python
class Solution(object):
    def getModifiedArray(self, length, updates):
        """
        :type length: int
        :type updates: List[List[int]]
        :rtype: List[int]
        """

        f = [0] * length
        for x, y, inc in updates:
            f[x] += inc
            if y + 1 < length:
                f[y + 1] -= inc
        
        now = 0
        res = []
        for index in range(length):
            now += f[index]
            res.append(now)
        return res
```
