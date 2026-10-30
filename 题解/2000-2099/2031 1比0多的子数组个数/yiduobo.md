---
title: "2031. 1比0多的子数组个数"
aliases: ["yiduobo的每日leetcode 2031.1比0多的子数组个数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/625233081"
zhihu_id: "625233081"
zhihu_title: "yiduobo的每日leetcode 2031.1比0多的子数组个数"
question_id: "2031"
question: "1比0多的子数组个数"
problem_url: "https://leetcode.cn/problems/count-subarrays-with-more-ones-than-zeros/"
created: "2023-04-27T02:28:56+08:00"
updated: "2023-04-27T02:28:56+08:00"
upvotes: 0
comments: 0
---

# 2031. 1比0多的子数组个数

> **[yiduobo的每日leetcode 2031.1比0多的子数组个数](https://zhuanlan.zhihu.com/p/625233081) · 知乎 · 2023-04-27 · 赞同 0**
> 力扣：[2031. 1比0多的子数组个数](https://leetcode.cn/problems/count-subarrays-with-more-ones-than-zeros/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

2031.1比0多的子数组个数

[力扣](https://leetcode.cn/problems/count-subarrays-with-more-ones-than-zeros/)

对于这类01计数的问题，一种常见的做法是将0视为-1，那么区间[l, r]的和就相当于区间中1的数量减去区间中0的数量，于是本题就转化成了找出所有区间和大于0的区间数量。

而对于区间和问题，通常则是利用前缀和相减来处理，于是本题进一步转化，变成了对于数组中的每个位置r，找出其左侧所有满足s[r] > s[l]的位置l的数量，这里的s数组表示前缀和。

对于这个问题，则可以一趟遍历，在计算前缀和的同时，利用树状数组来查询当前位置左侧有多少个前缀和小于当前的前缀和。

需要特别注意的是由于这里将0改成了-1，那么前缀和的取值范围就在-n到n之间，因此使用树状数组时需要将每个前缀和都额外加上n + 1。

最后附上python代码：

```python
class Solution(object):
    def subarraysWithMoreZerosThanOnes(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        f = [0] * (n + n + 2)
        mod = 10 ** 9 + 7

        def add(x):
            while x <= n + n + 1:
                f[x] += 1
                if f[x] >= mod:
                    f[x] -= mod
                x += x & -x

        def get(x):
            res = 0
            while x > 0:
                res += f[x]
                if res >= mod:
                    res -= mod
                x -= x & -x
            return res

        res = 0
        now = 0
        add(n + 1)
        for v in nums:
            if v == 0:
                now -= 1
            else:
                now += 1
            
            res += get(now + n)
            if res >= mod:
                res -= mod
            add(now + n + 1)
        
        return res
```
