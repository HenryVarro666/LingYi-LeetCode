---
title: "3599. 划分数组得到最小XOR"
aliases: ["yiduobo的每日leetcode 3599.划分数组得到最小XOR"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/prefix-sum", "leetcode/shortest-path", "leetcode/heap-priority-queue", "题单/动态规划", "题单/图论算法", "题单/动态规划/五-划分型-DP", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1941270820774196473"
zhihu_id: "1941270820774196473"
zhihu_title: "yiduobo的每日leetcode 3599.划分数组得到最小XOR"
question_id: "3599"
question: "划分数组得到最小 XOR"
problem_url: "https://leetcode.cn/problems/partition-array-to-minimize-xor/"
difficulty: "Medium"
rating: 1955
created: "2025-08-19T22:58:25+08:00"
updated: "2025-08-19T22:58:25+08:00"
upvotes: 0
comments: 0
---

# 3599. 划分数组得到最小XOR

> **[yiduobo的每日leetcode 3599.划分数组得到最小XOR](https://zhuanlan.zhihu.com/p/1941270820774196473) · 知乎 · 2025-08-19 · 赞同 0**
> 力扣：[3599. 划分数组得到最小 XOR](https://leetcode.cn/problems/partition-array-to-minimize-xor/) · Medium · 灵茶山艾府：[划分型 DP 的通用套路，附二分 / Dijkstra 做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3599.划分数组得到最小XOR

<https://leetcode.cn/problems/partition-array-to-minimize-xor/description/>

题目给出一个整数数组nums以及一个整数k，nums的长度不超过250。

现在要求将nums拆分为k个非空的子数组，对于每个子数组，计算其所有元素的按位异或值，返回这k个子数组中最大异或值的最小值。

经典的划分类问题，令f[index][p]表示将前index个数划分成p个子数组时，这些子数组中最大异或值的最小值，那么对于f[index][p]：

1、当p \= 1时，只有一个子数组，因此就有f[index][p] \= f[index - 1][p] ^ nums[p]

2、当p > 1时，则可以从index开始向前枚举分割点cut_pos，那么就有f[index][p] \= min(f[index][p], max(f[cut_pos][p - 1], xor(cut_pos + 1, index))，这里的xor表示子数组的异或值。由于是从后往前枚举，因此这个异或值只需在之前的基础上再异或当前元素就行了。

全部计算完成后，f[-1][-1]即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minXor(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        n = len(nums)

        f = [[None] * (k + 1) for _ in range(n)]
        for index in range(n):
            for p in range(1, k + 1):
                if p == 1:
                    if index == 0:
                        f[index][p] = nums[index]
                    else:
                        f[index][p] = f[index - 1][p] ^ nums[index]
                else:
                    xor = 0
                    for cut_pos in range(index, p - 2, -1):
                        xor ^= nums[cut_pos]
                        v = max(f[cut_pos - 1][p - 1], xor)
                        if f[index][p] is None or f[index][p] > v:
                            f[index][p] = v

        return f[-1][-1]
```
