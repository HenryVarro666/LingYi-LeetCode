---
title: "4081. 选择质数子集II"
aliases: ["yiduobo的每日leetcode 4081.选择质数子集II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2094957695732340069"
zhihu_id: "2094957695732340069"
zhihu_title: "yiduobo的每日leetcode 4081.选择质数子集II"
question_id: "4081"
question: "选择质数子集II"
problem_url: "https://leetcode.cn/problems/prime-subset-selection-ii/"
created: "2026-10-18T02:23:47+08:00"
updated: "2026-10-18T02:23:52+08:00"
upvotes: 0
comments: 0
---

# 4081. 选择质数子集II

> **[yiduobo的每日leetcode 4081.选择质数子集II](https://zhuanlan.zhihu.com/p/2094957695732340069) · 知乎 · 2026-10-18 · 赞同 0**
> 力扣：[4081. 选择质数子集II](https://leetcode.cn/problems/prime-subset-selection-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4081.选择质数子集II

<https://leetcode.cn/problems/prime-subset-selection-ii/>

题目给出两个正整数n和s，大小均不超过1000。

对于所有小于等于n的质数，从中选出一个子集，满足：

- 每个质数只能使用一次
- 选择的质数之和不超过s，且总和最大
- 在总和最大的前提下，选择的质数尽量少
- 如果总和相同，且选择的质数数量一致，则将各子集中的质数排序，然后选择字典序最小的

要求返回一个递增的数组，包含选择的质数。

非常标准的背包问题，不过要求选择尽量少的元素，同时需要字典序最小，并输出方案。

对于选择尽量少的元素这一要求，需要将其编入状态表示中，最直观的就是f[index][x]表示遍历了index个质数凑出和为x时，最少需要选择的质数数量。那么对于f[index][x]，设最后这个质数为v，那么就有f[index][x] \= min(f[index][x], f[index - 1][x - v])。

而对于字典序最小的方案，则可以通过从大到小遍历这些质数，并使用一个辅助数组use来记录每种状态是怎么转移得到的。

在这里选择从大到小的遍历顺序就可以保证最终方案的字典序最小，其原理和基数排序相同，越后更新状态的元素，其可能覆盖前面元素的决策，因此倒序遍历的话，可以使得越小的质数的优先级越高，从而保证字典序最小。

而对于use的使用，如果f[index][x]是从f[index - 1][x - v]过来的，就记录use[index][x]为v，表示是使用了v过来的；反过来，则记录use[index][x]为0，表示这一轮没有使用，直接通过上一轮的f[index - 1][x]过来。最后计算完成后，从index \= m(这里的m表示参与计算的质数的个数), x \= s开始向前倒推，每一轮将x减去use[index][x]，然后将index减一，将过程中所有非0的use收集起来，就得到了具体的方案。

需要注意的是，这里不能利用倒序遍历省去index这一维，理由是在这里需要记录方案，因此f[index - 1][x - v]必须是原汁原味，但是倒序遍历的话省去index的话，f[x - v]将被v再次更新，这样一来f[x]往前追溯到的就不是理想中的f[index - 1][x - v]，而是f[index][x - v]了，这样use就货不对版了。

最后附上python代码：

```python
class Solution(object):
    def maxPrimeSubset(self, n, s):
        """
        :type n: int
        :type s: int
        :rtype: List[int]
        """
        
        g = [True] * (n + 1)
        x = 2
        p = []
        while x <= n:
            if g[x]:
                p.append(x)
                for v in range(x + x, n + 1, x):
                    g[v] = False
            x += 1
        
        m = len(p)
        f = [[-1] * (s + 1) for _ in range(m + 1)]
        f[0][0] = 0
        use = [[None] * (s + 1) for _ in range(m + 1)]
        for index, v in enumerate(p[::-1], 1):
            for x in range(s + 1):
                f[index][x] = f[index - 1][x]
                use[index][x] = 0
                if x >= v and f[index - 1][x - v] != -1 and (f[index][x] == -1 or f[index][x] >= f[index - 1][x - v] + 1):
                    f[index][x] = f[index - 1][x - v] + 1
                    use[index][x] = v

        x = s
        res = []
        while x > 0 and f[-1][x] == -1:
            x -= 1

        index = m
        while x > 0:
            if use[index][x] > 0:
                res.append(use[index][x])
            x -= use[index][x]
            index -= 1
        
        return res
```
