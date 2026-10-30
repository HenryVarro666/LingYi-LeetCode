---
title: "3049. 标记所有下标的最早秒数II"
aliases: ["yiduobo的每日leetcode 3049.标记所有下标的最早秒数II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/binary-search", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/五-堆-优先队列", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/696471195"
zhihu_id: "696471195"
zhihu_title: "yiduobo的每日leetcode 3049.标记所有下标的最早秒数II"
question_id: "3049"
question: "标记所有下标的最早秒数 II"
problem_url: "https://leetcode.cn/problems/earliest-second-to-mark-indices-ii/"
difficulty: "Hard"
rating: 3111
created: "2024-05-08T04:18:39+08:00"
updated: "2024-05-08T04:18:39+08:00"
upvotes: 0
comments: 0
---

# 3049. 标记所有下标的最早秒数II

> **[yiduobo的每日leetcode 3049.标记所有下标的最早秒数II](https://zhuanlan.zhihu.com/p/696471195) · 知乎 · 2024-05-08 · 赞同 0**
> 力扣：[3049. 标记所有下标的最早秒数 II](https://leetcode.cn/problems/earliest-second-to-mark-indices-ii/) · Hard · 灵茶山艾府：[二分答案+反悔贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3049.标记所有下标的最早秒数II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/earliest-second-to-mark-indices-ii/description/)

上一题的加强版。本题中依然可以随时执行减1操作，也可以跳过这一轮，另一方面，标记操作也改成了可以随时执行，还新增了一种归零操作，归零操作的执行时机则受到changeIndices约束，依然是问最早可以标记所有下标的时间。

首先，由于本题还是有跳过这一轮的操作，依然满足二分的条件，因此还是可以二分最早可以满足条件的时间mid。mid的下界和上界还是可以取0和changeIndices的长度m。

接下来，由于本题中的标记操作可以随时进行，那么就应该尽量将标记操作安排到操作序列的后面。反之，归零操作则应该尽量靠前执行，因为必须预留足够的时间给标记操作。更进一步的，对于操作序列的任意后缀，其中归零操作的次数都不应该大于标记操作的次数，这样的话就说明出现了无效的归零操作。

另一方面，归零操作不应该对nums本来就为0的下标执行，因为这样相当于浪费了一次操作。

根据上面的结论，就可以先从0到mid遍历changeIndices，对于当前遍历到的changeIndices[index]，若其对应的nums中的数值大于0，且当前下标出现，那么就将index，也就是归零的时机记录到集合first_index_set中。

接下来使用两个变量mark和need_minus，分别表示当前已标记的下标数量以及当前还需要执行减1操作的次数，其中mark初始化为0，need_minus则初始化为在mid内不存在归零操作的nums数值之和，然后从mid开始向前进行一趟遍历，对于当前遍历到的时机index：

1、若index出现在first_index_set中：

此时的index是执行归零操作的时机，需要优先考虑执行。但是有一个问题就是归零操作的次数太多，超出了mark，那么就应该将其中某次归零操作替换为mark操作，同时让这次归零操作通过减1操作来替代。为了最终代价最小，此时就应该将当前归零操作中对应的nums中最小的那一个替换成mark，这是一个动态的最小值问题，可以使用一个堆来处理。

那么对于这种情况，就应该先将当前归零操作对应的nums值添加到堆中。若堆的大小大于mark，就需要将堆顶对应的归零操作替换成mark，此时应该将mark加上1，同时将need_minus加上堆顶元素，然后将堆顶元素弹出。

2、若index没有出现在first_index_set中，且mark小于nums的长度n：

此时就应该执行标记操作，将mark加上1。

3、以上情况都不满足：

此时则应该执行减1操作，将need_minus减去1。

遍历完成后，若mark小于n，即没有足够的标记时间，又或者need_minus大于0，也就是减1操作的次数不过，那么说明无法标记，此时就应给更新二分的下界为mid + 1，否则更新二分的上界为mid。

最后附上python代码：

```python
class Solution(object):
    def earliestSecondToMarkIndices(self, nums, changeIndices):
        """
        :type nums: List[int]
        :type changeIndices: List[int]
        :rtype: int
        """

        m = len(changeIndices)
        n = len(nums)

        left = 0
        right = m
        while left < right:
            mid = (left + right) // 2
            vis = set()
            first_index_set = set()
            for index in range(mid + 1):
                if nums[changeIndices[index] - 1] > 0 and changeIndices[index] - 1 not in vis:
                    vis.add(changeIndices[index] - 1)
                    first_index_set.add(index)

            mark = 0
            need_minus = 0

            for index in range(n):
                if index not in vis:
                    need_minus += nums[index]

            heap = []
            for index in range(mid, -1, -1):
                if index in first_index_set:
                    heapq.heappush(heap, nums[changeIndices[index] - 1])

                    if len(heap) > mark:
                        mark += 1
                        need_minus += heapq.heappop(heap)
                
                elif mark < n:
                    mark += 1
                else:
                    need_minus -= 1

            if mark != n or need_minus > 0:
                left = mid + 1
            else:
                right = mid
        
        if left == m:
            return -1
        
        return left + 1
```
