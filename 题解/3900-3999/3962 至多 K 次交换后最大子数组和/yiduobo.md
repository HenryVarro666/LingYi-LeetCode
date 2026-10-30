---
title: "3962. 至少K次交换后最大子数组和"
aliases: ["yiduobo的每日leetcode 3962.至少K次交换后最大子数组和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/binary-indexed-tree", "leetcode/sorting", "leetcode/sliding-window", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2049540358065877447"
zhihu_id: "2049540358065877447"
zhihu_title: "yiduobo的每日leetcode 3962.至少K次交换后最大子数组和"
question_id: "3962"
question: "至多 K 次交换后最大子数组和"
problem_url: "https://leetcode.cn/problems/maximum-subarray-sum-after-at-most-k-swaps/"
difficulty: "Hard"
rating: 2672
created: "2026-06-15T22:04:14+08:00"
updated: "2026-06-15T22:04:17+08:00"
upvotes: 2
comments: 0
---

# 3962. 至少K次交换后最大子数组和

> **[yiduobo的每日leetcode 3962.至少K次交换后最大子数组和](https://zhuanlan.zhihu.com/p/2049540358065877447) · 知乎 · 2026-06-15 · 赞同 2**
> 力扣：[3962. 至多 K 次交换后最大子数组和](https://leetcode.cn/problems/maximum-subarray-sum-after-at-most-k-swaps/) · Hard · 灵茶山艾府：[值域树状数组 + 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3962.至少K次交换后最大子数组和

<https://leetcode.cn/problems/maximum-subarray-sum-after-at-most-k-swaps/>

题目给出一个长度为n的整数数组nums以及一个整数k，其中n不超过1500，k在0到n之间。

现在可以对数组执行至多k次交换操作，每次操作都可以选择其中任意两个下标并交换其对应的元素值。

问执行操作后可能得到的最大子数组和。

基于题目的数据规模，在这里可以考虑枚举所有可能的子数组，并考察这些子数组如何交换才能使得和最大。

首先枚举子数组的起点start，然后从start开始枚举子数组的终点。对于当前枚举到的index，最理想的情况自然是将nums[index]与外界最大的元素进行交换，不过这里有次数限制，因此需要考虑具体的交换方案：

交换的目标可以分为两类，分别为：

1、原来在子数组中，因为之前的某次交换被换出去了

2、原来就在子数组的外部

可以发现，对于第一类的元素，本次的交换实际上是不需要代价的。

具体来说，对于第一类的某个元素nums[p]，其必然是原本位于start到index - 1之间的某个q，在执行之前的某次交换操作时，从nums[q]被换到nums[p]去的。因此如果现在交换nums[index]与nums[p]，实际上就相当于交换了nums[index]与原来的nums[p]，这次交换的代价在上次交换的时候已经支付过了。

例如数组[2, 1, 5]，start为0：

- 当index为0时，nums[index]为2，此时应该与外部的5进行交换，得到[5, 1, 2]，消耗了一次交换的代价
- 当index为1时，nums[index]为1，此时应该与外部的2进行交换，得到[5, 2, 1]。需要注意，这里1和2的交换就是上面所说的第一类交换，与在原数组[2, 1, 5]的基础上直接交换1和5后得到[2, 5, 1]在子数组和的意义上与[5, 2, 1]是完全等价的。

反过来，对于第二类的元素就是实打实的需要代价了。

基于上面的讨论，就可以分别使用两个堆rest_heap和swap_heap，维护本来就在子数组外部的元素的最大值，以及因为之前某次交换操作被换出去的元素的最大值。为了方便交换，堆中需要储存二元组：处理记录数值之外，还需要记录该元素在数组中的下标。

初始情况下，所有元素都属于rest_heap，而swap_heap为空。另外，还需要使用一个变量cnt记录已经执行的操作的总代价，接下来对于当前的nums[index]：

1、先将nums[index]从对应的堆中移除：

若nums[index]处于swap_heap中，说明当前的nums[index]是经过之前的某次操作，从start到index - 1之间的某个位置交换过来的。当子数组扩展到index时，之前这次操作的代价应该不算数了，此时应该将cnt减去1，并将nums[index]从swap_heap中移除。

反之，则需要将nums[index]从rest_heap中移除，但是cnt不需要修改。

2、接下来先考虑与swap_heap中的元素交换：

基于上面的讨论，与swap_heap的中的元素交换不需要代价。只要swap_heap的堆顶元素比nums[index]大，就应该进行交换操作。交换后注意把原始的堆顶从swap_heap中弹出，然后将nums[index]加入其中。

3、最后考虑与rest_heap交换：

此时交换的前提是rest_heap的堆顶更大，同时cnt + 1小于等于k。若满足，则交换二者，需要注意此时是将原始的堆顶从rest_heap中弹出，但是需要将nums[index]加入到swap_heap中。

4、执行完成交换操作后，最后将确定下来的nums[index]累加到子数组和s当中，然后使用s更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxSum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        mi = min(nums)
        res = max(nums)

        ori_heap = [(-v, index) for index, v in enumerate(nums)] + [(1 - mi, -1)]
        heapq.heapify(ori_heap)

        for start in range(len(nums)):
            rest_heap = ori_heap[:]
            rest_dict = {index: v for index, v in enumerate(nums)}
            swap_heap = [(1 - mi, -1)]
            swap_dict = {}

            now = nums[:]
            cnt = 0
            s = 0

            for index in range(start, len(nums)):
                v = now[index]
                if index in swap_dict:
                    cnt -= 1
                    swap_dict.pop(index)
                else:
                    rest_dict.pop(index)

                while len(rest_heap) > 1 and rest_dict.get(rest_heap[0][1], None) != -rest_heap[0][0]:
                    heapq.heappop(rest_heap)
                while len(swap_heap) > 1 and swap_dict.get(swap_heap[0][1], None) != -swap_heap[0][0]:
                    heapq.heappop(swap_heap)

                swap_v, swap_index = swap_heap[0]
                swap_v = -swap_v
                if swap_v > v:
                    now[index], now[swap_index] = now[swap_index], now[index]
                    heapq.heappop(swap_heap)
                    swap_dict.pop(swap_index)
                    heapq.heappush(swap_heap, (-v, swap_index))
                    swap_dict[swap_index] = v
                    v = swap_v
                
                rest_v, rest_index = rest_heap[0]
                rest_v = -rest_v
                if rest_v > v and cnt + 1 <= k:
                    now[index], now[rest_index] = now[rest_index], now[index]
                    heapq.heappop(rest_heap)
                    rest_dict.pop(rest_index)
                    heapq.heappush(swap_heap, (-v, rest_index))
                    swap_dict[rest_index] = v
                    v = rest_v
                    cnt += 1

                s += v
                res = max(res, s)

        return res
```
