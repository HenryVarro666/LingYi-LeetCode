---
title: "3362. 零数组变换III"
aliases: ["yiduobo的每日leetcode 3362.零数组变换III"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/two-pointers", "leetcode/sorting", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/二-差分", "题单/常用数据结构/五-堆-优先队列", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/27484340669"
zhihu_id: "27484340669"
zhihu_title: "yiduobo的每日leetcode 3362.零数组变换III"
question_id: "3362"
question: "零数组变换 III"
problem_url: "https://leetcode.cn/problems/zero-array-transformation-iii/"
difficulty: "Medium"
rating: 2424
created: "2025-03-03T00:05:10+08:00"
updated: "2025-03-03T00:05:23+08:00"
upvotes: 0
comments: 0
---

# 3362. 零数组变换III

> **[yiduobo的每日leetcode 3362.零数组变换III](https://zhuanlan.zhihu.com/p/27484340669) · 知乎 · 2025-03-03 · 赞同 0**
> 力扣：[3362. 零数组变换 III](https://leetcode.cn/problems/zero-array-transformation-iii/) · Medium · 灵茶山艾府：[贪心+最大堆+差分数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3362.零数组变换III

[3362. 零数组变换 III - 力扣（LeetCode）](https://leetcode.cn/problems/zero-array-transformation-iii/description/)

题目给出一个长度为n的整数数组nums和一个二维数组queries，其中queries\[i\] \=\[l\[i\], r\[i\]\]。对于每一个queries\[i\]，可以在l\[i\]到r\[i\]间任意选择一些下标，将nums中这些下标对应的元素减去1。

现在要求从queries中删去尽量多的元素，使得删除后的queries依然可以让nums变为全0。问最多可以删除多少个元素。若无法将nums变为全0，则返回-1。

之前3355题和3356题相同的queries和操作，但是题目需要计算的东西完全不同。本题要求从queries中删除尽量多的元素，且保证删除后queries任然可以使得nums变为全0，那么在这里就可以先思考是否存在贪心的解法。对于区间覆盖类的贪心，比较常见的做法是从边界情况入手分析，因为越靠近边界就越难被区间覆盖到，因此需要进行的抉择就更少，更容易发现贪心的策略。

对于本题，首先考虑nums[0]相关的情况。因为只有起点l[i] \= 0的queries[i]才有可能覆盖下标0，因此在这里就必须保留至少nums[0]个l[i] \= 0的区间。而对于这些保留的区间，很明显应该从所有l[i] \= 0的区间中，选出右边界最大的nums[0]个，因为这样的话可以使得后续下标位置所需的区间尽可能的少。

接下来对于nums[1]，不妨设之前选出的nums[0]个l[i] \= 0的区间中，有cnt个可以覆盖住下标1，那么还需要从所有之前未选择，且起点l[i] \<\= 1的区间中选出nums[1] - cnt个区间。同样的，这些区间的右边界应该尽量的大，且至少要求覆盖住下标1。

更进一步的，对于nums[index]，不妨设之前选出的区间中有cnt个可以覆盖住下标index，那么剩下的nums[index] - cnt个区间就需要从之前未选择，且起点l[i] \<\= index的区间中选出nums[index] - cnt个区间，这些区间必须至少覆盖住下标index，同时右边界尽可能的大。

这样一来，就得到了一种贪心的策略，接下来的问题就是如何高效维护cnt，以及如何高效选出右边界尽可能大的区间。

对于维护cnt的问题，可以照搬之前3355题和3356题的处理方法，利用差分数组来维护cnt。具体来说，使用一个数组f记录因为区间右边界闭合而带来的后缀减1，当首次遍历到某个下标index时，应该先让cnt减去f[index]，表示有f[index]个区间在index - 1闭合了，所以cnt中有f[index]个区间无法覆盖到下标index。而当新选择了某个区间覆盖index时，则应该将cnt加上1，同时将f中对应区间右边界加1的位置减去1。

而对于选择右边界尽可能大的区间这个问题，则可以使用一个堆来维护所有起点小于等于当前index，且还未被选择的区间，堆中用来排序的值自然是区间的右边界。

最后附上python代码：

```python
class Solution(object):
    def maxRemoval(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: int
        """
        
        n = len(nums)
        heap = []
        f = [0] * n
        cnt = 0
        res = len(queries)

        queries.sort()
        p = 0

        for index, v in enumerate(nums):
            while p < len(queries) and queries[p][0] == index:
                heapq.heappush(heap, -queries[p][1])
                p += 1

            cnt -= f[index]
            while cnt < v and heap and -heap[0] >= index:
                res -= 1
                cnt += 1
                if -heap[0] + 1 < n:
                    f[-heap[0] + 1] += 1
                heapq.heappop(heap)
            
            if cnt < v:
                return -1
        
        return res
```
