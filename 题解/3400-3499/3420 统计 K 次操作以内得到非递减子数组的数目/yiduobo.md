---
title: "3420. 统计K次操作以内得到非递减子数组的数目"
aliases: ["yiduobo的每日leetcode 3420.统计K次操作以内得到非递减子数组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/tree", "leetcode/queue", "leetcode/sliding-window", "leetcode/monotonic-queue", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/32988853826"
zhihu_id: "32988853826"
zhihu_title: "yiduobo的每日leetcode 3420.统计K次操作以内得到非递减子数组的数目"
question_id: "3420"
question: "统计 K 次操作以内得到非递减子数组的数目"
problem_url: "https://leetcode.cn/problems/count-non-decreasing-subarrays-after-k-operations/"
difficulty: "Hard"
rating: 2855
created: "2025-03-27T01:18:47+08:00"
updated: "2025-03-27T01:20:46+08:00"
upvotes: 2
comments: 0
---

# 3420. 统计K次操作以内得到非递减子数组的数目

> **[yiduobo的每日leetcode 3420.统计K次操作以内得到非递减子数组的数目](https://zhuanlan.zhihu.com/p/32988853826) · 知乎 · 2025-03-27 · 赞同 2**
> 力扣：[3420. 统计 K 次操作以内得到非递减子数组的数目](https://leetcode.cn/problems/count-non-decreasing-subarrays-after-k-operations/) · Hard · 灵茶山艾府：[两种 O(n) 方法：从左到右滑窗/从右到左滑窗+单调栈+单调队列（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3420.统计K次操作以内得到非递减子数组的数目

[3420. 统计 K 次操作以内得到非递减子数组的数目 - 力扣（LeetCode）](https://leetcode.cn/problems/count-non-decreasing-subarrays-after-k-operations/description/)

题目给出一个长度为n的数组nums以及一个整数k。

对于nums中的所有子数组，都可以对其执行至多k次操作，每次操作中可以将子数组中的任意元素加上1。注意，每个子数组都是互相独立的，也就是说对其中一个子数组的修改不会保留到另一个子数组中。

问有多少个子数组可以通过至多k次操作变为非递减的。

首先，如果固定子数组的起点start，那么数组终点end越大，需要的操作数量就越多。另一方面，如果起点在start的子数组最远可以扩展的终点为end，那么对于起点在start + 1的子数组而言，这些子数组最多可以扩展的终点必然大于等于end。也就是说，在这里使用滑动窗口来求解是很合适的。

接下来需要想办法计算窗口边界滑动时如何修正将窗口内子数组变为非递减所需的操作次数。

---

其中窗口右边界是比较好处理的。对于窗口右边界外的下一个元素nums[p]，只需对比nums[p]与当前窗口中最大元素ma的大小，若nums[p]较小，则需要一些操作将其补足到ma。而对于窗口内最大值这个问题，则只需使用一个堆来维护窗口中的元素就行了。

---

而对于窗口左边界的滑动，处理起来则比较麻烦，因为窗口中的部分元素之前补足到了左边界对应的元素，但是随着窗口的滑动，补足的操作数将会产生变化。

首先考虑计算移除nums[index]之后可以省去的操作数。对于nums[index]，不妨设其在数组中下一个更大的元素值为f[index]，这个f[index]可以通过单调栈来求解。

那么当f[index] > p时，说明窗口内所有的元素都小于等于nums[index]，也就是说这些元素都需要通过操作补足到nums[index]；而当f[index] \<\= p时，则说明窗口中从nums[index + 1]到f[index] - 1之间的元素都小于等于nums[index]，需要将这些元素补足到nums[index]。

方便起见，记bound \= min(f[index], p) - 1，那么之前为了补足到nums[index]消耗的操作数为

(nums[index] - nums[index + 1]) + (nums[index] - nums[index + 2]) + ... + (nums[index] - nums[bound])

将其中的nums[index]提出来，可以发现这是一个乘积减去一个区间和的形式，即为

nums[index] \* (bound - index) - (nums[index + 1] + nums[index + 2] + ... + nums[bound])

对于后面的部分，可以先计算nums的前缀和s，那么消耗的操作数为

nums[index] \* (bound - index) - (s[bound + 1] - s[index + 1])

接下来还需要考虑在移除nums[index]之后，其他元素在撤回之前的操作后还需要进行哪些操作才能保证数组非递减。根据上面计算出的bound的含义，可以发现bound之后的元素都没有修改的必要，因为这些元素本来就不是以之前的nums[index]为基准进行操作的，也就是说需要考虑的只有nums[index + 1]到nums[bound]这一段应该如何修改。

在这里可以先考察nums[index + 1]。对于nums[index + 1]而言，同样可以利用之前计算出来的f[index + 1]。与上面的做法类似，令right \= min(f[index + 1] - 1, bound)，那么对于nums[index + 2]到nums[right]之间的元素，现在都需要通过操作修正为nums[index + 1]，而修改的次数同样可以利用类似上面的式子进行计算，具体为nums[index + 1] \* (right - (index + 2) + 1)) - (s[right + 1] - s[index + 2])。

需要特别注意的是，在这里如果right + 1 \< bound，说明还有些元素并未得到修正，而下一个修正的基准为nums[right + 1]，可以按照上面相同的方法进行修正。当然在这里可能出现依然没有修正完的情况，于是只需不断向后迭代修正的基准，直到对应的right + 1大于等于bound为止。

上面修正的过程乍一看感觉是O(n)的，但是仔细分析可以发现，对于每个作为基准的下标，其只会在某一个特定下标被移除窗口时才会被作为基准来进行修正，换言之，这是一个树形结构，当窗口左边界被移出窗口时，相当于就树中某个节点删去，然后遍历其靠前的孩子节点的一部分作为新的修正基准。树中的每个节点只会被删去一次，也只会被作为基准一次，也就是说实际上这个过程是均摊O(1)的。

最后附上python代码：

```python
class Solution(object):
    def countNonDecreasingSubarrays(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        n = len(nums)
        f = [n] * n
        s = [0]
        stack = []
        heap = []
        removed = {}

        p = 0
        cost = 0
        res = 0
        for index, v in enumerate(nums):
            while p < n and (not heap or max(-heap[0] - nums[p], 0) + cost <= k):
                if heap:
                    cost += max(-heap[0] - nums[p], 0)
                heapq.heappush(heap, -nums[p])
                s.append(s[-1] + nums[p])

                while stack and nums[p] > nums[stack[-1]]:
                    f[stack.pop()] = p
                stack.append(p)

                p += 1

            res += p - index

            bound = min(f[index], p) - 1
            cost -= v * (bound - index)
            cost += s[bound + 1] - s[index + 1]

            left = index + 1
            while left < bound:
                right = min(f[left] - 1, bound)
                cost += nums[left] * (right - left)
                cost -= s[right + 1] - s[left + 1]
                left = right + 1
        
            removed[v] = removed.get(v, 0) + 1
            while heap and removed.get(-heap[0], 0) > 0:
                removed[-heap[0]] -= 1
                heapq.heappop(heap)

        return res
```
