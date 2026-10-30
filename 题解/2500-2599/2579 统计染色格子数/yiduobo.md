---
title: "2579. 统计染色格子数"
aliases: ["yiduobo的每日leetcode 2579.统计染色格子数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/642375264"
zhihu_id: "642375264"
zhihu_title: "yiduobo的每日leetcode 2579.统计染色格子数"
question_id: "2579"
question: "统计染色格子数"
problem_url: "https://leetcode.cn/problems/count-total-number-of-colored-cells/"
difficulty: "Medium"
rating: 1356
created: "2023-07-08T23:46:33+08:00"
updated: "2023-07-08T23:46:33+08:00"
upvotes: 0
comments: 0
---

# 2579. 统计染色格子数

> **[yiduobo的每日leetcode 2579.统计染色格子数](https://zhuanlan.zhihu.com/p/642375264) · 知乎 · 2023-07-08 · 赞同 0**
> 力扣：[2579. 统计染色格子数](https://leetcode.cn/problems/count-total-number-of-colored-cells/) · Medium · 灵茶山艾府：[找规律](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2579.统计染色格子数

[力扣](https://leetcode.cn/problems/count-total-number-of-colored-cells/)

找规律的题目。分析样例可以发现，第n轮相当于在第n - 1的轮的基础上额外添加了4 \* (n - 1)个格子，那么直接套用求和公式就可以得到最终染色格子数为1 + 4 \* 1 + 4 \* 2 + ... + 4 \* (n - 1) \= 2 \* (n - 1) \* n + 1。

最后附上python代码：

```python
class Solution(object):
    def coloredCells(self, n):
        """
        :type n: int
        :rtype: int
        """

        return n * (n - 1) * 2 + 1
```
