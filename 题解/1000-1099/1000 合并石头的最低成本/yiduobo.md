---
title: "1000. 合并石头的最低成本"
aliases: ["yiduobo的每日leetcode 1000.合并石头的最低成本"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/prefix-sum", "leetcode/tu-jie", "leetcode/dp-2", "题单/动态规划", "题单/动态规划/八-区间-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/365859585"
zhihu_id: "365859585"
zhihu_title: "yiduobo的每日leetcode 1000.合并石头的最低成本"
question_id: "1000"
question: "合并石头的最低成本"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-merge-stones/"
difficulty: "Hard"
rating: 2423
created: "2021-04-18T21:19:03+08:00"
updated: "2021-04-18T21:19:03+08:00"
upvotes: 2
comments: 0
---

# 1000. 合并石头的最低成本

> **[yiduobo的每日leetcode 1000.合并石头的最低成本](https://zhuanlan.zhihu.com/p/365859585) · 知乎 · 2021-04-18 · 赞同 2**
> 力扣：[1000. 合并石头的最低成本](https://leetcode.cn/problems/minimum-cost-to-merge-stones/) · Hard · 灵茶山艾府：[【图解】区间 DP：状态设计与优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1000.合并石头的最低成本

[力扣](https://leetcode-cn.com/problems/minimum-cost-to-merge-stones/)

经典的区间动态规划问题，不过这里是进阶版。原版问题是合并两堆石头，这里是合并K堆。

首先来判断是否有解。执行一次合并操作之后，会将k堆石头变为1堆石头，那么总的石头堆数就是减少了k - 1堆。初始有n堆石头，我们的目标是将其变为1堆，也就是减少n - 1堆，于是这里需要n - 1是k - 1的倍数才能保证最后能合成一堆石头，即当(N - 1) % (K - 1) !\= 0 时，直接返回-1。

接下来进行动态规划，依然是经典区间[i, j]来表示状态。需要注意的是，这里区间长度l \= j - i + 1并不一定满足(l - 1) % (k - 1) \= 0，也就是说区间[i, j]并不一定可以合并成为1堆石头，于是在这里f[i][j]定义为尽可能合并区间[i, j]之间的石头所需的最小代价。

那么对于f[i][j]，设l \= j - i + 1：

1、当l \< k时，f[i][j]已经无法再合并，于是有f[i][j] \= 0

2、当l >\= k 时，我们枚举分割点cut_pos。

需要注意的是，这里分割点的枚举需要将合并操作隐藏在里面，例如区间[0, 3]，当k\=3时，此时的分割点就不应该是1，因为此时0到3可以执行1次合并，但是将区间分割成[0, 1], [2, 3]之后就失去了这次合并的机会。

换言之，这里的分割点必须分割出一个可合并的部分，也就是(cut_pos - i + 1 - 1) % (k - 1) \= 0。于是我们需要从i开始，以步长k - 1开始枚举cut_pos，那么就有

f[i][j] \= min(f[i][cut_pos] + f[cut + 1][j])

求得f[i][j]之后，若此时的(l - 1) % (k - 1) \= 0，说明f[i][j]最终可以合并为1堆石头，那么此时合并的代价就是stones[i] + stones[i + 1] + ... + stones[j]。这里是熟悉的区间和形式，可以预处理出前缀和然后通过prefix[j] - prefix[i - 1]快速求得。

另外，在执行动态规划时，由于f[i][j]的更新依赖于f[i][cut_pos]以及f[cut_pos][j]，于是我们应该优先求解较短的区间，也就是先枚举区间长度l，然后枚举i并通过i + l - 1计算出j。

最后附上python代码：

```python
class Solution(object):
    def mergeStones(self, stones, K):
        """
        :type stones: List[int]
        :type K: int
        :rtype: int
        """

        n = len(stones)
        if (n - 1) % (K - 1) != 0:
            return -1
        
        f = [[None] * n for _ in range(n)]
        s = [stones[0]]
        for num in stones[1:]:
            s.append(s[-1] + num)

        for l in range(1, n + 1):
            for i in range(n - l + 1):
                j = i + l - 1
                if l < K:
                    f[i][j] = 0
                else:
                    for cut_pos in range(i, j, K - 1):
                        tmp = f[i][cut_pos] + f[cut_pos + 1][j]
                        if f[i][j] is None or f[i][j] > tmp:
                            f[i][j] = tmp

                    if (l - 1) % (K - 1) == 0:
                        f[i][j] += s[j]
                        if i > 0:
                            f[i][j] -= s[i - 1]
        
        return f[0][n - 1]
```
