---
title: "1049. 最后一块石头的重量II"
aliases: ["yiduobo的每日leetcode 1049.最后一块石头的重量II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/371553680"
zhihu_id: "371553680"
zhihu_title: "yiduobo的每日leetcode 1049.最后一块石头的重量II"
question_id: "1049"
question: "最后一块石头的重量II"
problem_url: "https://leetcode.cn/problems/last-stone-weight-ii/"
created: "2021-05-11T23:32:32+08:00"
updated: "2021-05-11T23:32:32+08:00"
upvotes: 0
comments: 0
---

# 1049. 最后一块石头的重量II

> **[yiduobo的每日leetcode 1049.最后一块石头的重量II](https://zhuanlan.zhihu.com/p/371553680) · 知乎 · 2021-05-11 · 赞同 0**
> 力扣：[1049. 最后一块石头的重量II](https://leetcode.cn/problems/last-stone-weight-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1049.最后一块石头的重量II

[力扣](https://leetcode-cn.com/problems/last-stone-weight-ii/)

由于每一轮可以任意选取两块石头，那么这里的问题实际上就是如何将石头划分成两个部分，使这两个部分重量之差最小。于是又转化成了经典的背包问题。

首先计算出所有石头的和s，那么我们的目标就是从这些石头中选出一些，使得这些石头的重量之后尽可能地接近target \= s / 2。

令f[i][j]表示能否从前i块石头中选出一些凑成重量j，边界条件为f[0][0] \= true。对于f[i][j]，可以选择第i - 1块石头也可以不选，那么就有

f\[i\]\[j\] \= f\[i - 1\]\[j\] or f\[i - 1\]\[j - stones\[i - 1\]\]

又由于每一轮状态只与上一轮有关，那么可以省去i这一维，通过从大到小枚举j的方式进行动态规划。

动态规划完成之后，从target开始向下枚举，若当前的f[target]为true，那么答案就是

(s - target) - target

最后附上python代码：

```python
class Solution(object):
    def lastStoneWeightII(self, stones):
        """
        :type stones: List[int]
        :rtype: int
        """

        n = len(stones)
        s = sum(stones)
        target = s / 2

        f = [False] * (target + 1)
        f[0] = True
        for stone in stones:
            for l in range(target, stone - 1, -1):
                if f[l - stone]:
                    f[l] = True
        
        while not f[target]:
            target -= 1
        
        return s - target - target
```
