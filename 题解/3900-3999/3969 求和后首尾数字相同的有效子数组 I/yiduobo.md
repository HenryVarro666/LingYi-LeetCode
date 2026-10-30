---
title: "3969. 求和后首尾数字相同的有效子数组I & 3972. 求和后首尾数字相同的有效子数组II"
aliases: ["yiduobo的每日leetcode 3969.求和后首尾数字相同的有效子数组I && 3972.求和后首尾数字相同的有效子数组II", "3969. 求和后首尾数字相同的有效子数组I", "3972. 求和后首尾数字相同的有效子数组II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/number-theory", "leetcode/prefix-sum", "leetcode/sliding-window", "题单/常用数据结构", "题单/常用数据结构/一-前缀和", "leetcode/hard"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2052162548628295825"
zhihu_id: "2052162548628295825"
zhihu_title: "yiduobo的每日leetcode 3969.求和后首尾数字相同的有效子数组I && 3972.求和后首尾数字相同的有效子数组II"
question_id: ["3969", "3972"]
question: ["求和后首尾数字相同的有效子数组 I", "求和后首尾数字相同的有效子数组 II"]
problem_url: ["https://leetcode.cn/problems/valid-subarrays-with-matching-sum-digits-i/", "https://leetcode.cn/problems/valid-subarrays-with-matching-sum-digits-ii/"]
difficulty: ["Medium", "Hard"]
created: "2026-06-25T21:40:19+08:00"
updated: "2026-06-25T21:40:21+08:00"
upvotes: 2
comments: 0
---

# 3969. 求和后首尾数字相同的有效子数组I & 3972. 求和后首尾数字相同的有效子数组II

> **[yiduobo的每日leetcode 3969.求和后首尾数字相同的有效子数组I && 3972.求和后首尾数字相同的有效子数组II](https://zhuanlan.zhihu.com/p/2052162548628295825) · 知乎 · 2026-06-25 · 赞同 2**
> 力扣：[3969. 求和后首尾数字相同的有效子数组 I](https://leetcode.cn/problems/valid-subarrays-with-matching-sum-digits-i/) · Medium · 灵茶山艾府：[O(nlogS) 做法：前缀和 + 滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3972. 求和后首尾数字相同的有效子数组 II](https://leetcode.cn/problems/valid-subarrays-with-matching-sum-digits-ii/) · Hard · 灵茶山艾府：[前缀和 + 滑动窗口（Python/Java/C++/Go）](../3972%20求和后首尾数字相同的有效子数组%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3969.求和后首尾数字相同的有效子数组I

<https://leetcode.cn/problems/valid-subarrays-with-matching-sum-digits-i/>

3972.求和后首尾数字相同的有效子数组II

<https://leetcode.cn/problems/valid-subarrays-with-matching-sum-digits-ii/description/>

题目给出一个正整数数组nums以及一个整数x。

若nums中从left到right这一段子数组中的元素之和的最高位以及最低位都恰好等于x，那么就称这个子数组为有效子数组。

问nums中有效子数组的数目。

两题的题设相同，第二题的数据规模较大，nums长度可达10^5，其中元素在1到10^9之间，x在1到9之间。

对于子数组和相关的问题，一个自然的想法就是先拆分称前缀和问题再来看看。

一趟遍历，计算前缀和数组s。对于当前得到的s[index]，接下来需要计算其左侧有多少个前缀和满足s[index]与该前缀和之差的最高位和最低位都恰好等于x。

对于最低位是很容易计算的。最低位本质上就是一个整数模10的余数，因此在这里可以利用哈希表记录前缀模10的余数出现的次数，就能很快得到结果。

而对于最高位则不太好确定，不过好在本题中nums中全都是正整数，也就是说s必然是单调递增的。更进一步的，满足小于等于s[index] - x \* 10^k，同时大于s[index] - (x + 1) \* 10^k的元素在s中必然是连续的一段，同时随着index的向右移动，s[index]将逐渐增大，因此这一段也会跟着向右移动，也就是说在这里可以通过滑动窗口确定满足上面条件的左右边界。

之所以选择s[index] - x \* 10^k和s[index] - (x + 1) \* 10^k作为界，理由是使用s[index]减去其中的元素，得到的差必然在x\*10^k到(x + 1) \* 10^k - 1之间，即最高位恰好为x。

接下来，只需要结合上面关于最低位的讨论，使用哈希表维护窗口内所有元素模10的余数的数量，就可以通过在哈希表中查找s[index] % 10 - x出现的次数，确定子数组和的首尾恰好都为x的k + 1位数的数量了。

需要特别注意的是，这里只计算了k + 1位数的数量，理论上对于s[index]，需要计算子数组和首尾都恰好为x的1位数到length(s[index])位数的数量，因此在这里需要对每种数位分别维护一个滑动窗口以及哈希表。

最后附上python代码：

```python
class Solution(object):
    def countValidSubarrays(self, nums, x):
        """
        :type nums: List[int]
        :type x: int
        :rtype: int
        """

        n = len(nums)

        p10 = [1]
        while p10[-1] <= n * (10 ** 9):
            p10.append(p10[-1] * 10)

        m = len(p10)
        left = [0] * m
        right = [0] * m
        f = [[0] * 10 for _ in range(m)]
        s = [0]

        res = 0
        for v in nums:
            s.append(s[-1] + v)
            p = 0
            while p < m and p10[p] * x <= s[-1]:
                while s[-1] - s[right[p]] >= x * p10[p]:
                    f[p][s[right[p]] % 10] += 1
                    right[p] += 1
                while s[-1] - s[left[p]] >= (x + 1) * p10[p]:
                    f[p][s[left[p]] % 10] -= 1
                    left[p] += 1
                
                target = s[-1] % 10 - x
                if target < 0:
                    target += 10
                res += f[p][target]
                p += 1

        return res
```
