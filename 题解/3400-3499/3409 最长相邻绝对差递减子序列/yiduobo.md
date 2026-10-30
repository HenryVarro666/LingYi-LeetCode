---
title: "3409. 最长相邻绝对差递减子序列"
aliases: ["yiduobo的每日leetcode 3409.最长相邻绝对差递减子序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/31922415548"
zhihu_id: "31922415548"
zhihu_title: "yiduobo的每日leetcode 3409.最长相邻绝对差递减子序列"
question_id: "3409"
question: "最长相邻绝对差递减子序列"
problem_url: "https://leetcode.cn/problems/longest-subsequence-with-decreasing-adjacent-difference/"
difficulty: "Medium"
rating: 2500
created: "2025-03-21T23:22:38+08:00"
updated: "2025-03-21T23:22:38+08:00"
upvotes: 0
comments: 0
---

# 3409. 最长相邻绝对差递减子序列

> **[yiduobo的每日leetcode 3409.最长相邻绝对差递减子序列](https://zhuanlan.zhihu.com/p/31922415548) · 知乎 · 2025-03-21 · 赞同 0**
> 力扣：[3409. 最长相邻绝对差递减子序列](https://leetcode.cn/problems/longest-subsequence-with-decreasing-adjacent-difference/) · Medium · 灵茶山艾府：[状态设计 + 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3409.最长相邻绝对差递减子序列

[3409. 最长相邻绝对差递减子序列 - 力扣（LeetCode）](https://leetcode.cn/problems/longest-subsequence-with-decreasing-adjacent-difference/)

题目给出一个整数数组nums，其长度可以达到10^4，其中的元素值都在1到300之间。

现在要求从中找出一个最长的序列seq，满足seq中相邻项之间的差的绝对值是单调不增的，即abs(seq[0] - seq[1]) >\= abs(seq[1] - seq[2]) >\= ... >\= abs(seq[-2] - seq[-1])。

由于题目找需要考察的是相邻项间差的绝对值，想不出什么比较合理的贪心策略，因此在这里应该向动态规划的方向来考虑。同样是因为这个差的绝对值，在动态规划的状态表示中就应该出现当前子序列的最后一项，以及当前子序列最后两项差的绝对值，于是可以设计状态f[v][diff]表示对于当前遍历到的前缀中，以v为结尾且最后两项的绝对差为diff的子序列的最大长度。

对nums进行一趟遍历，对于当前遍历到的元素v，还需要遍历所有可能的diff，那么对于f[v][diff]，倒数第二项的值只能是v + diff或者v - diff，那么对于pre_v1 \= v + diff，就有

f[v][diff] \= max(f[v][diff], f[pre_v1][pre_diff] + 1)，其中pre_diff >\= diff

同样的，对于pre_v2 \= v - diff，就有

f[v][diff] \= max(f[v][diff], f[pre_v2][pre_diff] + 1)，其中pre_diff >\= diff

在这里如果直接枚举所有pre_diff的话，时间复杂度会比较吃紧。注意到这是一个后缀的最大值，于是可以令best[v][diff] \= max(f[v][diff], f[v][diff + 1], ..., f[v][300])，那么上面的式子就可以写成

f[v][diff] \= max(f[v][diff], best[pre_v1][diff] + 1)

以及

f[v][diff] \= max(f[v][diff], best[pre_v2][diff] + 1)

而对于best[v][diff]，则可以倒序遍历diff，使用max(best[v][diff], best[v][diff + 1], f[v][diff])来更新best[v][diff]。

全部计算完成后，遍历所有可能的v和diff，取最大的f[v][diff]即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def longestSubsequence(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        f = [[0] * 301 for _ in range(301)]
        best = [[0] * 301 for _ in range(301)]

        for diff in range(301):
            f[nums[0]][diff] = 1
            best[nums[0]][diff] = 1

        for v in nums[1:]:
            for diff in range(300):
                pre_v1 = v + diff
                if pre_v1 <= 300:
                    f[v][diff] = max(f[v][diff], best[pre_v1][diff] + 1)
                
                pre_v2 = v - diff
                if pre_v2 >= 1:
                    f[v][diff] = max(f[v][diff], best[pre_v2][diff] + 1)

            f[v][300] = 1
            best[v][300] = 1

            for diff in range(299, -1, -1):
                best[v][diff] = max(best[v][diff + 1], best[v][diff], f[v][diff])
        
        res = 0
        for v in range(1, 301):
            for diff in range(300):
                res = max(res, f[v][diff])
        
        return res
```
