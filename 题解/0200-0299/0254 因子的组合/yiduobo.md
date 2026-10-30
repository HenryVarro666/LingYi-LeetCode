---
title: "254. 因子的组合"
aliases: ["yiduobo的每日leetcode 254.因子的组合"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/592766649"
zhihu_id: "592766649"
zhihu_title: "yiduobo的每日leetcode 254.因子的组合"
question_id: "254"
question: "因子的组合"
problem_url: "https://leetcode.cn/problems/factor-combinations/"
created: "2022-12-18T23:08:25+08:00"
updated: "2022-12-18T23:08:25+08:00"
upvotes: 0
comments: 0
---

# 254. 因子的组合

> **[yiduobo的每日leetcode 254.因子的组合](https://zhuanlan.zhihu.com/p/592766649) · 知乎 · 2022-12-18 · 赞同 0**
> 力扣：[254. 因子的组合](https://leetcode.cn/problems/factor-combinations/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

254.因子的组合

[力扣](https://leetcode.cn/problems/factor-combinations/)

题目并没有给出数据规模，但是由于题目要求输出所有可能的因子组合，那么注定了n的规模不会太大，于是可以枚举n的所有因子x，递归求解n / x的所有因子组合，然后在这些因子组合的基础上添加x，就得到了乘积为n的因子组合。由于某些整数可能出现多次计算，因此在这里可以使用记忆化搜索来优化这个过程。

不过这个做法有可能出现重复计算的情况，例如对于8，当枚举到因子2时，可以得到[2, 4]，[2，2，2]这两组答案，而枚举到因子4时，则可以得到[4, 2]这组答案。可以发现，[2，4]和[4，2]是重复的。

在这里最简单的处理方法就是对于合并的因子组合以及x，若这个因子组合中最小的因子大于等于x，才执行合并操作，这样一来就可以保证得到的所有因子组合都是单调不增的，从而保证了没有重复情况的出现。

另外还需要注意一点，使用上面这种做法计算所有因子时，会将n自身不动作为一个合法的答案，因此在返回最终结果时需要注意去掉这种情况。

最后附上python代码：

```python
class Solution(object):
    def getFactors(self, n):
        """
        :type n: int
        :rtype: List[List[int]]
        """

        f = {}
        f[1] = []

        def dfs(now,):
            if now not in f:
                f[now] = [[now]]
                x = 2
                while x * x <= now:
                    if now % x == 0:
                        for combo in dfs(now / x):
                            if combo[-1] >= x:
                                f[now].append(combo[:])
                                f[now][-1].append(x)
                    x += 1

            return f[now]

        return dfs(n)[1:]
```
