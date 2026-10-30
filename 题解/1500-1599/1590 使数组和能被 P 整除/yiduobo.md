---
title: "1590. 使数组和能被P整除"
aliases: ["yiduobo的每日leetcode 1590.使数组和能被P整除"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/math", "leetcode/number-theory", "leetcode/prefix-sum", "题单/常用数据结构", "题单/数学算法", "题单/常用数据结构/一-前缀和", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/431428946"
zhihu_id: "431428946"
zhihu_title: "yiduobo的每日leetcode 1590.使数组和能被P整除"
question_id: "1590"
question: "使数组和能被 P 整除"
problem_url: "https://leetcode.cn/problems/make-sum-divisible-by-p/"
difficulty: "Medium"
rating: 2039
created: "2021-11-10T00:03:17+08:00"
updated: "2021-11-10T00:03:17+08:00"
upvotes: 0
comments: 0
---

# 1590. 使数组和能被P整除

> **[yiduobo的每日leetcode 1590.使数组和能被P整除](https://zhuanlan.zhihu.com/p/431428946) · 知乎 · 2021-11-10 · 赞同 0**
> 力扣：[1590. 使数组和能被 P 整除](https://leetcode.cn/problems/make-sum-divisible-by-p/) · Medium · 灵茶山艾府：[前缀和与哈希表（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1590.使数组和能被P整除

[力扣](https://leetcode-cn.com/problems/make-sum-divisible-by-p/)

题目要求从原数组中移除掉一个子数组，使得最终的数组之后是P的倍数。

首先还是考察边界情况。若原数组之和一开始就是P的倍数，那么也就没有必要移除掉子数组了，此时直接返回0即可。

接下来考虑一般情况。若原数组之和模P为t，那么被移除的子数组也必须满足模P等于t，那么此时问题就转化成了找出一个最短的子数组，使得这个子数组模P等于t。对于子数组取模相关的问题，使用前缀和配合哈希表就能很快求解出来。具体来说就是从前向后一趟扫描，对于当前位置index，不妨设此时的前缀和为s[index]，那么就需要找出index之前的某个位置pos，满足 (s[index] - s[pos - 1]) % P \= t。将这个式子转化一下，就变成了需要找出最靠后的，且模P余数为(s[index] - t + P) % P的位置pos。

由于这里模P的余数只有0到P - 1这一共P中情况，那么可以使用哈希表记录下来每种余数最后一次出现的位置，这样一来就可以在O(1)的时间内确定pos的位置了。确定了pos之后，pos + 1到index这一段子数组就是模P余t的子数组，其长度为index - pos，用这个数来更新答案即可。另外，若扫描完成后没有找到任何符合条件的子数组，那么答案就是-1。

最后附上python代码：

```python
class Solution(object):
    def minSubarray(self, nums, p):
        """
        :type nums: List[int]
        :type p: int
        :rtype: int
        """

        s = sum(nums)
        if s % p == 0:
            return 0
        
        target = s % p
        last_pos = {}
        last_pos[0] = -1
        now = 0
        res = len(nums)
        for index, num in enumerate(nums):
            now += num
            r = (now - target + p) % p
            if r in last_pos:
                res = min(res, index - last_pos[r])
            
            last_pos[now % p] = index
        
        if res == len(nums):
            res = -1
        
        return res
```
