---
title: "3501. 操作后最大活跃区段数II"
aliases: ["yiduobo的每日leetcode 3501.操作后最大活跃区段数II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1901138792162792938"
zhihu_id: "1901138792162792938"
zhihu_title: "yiduobo的每日leetcode 3501.操作后最大活跃区段数II"
question_id: "3501"
question: "操作后最大活跃区段数 II"
problem_url: "https://leetcode.cn/problems/maximize-active-section-with-trade-ii/"
difficulty: "Hard"
rating: 2941
created: "2025-05-01T05:21:05+08:00"
updated: "2025-05-01T05:21:05+08:00"
upvotes: 1
comments: 0
---

# 3501. 操作后最大活跃区段数II

> **[yiduobo的每日leetcode 3501.操作后最大活跃区段数II](https://zhuanlan.zhihu.com/p/1901138792162792938) · 知乎 · 2025-05-01 · 赞同 1**
> 力扣：[3501. 操作后最大活跃区段数 II](https://leetcode.cn/problems/maximize-active-section-with-trade-ii/) · Hard · 灵茶山艾府：[区间最大值 + 分类讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3501.操作后最大活跃区段数II

[3501. 操作后最大活跃区段数 II - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-active-section-with-trade-ii/description/)

题目给出一个长度为n的二进制字符串s，其中'1'表示一个活跃区段，'0'则表示一个非活跃区段。

现在可以执行至多一次操作来最大化s中的活跃区段数目。在一次操作中，可以将一个被'0'包围的连续'1'全部变为'0'，再将一个被'1'包围的连续'0'全部变为'1'。

另外给出一个二维数组queries，其中queries\[index\] \= \[l\[index\], r\[index\]\]，表示子数组s\[l\[index\] : r\[index\] + 1\]。对于每个查询，需要确定这个子串在执行一次操作后最大活跃区段数。

需要注意，在处理时需要在s的两侧加上'1'，即t \= '1' + s + '1'，但是两侧的'1'不影响最终的计数，另外各个查询间相互独立。

之前3499题的升级版。

[yiduobo：yiduobo的每日leetcode 3499.操作后最大活跃区段数I](https://zhuanlan.zhihu.com/p/1899630240860448154)

本题从单次查询变成了多次查询，但是整体思路类似，依然是先分离连续的0和1，记录所有0的区间intervals。接下来对于每次查询，想办法找出查询区间内相邻0区间的最大长度之和。

对于单组查询[left, right]，可以先用left和right分别在intervals中进行二分，找出intervals中最左侧的满足intervals[p][1] >\= left的下标p，以及最右侧的满足intervals[q][0] \<\= right的下标q。

这样一来，对于本次查询[left, right]，将完整包含p + 1到q - 1之间的所有0区间，以及部分或者完整的区间p、q，是否为完整的intervals[p]取决于left是否小于等于intervals[p][0]，同理，是否为完整的intervals[q]则取决于right是否大于等于intervals[q][1]。

更进一步的，最长的相邻0区间的长度之和就可能出现：

1、区间p被包含在[left, right]之内的部分，加上区间p + 1被包含在[left, right]之内的部分。这里的前提条件是p \< q。在这里可以通过p的左边界与left中的较大值确定区间p被包含部分的左边界，同时通过p + 1的右边界与right中的较小值确定区间p + 1被包含部分的右边界。

2、区间q被包含在[left, right]之内的部分，加上区间q - 1被包含在[left, right]之内的部分。与情况1类似，也需要满足p \< q，被包含部分的计算方法也类似

3、p + 1到q - 1之间相邻区间长度之和。对于这个部分，由于这些区间长度是不会产生变化的，因此可以先对intervals进行一趟遍历，计算相邻区间长度之和，那么问题就变成了找出这个长度和数组的区间最大值。这是一个静态的区间最大值问题，可以使用st算法或者线段树来处理。我在这里使用的是线段树。

另外在具体计算时，需要在二分前注意判断p和q的各种边界情况，同时也不要忘了把本来就有的1的数量计入最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxActiveSectionsAfterTrade(self, s, queries):
        """
        :type s: str
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        n = len(s)

        intervals = []
        p = 0
        one = n
        while p < n:
            while p < n and s[p] == '1':
                p += 1
            
            if p == n:
                break
            
            q = p + 1
            while q < n and s[q] == '0':
                q += 1
            
            intervals.append((p, q - 1))
            one -= q - p
            p = q

        if not intervals:
            return [one] * len(queries)

        length = [0]
        for index in range(1, len(intervals)):
            length.append(intervals[index][1] - intervals[index][0] + 1 + intervals[index - 1][1] - intervals[index - 1][0] + 1)
        
        n = len(intervals)
        f = [0] * (n * 4)

        def build(p, start, end):
            if start == end:
                f[p] = length[start]
                return
            
            mid = (start + end) // 2
            build(p * 2 + 1, start, mid)
            build(p * 2 + 2, mid + 1, end)
            f[p] = max(f[p * 2 + 1], f[p * 2 + 2])
        
        def find(p, start, end, i, j):
            if start == i and end == j:
                return f[p]
            mid = (start + end) // 2
            if j <= mid:
                return find(p * 2 + 1, start, mid, i, j)
            elif i >= mid + 1:
                return find(p * 2 + 2, mid + 1, end, i, j)
            else:
                return max(find(p * 2 + 1, start, mid, i, mid), find(p * 2 + 2, mid + 1, end, mid + 1, j))

        build(0, 0, n - 1)

        res = []
        for left, right in queries:
            if left > intervals[-1][-1] or right < intervals[0][0]:
                res.append(one)
                continue
            
            lo = 0
            hi = len(intervals) - 1
            while lo < hi:
                mid = (lo + hi) // 2
                if intervals[mid][1] >= left:
                    hi = mid
                else:
                    lo = mid + 1

            p = lo

            lo = 0
            hi = len(intervals) - 1
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if intervals[mid][0] <= right:
                    lo = mid
                else:
                    hi = mid - 1
            
            q = hi

            best = 0
            if p + 2 <= q - 1:
                best = find(0, 0, n - 1, p + 2, q - 1)
            if q > p:
                best = max(best, min(intervals[p + 1][1], right) - intervals[p + 1][0] + 1 + intervals[p][1] - max(intervals[p][0], left) + 1)
                best = max(best, intervals[q - 1][1] - max(intervals[q - 1][0], left) + 1 + min(intervals[q][1], right) - intervals[q][0] + 1)
            
            res.append(one + best)
        
        return res
```
