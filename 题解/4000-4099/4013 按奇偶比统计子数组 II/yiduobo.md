---
title: "4011. 按奇偶比统计子数组I & 4013. 按奇偶比统计子数组II"
aliases: ["yiduobo的每日leetcode 4011.按奇偶比统计子数组I && 4013.按奇偶比统计子数组II", "4011. 按奇偶比统计子数组I", "4013. 按奇偶比统计子数组II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-indexed-tree", "leetcode/prefix-sum", "leetcode/merge-sort", "leetcode/hard", "leetcode/ordered-set", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2068824159480706198"
zhihu_id: "2068824159480706198"
zhihu_title: "yiduobo的每日leetcode 4011.按奇偶比统计子数组I && 4013.按奇偶比统计子数组II"
question_id: ["4011", "4013"]
question: ["按奇偶比统计子数组 I", "按奇偶比统计子数组 II"]
problem_url: ["https://leetcode.cn/problems/count-subarrays-with-even-odd-ratio-i/", "https://leetcode.cn/problems/count-subarrays-with-even-odd-ratio-ii/"]
difficulty: ["Medium", "Hard"]
rating: 2156
created: "2026-08-06T22:33:00+08:00"
updated: "2026-08-06T22:33:05+08:00"
upvotes: 1
comments: 0
---

# 4011. 按奇偶比统计子数组I & 4013. 按奇偶比统计子数组II

> **[yiduobo的每日leetcode 4011.按奇偶比统计子数组I && 4013.按奇偶比统计子数组II](https://zhuanlan.zhihu.com/p/2068824159480706198) · 知乎 · 2026-08-06 · 赞同 1**
> 力扣：[4011. 按奇偶比统计子数组 I](https://leetcode.cn/problems/count-subarrays-with-even-odd-ratio-i/) · Medium · 灵茶山艾府：[非暴力做法（Python/Java/C++/Go）](../4011%20按奇偶比统计子数组%20I/灵茶山艾府.md)
> 力扣：[4013. 按奇偶比统计子数组 II](https://leetcode.cn/problems/count-subarrays-with-even-odd-ratio-ii/) · Hard · 灵茶山艾府：[等价转化 + 前缀和 + 树状数组 / 归并排序（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4011.按奇偶比统计子数组I

<https://leetcode.cn/problems/count-subarrays-with-even-odd-ratio-i/description/>

4013.按奇偶比统计子数组II

<https://leetcode.cn/problems/count-subarrays-with-even-odd-ratio-ii/description/>

题目给出一个正整数数组nums，以及两个正整数a和b。

对于一个子数组，记其中偶数元素的数量为x，奇数元素的数量为y，那么当一个子数组满足：

- y > 0
- x / y \<\= a / b

就称这个子数组为有效子数组。这里的比较是精确的分数比较。

问nums中有效子数组的数量。

两题的题设相同，第二题的数据规模较大，数组长度可达10^5，其中元素的大小以及a和b的大小可达10^9。

基于题目中的数据规模，直接枚举所有子数组显然是不行的。

另一方面，对于这类问题可能可以使用滑动窗口。尝试固定数组的一端，随着另一端的移动，x / y并没有呈现出单调性，因此在这里使用滑动窗口也是不可行的。

比较常见的思路不可行，那么在这里不妨先关注这个比较的等式本身。分数的比较不是很方便，将其通分后可得bx \<\= ay时数组有效。更进一步的，若y为0且数组非空，这个式子显然不成立，因此实际上并不需要额外考虑y > 0这个条件。

接下来，对于bx \<\= ay这个式子，其中x对应的是子数组中偶数的数量，y对应的则是子数组中奇数的数量，那么一个自然的想法就是将nums中的所有偶数都替换为-b，所有奇数都替换为a，那么对于一个拥有x个偶数以及y个奇数的子数组，其子数组之和恰好就是ay - bx。换言之，子数组和大于等于0的子数组就是要找有效子数组。

到了这里，问题就转化成了如何计算数组中有多少个子数组的和大于等于0。对于这个问题，则可以先做进一步的转化。对于涉及到子数组和的问题，通常可以使用前缀和来提高计算效率。对于本题，对于转化后的nums计算前缀和数组s，接下来对于s中的某个下标index，若选择其为子数组的右边界，那么在这里实际上需要计算的就是0到index - 1之间有多少个前缀和小于等于s[index]。

可以发现，这实际上就是数组中非逆序对数量的问题，因此只需对s进行归并排序，在排序过程中顺便计算即可。

最后附上python代码：

```python
class Solution(object):
    def countRatioSubarrays(self, nums, a, b):
        """
        :type nums: List[int]
        :type a: int
        :type b: int
        :rtype: int
        """
        
        s = [0]
        for v in nums:
            if v % 2 == 0:
                s.append(s[-1] - b)
            else:
                s.append(s[-1] + a)
        
        def calc(left, right, s):
            if left == right:
                return 0
            
            mid = (left + right) // 2
            tot = calc(left, mid, s) + calc(mid + 1, right, s)
            tmp = []
            
            i, j = left, mid + 1
            while i <= mid and j <= right:
                if s[i] <= s[j]:
                    tot += right - j + 1
                    tmp.append(s[i])
                    i += 1
                else:
                    tmp.append(s[j])
                    j += 1
            
            tmp.extend(s[i: mid + 1])
            tmp.extend(s[j: right + 1])

            for index in range(left, right + 1):
                s[index] = tmp[index - left]
            return tot

        return calc(0, len(s) - 1, s)
```
