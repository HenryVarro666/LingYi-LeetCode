---
title: "2992. 自整除排列的数量"
aliases: ["yiduobo的每日leetcode 2992.自整除排列的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/692469811"
zhihu_id: "692469811"
zhihu_title: "yiduobo的每日leetcode 2992.自整除排列的数量"
question_id: "2992"
question: "自整除排列的数量"
problem_url: "https://leetcode.cn/problems/number-of-self-divisible-permutations/"
created: "2024-04-15T02:44:58+08:00"
updated: "2024-04-15T02:44:58+08:00"
upvotes: 1
comments: 0
---

# 2992. 自整除排列的数量

> **[yiduobo的每日leetcode 2992.自整除排列的数量](https://zhuanlan.zhihu.com/p/692469811) · 知乎 · 2024-04-15 · 赞同 1**
> 力扣：[2992. 自整除排列的数量](https://leetcode.cn/problems/number-of-self-divisible-permutations/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2992.自整除排列的数量

[. - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-self-divisible-permutations/description/)

本题的数据规模很小，可以直接使用状态压缩动态规划来处理。令f[state]表示用state中的字符填充数组前p个位置的方案数，其中p是state中包含的1的数量。

对于f[state]，首先计算其中所有1的数量p，接下来枚举第p个位置填充的数字v。若state中包含1 \<\< v，且v和p的最大公约数为1，那么说明将v填充在p是合法的，即state可以从state ^ (1 \<\< v)转移过来，于是就有f[state] +\= f[state ^ (1 \<\< v)]。

最后附上python代码：

```python
class Solution(object):
    def selfDivisiblePermutationCount(self, n):
        """
        :type n: int
        :rtype: int
        """

        max_state = 1 << n
        f = [0] * max_state
        f[0] = 1

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        for state in range(1, max_state):
            p = 0
            for index in range(n):
                if state & (1 << index) == (1 << index):
                    p += 1
            
            for index in range(n):
                if state & (1 << index) == (1 << index) and gcd(index + 1, p) == 1:
                    f[state] += f[state ^ (1 << index)]
        
        return f[-1]
```
