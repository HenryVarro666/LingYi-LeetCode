---
title: "3555. 排序每个滑动窗口中最小的子数组"
aliases: ["yiduobo的每日leetcode 3555.排序每个滑动窗口中最小的子数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1909771892845417506"
zhihu_id: "1909771892845417506"
zhihu_title: "yiduobo的每日leetcode 3555.排序每个滑动窗口中最小的子数组"
question_id: "3555"
question: "排序每个滑动窗口中最小的子数组"
problem_url: "https://leetcode.cn/problems/smallest-subarray-to-sort-in-every-sliding-window/"
created: "2025-05-25T19:22:30+08:00"
updated: "2025-05-25T19:22:30+08:00"
upvotes: 0
comments: 0
---

# 3555. 排序每个滑动窗口中最小的子数组

> **[yiduobo的每日leetcode 3555.排序每个滑动窗口中最小的子数组](https://zhuanlan.zhihu.com/p/1909771892845417506) · 知乎 · 2025-05-25 · 赞同 0**
> 力扣：[3555. 排序每个滑动窗口中最小的子数组](https://leetcode.cn/problems/smallest-subarray-to-sort-in-every-sliding-window/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3555.排序每个滑动窗口中最小的子数组

[3555. 排序每个滑动窗口中最小的子数组 - 力扣（LeetCode）](https://leetcode.cn/problems/smallest-subarray-to-sort-in-every-sliding-window/description/)

题目给出一个整数数组nums以及一个整数k，现在要求对于每个长度为k的子数组，确定使得这个子数组有序所需排序的最短子段长度。如果子数组本身就有序，那么所需排序的最短子段长度为0。

在这里不会真的对子数组进行排序，只需要计算需要排序的子段长度。

对于一个起点位于index的子数组，其终点位于index + k - 1。对于这个子数组，需要对其中所有逆序对覆盖的部分进行排序才能使得整个子数组有序。不妨设子数组中最左侧逆序对的起点下标为start，最右侧逆序对的终点下标为end，那么需要排序的就是start到end这一段，其长度为end - start + 1。

接下来的问题就是如何确定每个子数组中最左侧逆序对的起点以及最右侧逆序对的终点。对于这个问题，不妨反过来思考：对于每个下标index，其可以成为哪些子数组中逆序对的起点，以及哪些子数组中逆序对的终点。

令f[index]表示数组中下一个小于nums[index]的下标，那么当且仅当子数组同时涵盖index以及f[index]这两个位置时，index才是逆序对的起点。由于题目固定了子数组的长度，因此只有当左边界大于等于f[index] - k + 1，同时小于等于index时，子数组才同时覆盖index以及f[index]这两个下标，那么index就是这些子数组中某个逆序对的起点。在这里可以使用一个数组mi_intervals记录这些信息，也就是将三元组(f[index] - k + 1, index, index)加入到mi_intervals中，表示index是起点在f[index] - k + 1到index之间的所有子数组中某个逆序对的起点。

同理，令g[index]表示数组中上一个大于nums[index]的下标，那么只有当左边界大于等于index - k + 1，同时小于等于g[index]时，子数组才同时覆盖g[index]以及index这两个下标，那么index就是这些子数组中某个逆序对的终点。在这里同样是使用一个数组ma_intervals记录这些信息，也就是就三元组(index - k + 1, g[index], index)加入到ma_intervals中，表示index是起点在index - k + 1到g[index]之间的所有子数组中某个逆序对的终点。

对于下一个更小的元素以及上一个更大的元素这个问题，可以正反各一趟遍历利用单调栈求解，这里就不展开了。

得到mi_intervals以及ma_intervals之后，问题就变成了静态的区间赋值，单点求最值的问题，可以排序后使用堆来求解。

以mi_intervals为例，先将mi_intervals中的三元组按照区间的起点从小到大进行排序，接下来从0开始遍历每个数组下标。对于当前遍历到的下标index，将mi_intervals中所有区间起点等于index的三元组中的区间终点以及逆序对起点加入到堆中，以逆序对起点为第一关键字。由于mi_intervals已经排过序了，因此随着index的增大，区间起点等于index的三元组在mi_intervals中的下标也是逐渐增大的，因此可以使用一个指针p指向mi_intervals中下一个待匹配三元组的下标，随着index的增大，p只需在上一轮的基础上进行比较并向后移动即可。

接下来，对于堆中记录的所有区间终点以及逆序对起点，先将区间终点小于index的二元组从堆中移除，若堆不为空，那么堆顶记录的逆序对起点就处于以index为起点的区间中最左侧的逆序对起点了。

最后附上python代码：

```python
class Solution(object):
    def minSubarraySort(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        
        n = len(nums)
        f = [None] * n
        stack = []
        for index in range(n):
            while stack and nums[stack[-1]] > nums[index]:
                f[stack.pop()] = index
            
            stack.append(index)
        
        g = [None] * n
        stack = []
        for index in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] < nums[index]:
                g[stack.pop()] = index
            
            stack.append(index)

        mi_intervals = []
        ma_intervals = []
        for index in range(n):
            if f[index] is not None:
                start = max(0, f[index] - k + 1)
                if start <= index:
                    mi_intervals.append([start, index, index])
        
            if g[index] is not None:
                start = max(0, index - k + 1)
                if start <= g[index]:
                    ma_intervals.append([start, g[index], index])

        mi_intervals.sort()
        ma_intervals.sort()
        mi_heap = []
        ma_heap = []
        mi = []
        ma = []
        p = 0
        q = 0
        for index in range(n):
            while p < len(mi_intervals) and mi_intervals[p][0] == index:
                heapq.heappush(mi_heap, (mi_intervals[p][2], mi_intervals[p][1]))
                p += 1
            
            while mi_heap and mi_heap[0][1] < index:
                heapq.heappop(mi_heap)
            
            if mi_heap:
                mi.append(mi_heap[0][0])
            else:
                mi.append(None)

            while q < len(ma_intervals) and ma_intervals[q][0] == index:
                heapq.heappush(ma_heap, (-ma_intervals[q][2], ma_intervals[q][1]))
                q += 1
            
            while ma_heap and ma_heap[0][1] < index:
                heapq.heappop(ma_heap)
            
            if ma_heap:
                ma.append(-ma_heap[0][0])
            else:
                ma.append(None)

        res = []
        for index in range(n - k + 1):
            if mi[index] is None:
                res.append(0)
            else:
                res.append(ma[index] - mi[index] + 1)
        
        return res
```
