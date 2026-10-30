---
title: "1434. 每个人戴不同帽子的方案数"
aliases: ["yiduobo的每日leetcode 1434.每个人戴不同帽子的方案数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/409320275"
zhihu_id: "409320275"
zhihu_title: "yiduobo的每日leetcode 1434.每个人戴不同帽子的方案数"
question_id: "1434"
question: "每个人戴不同帽子的方案数"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-wear-different-hats-to-each-other/"
created: "2021-09-11T15:16:12+08:00"
updated: "2021-09-11T15:16:12+08:00"
upvotes: 1
comments: 0
---

# 1434. 每个人戴不同帽子的方案数

> **[yiduobo的每日leetcode 1434.每个人戴不同帽子的方案数](https://zhuanlan.zhihu.com/p/409320275) · 知乎 · 2021-09-11 · 赞同 1**
> 力扣：[1434. 每个人戴不同帽子的方案数](https://leetcode.cn/problems/number-of-ways-to-wear-different-hats-to-each-other/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1434.每个人戴不同帽子的方案数

[力扣](https://leetcode-cn.com/problems/number-of-ways-to-wear-different-hats-to-each-other/)

动态规划的题目，注意到这里的人数n最多只有10，那么很自然想到使用二进制编码来进行状态压缩。

令f[i][state]表示前i + 1顶帽子，给state表示的人来戴有多少种方案。那么对于f[i][state]，可以先枚举第i + 1顶帽子可以给哪些人来戴，设当前枚举到的人为p，若此时state&(1\<\<p)不为0，就说明当前这顶帽子可以给p这个人来戴，那么之前的帽子就需要覆盖住state^(1\<\<p)这些人，于是就有f[i][state] +\= f[i - 1][state^(1\<\<p)]。

由于这里的每一轮的状态只与上一轮有关，因此可以使用滚动数组的方法优化掉其中一维。

最后附上python代码：

```python
class Solution(object):
    def numberWays(self, hats):
        """
        :type hats: List[List[int]]
        :rtype: int
        """

        hat_dict = {}
        for index, hat_list in enumerate(hats):
            for hat in hat_list:
                if hat not in hat_dict:
                    hat_dict[hat] = []
                hat_dict[hat].append(index)
        
        n = len(hats)
        max_state = 1 << n

        l = len(hat_dict)

        g = [0] * max_state
        g[0] = 1

        mod = 10 ** 9 + 7

        for hat in hat_dict.keys():
            f = g[:]
            for state in range(1, max_state):
                for p in hat_dict[hat]:
                    if state & (1 << p):
                        f[state] += g[state ^ (1 << p)]
                        f[state] %= mod
        
            g = f[:]
        
        return f[-1]
```
