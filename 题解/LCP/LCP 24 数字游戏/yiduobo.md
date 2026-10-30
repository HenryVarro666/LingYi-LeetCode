---
title: "LCP 24. 数字游戏"
aliases: ["yiduobo的每日leetcode LCP24.数字游戏"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/math", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/五-堆-优先队列", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/573053023"
zhihu_id: "573053023"
zhihu_title: "yiduobo的每日leetcode LCP24.数字游戏"
question_id: "LCP 24"
question: "数字游戏"
problem_url: "https://leetcode.cn/problems/5TxKeK/"
difficulty: "Hard"
created: "2022-10-13T02:08:17+08:00"
updated: "2022-10-13T02:08:17+08:00"
upvotes: 0
comments: 0
---

# LCP 24. 数字游戏

> **[yiduobo的每日leetcode LCP24.数字游戏](https://zhuanlan.zhihu.com/p/573053023) · 知乎 · 2022-10-13 · 赞同 0**
> 力扣：[LCP 24. 数字游戏](https://leetcode.cn/problems/5TxKeK/) · Hard · 灵茶山艾府：[转换+中位数贪心+对顶堆（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP24.数字游戏

[力扣](https://leetcode.cn/problems/5TxKeK/)

题目给出一个数组nums，接下来对于nums的每个前缀，要求通过加1或者减1的操作将这个前缀变成x, x+ 1, x + 2, ...这种逐一递增的形式，问对于每个前缀需要的最少操作数是多少。

对于这个问题，首先可以将式子做一些变形。题目要求将nums[index]变为x + index，那么不妨在一开始就将nums[index]减去index，这样一来问题就变成了对于nums的各个前缀，分别找出一个整数x，将这个前缀都变为x所需的最少操作数是多少。

不妨考虑其中的某个前缀nums[0]到nums[p]。此时相当于给出了一个数组，需要找出一个整数x，使得 |nums[index] - x| 之和最小。这是一个经典的贪心问题，答案是应该将数组排序，然后选择正中间那个数作为最终的x。具体的证明可以将数组排序后，从外向内两个两个一组，论证x处于这两个数之间时的代价最小，从而推导出选择正中间的数作为x时整体的代价最小，在这里就不展开了。

当然，对于本题每次都进行排序是不现实的，不过之前也遇到过一个完全一样的题目，即295题数据流的中位数问题。在这里可以直接套用当时采用的大小堆做法，具体可以参考

[yiduobo：yiduobo的每日leetcode 295.数据流的中位数](https://zhuanlan.zhihu.com/p/157331072)

对于某个前缀，通过上面的做法得到目标x之后，还需要计算将数组中所有数变为x的代价。在这里可以进一步利用求解中位数时的两个堆。可以明确的是，储存较小值的堆first中数都小于等于x，而储存较大值的堆second中的数都大于等于x，那么就可以通过两个堆中整数之和，以及堆的大小直接计算出将所有整数都变为x的代价。

具体来说，设较小值堆中有p个数，和为s_first，较大值堆中有q个数，和为s_second，那么最终结果就是

(x - first[0]) + (x - first[1]) + ... + (x - first[p - 1]) + (second[0] - x) + (second[1] - x) + ... + (second[q - 1] - x) \= x \* p - s_first + s_second - x \* q

最后附上python代码：

```python
class Solution(object):
    def numsGame(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        n = len(nums)
        for index in range(n):
            nums[index] -= index
        
        first_heap = []
        second_heap = []
        s_first = 0
        s_second = 0
        res = []
        mod = 10 ** 9 + 7
        for num in nums:
            if not first_heap:
                if not second_heap:
                    heapq.heappush(second_heap, num)
                    s_second = num
                else:
                    if second_heap[0] < num:
                        min_of_second = heapq.heappop(second_heap)
                        s_second -= min_of_second
                        num, min_of_second = min_of_second, num
                        heapq.heappush(second_heap, min_of_second)
                        s_second += min_of_second
                    heapq.heappush(first_heap, -num)
                    s_first += num
            else:
                if num >= second_heap[0]:
                    if len(first_heap) < len(second_heap):
                        min_of_second = heapq.heappop(second_heap)
                        s_second -= min_of_second
                        heapq.heappush(first_heap, -min_of_second)
                        s_first += min_of_second
                    heapq.heappush(second_heap, num)
                    s_second += num

                elif num <= -first_heap[0]:
                    if len(first_heap) == len(second_heap):
                        max_of_first = heapq.heappop(first_heap)
                        s_first += max_of_first
                        heapq.heappush(second_heap, -max_of_first)
                        s_second -= max_of_first
                    heapq.heappush(first_heap, -num)
                    s_first += num

                else:
                    if len(first_heap) < len(second_heap):
                        heapq.heappush(first_heap, -num)
                        s_first += num
                    else:
                        heapq.heappush(second_heap, num)
                        s_second += num

            if len(second_heap) > len(first_heap):
                target = second_heap[0]
            else:
                target = (-first_heap[0] + second_heap[0]) / 2
            
            res.append((s_second - len(second_heap) * target + len(first_heap) * target - s_first) % mod)
        
        return res
```
