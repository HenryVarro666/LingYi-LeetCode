---
title: "2741. 特别的排列"
aliases: ["yiduobo的每日leetcode 2741.特别的排列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/bitmask", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/653405078"
zhihu_id: "653405078"
zhihu_title: "yiduobo的每日leetcode 2741.特别的排列"
question_id: "2741"
question: "特别的排列"
problem_url: "https://leetcode.cn/problems/special-permutations/"
difficulty: "Medium"
rating: 2021
created: "2023-08-31T02:24:34+08:00"
updated: "2023-08-31T02:24:34+08:00"
upvotes: 0
comments: 0
---

# 2741. 特别的排列

> **[yiduobo的每日leetcode 2741.特别的排列](https://zhuanlan.zhihu.com/p/653405078) · 知乎 · 2023-08-31 · 赞同 0**
> 力扣：[2741. 特别的排列](https://leetcode.cn/problems/special-permutations/) · Medium · 灵茶山艾府：[状压 DP：排列型 ② 相邻相关（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2741.特别的排列

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/special-permutations/description/)

如果将数组中的数视为图中的点，那么对于互为倍数关系的两个点，就可以在图中建立一条无向边，此时问题就变成了问图中哈密顿路径的数目。

对于这个问题，没有比较优美的处理方法，不过本题的数据规模不大，可以使用状态压缩动态规划来求解。

令f[state][last]表示由state中的点构成，最后一个节点为last的哈密顿路径的数目，那么对于f[state][last]，可以先通过state ^ (1 \<\< last)计算出上一轮的状态pre_state。若pre_state为0，说明f[state][last]只有last这唯一一个节点，于是有f[state][last] \= 1，否则就需要从枚举pre_state中的最后这个节点pre_last，要求满足pre_state | (1 \<\< pre_last) \= (1 \<\< pre_last)，那么就有f[state][last] +\= f[pre_state][pre_last]。

计算完成后，将f[(1 \<\< n) - 1]中的所有值累加起来即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def specialPerm(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        max_state = 1 << n
        f = [[0] * n for _ in range(max_state)]
        mod = 10 ** 9 + 7
        for state in range(1, max_state):
            for last in range(n):
                if state & (1 << last) == (1 << last):
                    pre_state = state ^ (1 << last)
                    if pre_state == 0:
                        f[state][last] = 1
                    else:
                        for pre_last in range(n):
                            if pre_state & (1 << pre_last) == (1 << pre_last) and (nums[last] % nums[pre_last] == 0 or nums[pre_last] % nums[last] == 0):
                                f[state][last] += f[pre_state][pre_last]
                                if f[state][last] >= mod:
                                    f[state][last] -= mod
        
        return sum(f[-1]) % mod
```
