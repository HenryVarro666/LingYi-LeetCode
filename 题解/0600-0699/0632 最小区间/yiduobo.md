---
title: "632. 最小区间"
aliases: ["yiduobo的每日leetcode 632.最小区间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/sorting", "leetcode/sliding-window", "leetcode/heap-priority-queue", "题单/滑动窗口与双指针", "题单/常用数据结构", "题单/滑动窗口与双指针/二-不定长滑动窗口", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/270642726"
zhihu_id: "270642726"
zhihu_title: "yiduobo的每日leetcode 632.最小区间"
question_id: "632"
question: "最小区间"
problem_url: "https://leetcode.cn/problems/smallest-range-covering-elements-from-k-lists/"
difficulty: "Hard"
created: "2020-10-31T19:22:29+08:00"
updated: "2020-10-31T19:22:29+08:00"
upvotes: 0
comments: 0
---

# 632. 最小区间

> **[yiduobo的每日leetcode 632.最小区间](https://zhuanlan.zhihu.com/p/270642726) · 知乎 · 2020-10-31 · 赞同 0**
> 力扣：[632. 最小区间](https://leetcode.cn/problems/smallest-range-covering-elements-from-k-lists/) · Hard · 灵茶山艾府：[两种方法：堆/排序+滑动窗口（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

632.最小区间

[力扣](https://leetcode-cn.com/problems/smallest-range-covering-elements-from-k-lists/)

题目要求找出一个最短的区间，使得每个列表中至少有一个数在这个区间里面。

我们不妨先考虑一下这个问题的简化版：给出一个有序的数组，数组中的每个数有一个来源标记。要求从里面找出一个最短的区间，使得这个区间中的数包含了所有的来源。

这个简化的问题就可以用经典的滑动窗口来解决：

1、右边界不断往右扩展直到包含了所有的来源

2、不断缩减左边界直到不再包含所有来源，同时更新答案

3、重复步骤1和步骤2直到窗口扫完整个数组

回到原题。在这里，实际上就是右边界不再是简单的往右扩展，而是需要通过执行多路归并来获取到有序的序列，然后再往右扩展。左边界的缩减操作则维持不变。于是现在的做法为：

1、对k个列表执行多路归并，每次选出其中最小的一个数并加入到当前窗口中，直到窗口中包含了每个列表的数

2、不断缩减窗口的左边界直到不再包含所有列表，同时更新答案

3、重复步骤1和步骤2直到多路归并完成

最后附上python代码：

```python
import heapq

class Solution(object):
    def smallestRange(self, nums):
        """
        :type nums: List[List[int]]
        :rtype: List[int]
        """

        q = []
        heap = []
        pos_dict = {}
        cnt_dict = {}
        part_cnt = 0
        k = len(nums)
        l = r = 0
        res = None

        for index, part in enumerate(nums):
            heapq.heappush(heap, [part[0], index])
            pos_dict[index] = 1
            cnt_dict[index] = 0

        while heap:
            while heap and part_cnt < k:
                now, source = heap[0]

                while heap and heap[0][0] == now:
                    now, source = heapq.heappop(heap)
                    q.append([now, source])
                    r += 1
                    cnt_dict[source] += 1
                    if cnt_dict[source] == 1:
                        part_cnt += 1
                    if pos_dict[source] < len(nums[source]):
                        heapq.heappush(heap, [nums[source][pos_dict[source]], source])
                        pos_dict[source] += 1
            
            while l < r and part_cnt == k:
                if res is None or q[r - 1][0] - q[l][0] < res[1] - res[0]:
                    res = [q[l][0], q[r - 1][0]]
                remove_num = q[l][0]
                for remove_pos in range(l, r):
                    if q[remove_pos][0] != remove_num:
                        break
                if q[remove_pos][0] == remove_num:
                    remove_pos += 1
                for index in range(l, remove_pos):
                    cnt_dict[q[index][1]] -= 1
                    if cnt_dict[q[index][1]] == 0:
                        part_cnt -= 1
                
                l = remove_pos
        return res
```
