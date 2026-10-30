---
title: "4017. 数组中的峰值II"
aliases: ["yiduobo的每日leetcode 4017.数组中的峰值II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/segment-tree", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2071984809795117152"
zhihu_id: "2071984809795117152"
zhihu_title: "yiduobo的每日leetcode 4017.数组中的峰值II"
question_id: "4017"
question: "数组中的峰值 II"
problem_url: "https://leetcode.cn/problems/peaks-in-array-ii/"
difficulty: "Hard"
created: "2026-08-15T16:13:09+08:00"
updated: "2026-08-15T16:13:10+08:00"
upvotes: 1
comments: 0
---

# 4017. 数组中的峰值II

> **[yiduobo的每日leetcode 4017.数组中的峰值II](https://zhuanlan.zhihu.com/p/2071984809795117152) · 知乎 · 2026-08-15 · 赞同 1**
> 力扣：[4017. 数组中的峰值 II](https://leetcode.cn/problems/peaks-in-array-ii/) · Hard · 灵茶山艾府：[用分治思考，用线段树维护（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4017.数组中的峰值II

<https://leetcode.cn/problems/peaks-in-array-ii/description/>

题目给出一个长度为n的整数数组nums，以及一个二维整数数组queries。

对于一个子数组，若其中某个非边界位置上的元素值大于其相邻的两个元素值，那么就称其为峰值。若一个子数组的中存在至少一个峰值元素，那么就称其为峰值子数组。

现在要求处理以下两种查询：

- \[1, left\[index\], right\[index\]\]：要求计算所有左边界大于等于left\[index\]且右边界小于等于right\[index\]的子数组中，峰值子数组的数目。
- \[2, idx\[index\], val\[index\]\]：要求将nums\[idx\[index\]\]修改为val\[index\]。这次更新将影响后续的操作。

要求返回一个答案数组，记录所有的1类查询的结果。

对于一个left到right的子数组，不妨设其中存在的峰值按从左到右的顺序排列下来分别为p0、p1、...、pk，那么在这里不妨考虑以每种峰值为最右侧峰值的峰值子数组的数目：

- 首先是p0。此时子数组的左边界可以在left到p0 - 1之间，而右边界则需要处于p0 + 1到p1之间，因此峰值子数组的数目就是(p0 - left) \* (p1 - p0)
- 接下来是p1。此时子数组的左边界可以在left到p1 - 1之间，而右边界则需要处于p1 + 1到p2之间，因此峰值子数组的数目就是(p1 - left) \* (p2 - p1)
- ...
- 最后对于pk。此时子数组的左边界可以在left到pk - 1之间，而右边界则需要处于pk + 1到right之间，因此峰值子数组的数目就是(pk - left) \* (right - pk)

在left到right之间的峰值子数组的数目，就是以上各种情况的累加之和，即

(p0 - left) \* (p1 - p0) + (p1 - left) \* (p2 - p1) + ... + (pk - left) \* (right - pk)

对于这个式子，可以将左侧-left这一项提出来，有

-left \* (p1 - p0) - left \* (p2 - p1) - ... - left \* (right - pk) \= -left \* (p1 - p0 + p2 - p1 + ... + right - pk)

最终就得到了-left \* (right - p0)

而对于剩余的项，则为

p0 \* (p1 - p0) + p1 \* (p2 - p1) + ... + p[k-1] \* (pk - p[k-1]) + pk \* (right - pk)

综合上面-left有关的项，最终得到的就是

p0 \* (p1 - p0) + p1 \* (p2 - p1) + ... + p[k-1] \* (pk - p[k-1]) + pk \* (right - pk) - left \* (right - p0)

对于这个式子，可以利用线段树维护前面p0 \* (p1 - p0) + ... + p[k-1] \* (pk - p[k-1])这一段的结果，以及区间中最左侧以及最右侧的峰值下标p0和pk，就可以高效计算出left到right间的峰值子数组的数目了。

需要注意，以上形如p0 \* (p1 - p0)的项，都是在区间合并时，通过右侧区间的最左侧峰值，以及左侧区间的最右侧峰值计算得到的。在计算时需要特别注意，小区间中边界上的峰值在小区间中不应该算作峰值，但是合并时，左侧区间的右边界或者右侧区间的左边界可能有峰值存在，不能遗漏掉。

最后附上python代码：

```python
class Solution(object):
    def countOfPeaks(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        n = len(nums)
        peak = [False] * n

        for index in range(1, n - 1):
            peak[index] = (nums[index] > nums[index - 1] and nums[index] > nums[index + 1])

        f = [0] * (n * 4)
        first = [None] * (n * 4)
        last = [None] * (n * 4)

        def build(p, left, right):
            if left == right:
                if peak[left]:
                    first[p] = left
                    last[p] = left
                return

            mid = (left + right) // 2
            build(p * 2 + 1, left, mid)
            build(p * 2 + 2, mid + 1, right)
            
            f[p] = f[p * 2 + 1] + f[p * 2 + 2]
            if last[p * 2 + 1] is not None and first[p * 2 + 2] is not None:
                f[p] += last[p * 2 + 1] * (first[p * 2 + 2] - last[p * 2 + 1])
            
            if first[p * 2 + 1] is None:
                first[p] = first[p * 2 + 2]
            else:
                first[p] = first[p * 2 + 1]
            
            if last[p * 2 + 2] is None:
                last[p] = last[p * 2 + 1]
            else:
                last[p] = last[p * 2 + 2]
        
        def query(p, left, right, start, end):
            if start == left and right == end:
                return f[p], first[p], last[p]
            
            mid = (left + right) // 2
            if end <= mid:
                return query(p * 2 + 1, left, mid, start, end)
            elif start > mid:
                return query(p * 2 + 2, mid + 1, right, start, end)
            else:
                left_v, left_first, left_last = query(p * 2 + 1, left, mid, start, mid)
                right_v, right_first, right_last = query(p * 2 + 2, mid + 1, right, mid + 1, end)

                tot = left_v + right_v
                if left_last is not None and right_first is not None:
                    tot += left_last * (right_first - left_last)

                if left_first is None:
                    interval_first = right_first
                else:
                    interval_first = left_first

                if right_last is None:
                    interval_last = left_last
                else:
                    interval_last = right_last

                return tot, interval_first, interval_last
        
        def update(p, left, right, index):
            if left == right:
                if peak[index]:
                    first[p] = index
                    last[p] = index
                else:
                    first[p] = None
                    last[p] = None
                return    
            
            mid = (left + right) // 2
            if index <= mid:
                update(p * 2 + 1, left, mid, index)
            else:
                update(p * 2 + 2, mid + 1, right, index)
            
            f[p] = f[p * 2 + 1] + f[p * 2 + 2]
            if last[p * 2 + 1] is not None and first[p * 2 + 2] is not None:
                f[p] += last[p * 2 + 1] * (first[p * 2 + 2] - last[p * 2 + 1])
            
            if first[p * 2 + 1] is None:
                first[p] = first[p * 2 + 2]
            else:
                first[p] = first[p * 2 + 1]
            
            if last[p * 2 + 2] is None:
                last[p] = last[p * 2 + 1]
            else:
                last[p] = last[p * 2 + 2]
        
        build(0, 0, n - 1)

        res = []
        for q in queries:
            if q[0] == 1:
                tot, interval_first, interval_last = query(0, 0, n - 1, q[1], q[2])
                if interval_first is None:
                    res.append(0)
                elif interval_first == interval_last:
                    res.append((interval_first - q[1]) * (q[2] - interval_first))
                else:
                    res.append(tot + interval_last * (q[2] - interval_last) - q[1] * (q[2] - interval_first))
            
            else:
                pending = []
                nums[q[1]] = q[2]
                for index in range(q[1] - 1, q[1] + 2):
                    if index <= 0 or index >= n - 1:
                        continue
                    
                    ori = peak[index]
                    peak[index] = (nums[index] > nums[index - 1] and nums[index] > nums[index + 1])
                    if ori and not peak[index]:
                        update(0, 0, n - 1, index)
                    elif not ori and peak[index]:
                        pending.append(index)
                
                for index in pending:
                    update(0, 0, n - 1, index)
                
                nums[q[1]] = q[2]

        return res
```
