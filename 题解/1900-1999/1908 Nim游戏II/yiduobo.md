---
title: "1908. Nim游戏II"
aliases: ["yiduobo的每日leetcode 1908.Nim游戏II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/623299802"
zhihu_id: "623299802"
zhihu_title: "yiduobo的每日leetcode 1908.Nim游戏II"
question_id: "1908"
question: "Nim游戏II"
problem_url: "https://leetcode.cn/problems/game-of-nim/"
created: "2023-04-20T01:06:27+08:00"
updated: "2023-04-20T01:06:27+08:00"
upvotes: 1
comments: 0
---

# 1908. Nim游戏II

> **[yiduobo的每日leetcode 1908.Nim游戏II](https://zhuanlan.zhihu.com/p/623299802) · 知乎 · 2023-04-20 · 赞同 1**
> 力扣：[1908. Nim游戏II](https://leetcode.cn/problems/game-of-nim/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1908.Nim游戏II

[力扣](https://leetcode.cn/problems/game-of-nim/)

题目标题明着写了是nim游戏，那么最好的处理方法自然是sg函数。关于sg函数之前294题也使用到了，在这里也不打算展开来说。

对于本题，piles中的每一堆石头都可以视为一个平等的子局面，那么对于其中某一堆石头v，都有sg(v) \= v。证明则可以使用归纳法。首先必然有sg(0) \= 0，sg(1) \= 1，而对于i > 1的情况，若0 \<\= j \< i的所有j都满足sg(j) \= j，那么就有sg(i) \= mex(sg(0)，sg(1)，...，sg(i - 1)) \= mex(0, 1, ..., i - 1) \= i。这里mex中是sg(0)到sg(i - 1)的理由是对于i颗石头，可以选择取走1到i颗石头，那么剩下的石头就是i - 1、i - 2、...、1、0这些情况中的一种。

得到sg(v) \= v这一结论后，只需将这些自局面的sg值异或起来即为最终答案，因此最终答案就是piles中的所有数全部异或起来。

最后附上python代码：

```python
class Solution(object):
    def nimGame(self, piles):
        """
        :type piles: List[int]
        :rtype: bool
        """

        v = 0
        for p in piles:
            v ^= p
        
        return v > 0
```
