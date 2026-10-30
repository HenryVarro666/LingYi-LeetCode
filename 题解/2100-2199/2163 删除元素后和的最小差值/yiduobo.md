---
title: "2163. 删除元素后和的最小差值"
aliases: ["yiduobo的每日leetcode 2163.删除元素后和的最小差值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/enumeration", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/五-堆-优先队列", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/532511133"
zhihu_id: "532511133"
zhihu_title: "yiduobo的每日leetcode 2163.删除元素后和的最小差值"
question_id: "2163"
question: "删除元素后和的最小差值"
problem_url: "https://leetcode.cn/problems/minimum-difference-in-sums-after-removal-of-elements/"
difficulty: "Hard"
rating: 2225
created: "2022-06-22T23:56:09+08:00"
updated: "2022-06-22T23:56:09+08:00"
upvotes: 0
comments: 0
---

# 2163. 删除元素后和的最小差值

> **[yiduobo的每日leetcode 2163.删除元素后和的最小差值](https://zhuanlan.zhihu.com/p/532511133) · 知乎 · 2022-06-22 · 赞同 0**
> 力扣：[2163. 删除元素后和的最小差值](https://leetcode.cn/problems/minimum-difference-in-sums-after-removal-of-elements/) · Hard · 灵茶山艾府：[前后缀分解 + 堆（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2163.删除元素后和的最小差值

[力扣](https://leetcode.cn/problems/minimum-difference-in-sums-after-removal-of-elements/)

首先，题目中的最小差值指的就是字面意义上差的最小值，而不是一般理解中的绝对值最小，因此在这里可以确定这是贪心法的题目。

为了使得答案最小，那么显然应该让前半部分的和最小，后半部分的和最大。由于两个部分不能交叉，那么可以认为题目实在n - 1到2n - 1之间选择了一个分割点cut_pos，然后从0到cut_pos这些数里面选出最小的n个数组成前半部分，从cut_pos + 1到3n - 1之间选出最大的n个数组成后半部分。

那么在这里一个自然的想法就是先计算出每种cut_pos对应的前半部分的最小和以及后半部分的最大和，然后枚举cut_pos并使用当前cut_pos对应的最小和以及最大和来更新答案。

对于计算最小和以及最大和的问题，实际上可以理解成给出对于初始的n个数，接下来有n个数依次过来，要求找出其中top n的问题。这个问题与之前遇到过的数据流中第n大值的问题本质上是一样的，那么也可以使用相同的方法求解。

以前半部分为例。首先使用一个大小为n的大根堆储存数组中的前n个数，记此时的和为now，那么当cut_pos为n - 1时对应的最小和就是now。接下来从n开始到2n - 1逐个枚举nums中的数。对于当前枚举到的nums[cut_pos]，若其比堆顶元素top要小，那么使用nums[cut_pos]来替代top显然可以让这些数的和更小，因此就应该将top弹出，并将nums[cut_pos]加入到堆中，同时更新now为now - top + nums[cut_pos]。反之，若其大于等于top，那么就没有替换的必要了，此时的now也不需要变动。

按同样的方法从后向前计算出后半部分每个cut_pos对应的最大和，然后遍历每个cut_pos，计算其对应的前半部分的最小和减去后半部分的最大和的差值并更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def minimumDifference(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums) / 3
        heap = []
        for num in nums[:n]:
            heapq.heappush(heap, -num)
        f = [-sum(heap)]
        for num in nums[n : n + n]:
            f.append(f[-1])
            if num < -heap[0]:
                f[-1] += num + heap[0]
                heapq.heappush(heap, -num)
                heapq.heappop(heap)

        heap = []
        for num in nums[-1 : -n - 1: -1]:
            heapq.heappush(heap, num)
        g = [sum(heap)]
        for num in nums[-n - 1: -n - n - 1: -1]:
            g.append(g[-1])
            if num > heap[0]:
                g[-1] += num - heap[0]
                heapq.heappush(heap, num)
                heapq.heappop(heap)
        g.reverse()

        res = f[0] - g[0]
        for index in range(1, n + 1):
            res = min(res, f[index] - g[index])
        
        return res
```
