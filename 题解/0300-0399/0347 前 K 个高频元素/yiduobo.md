---
title: "347. 前K个高频元素"
aliases: ["yiduobo的每日leetcode 347.前K个高频元素"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/bucket-sort", "leetcode/sorting", "题单/LeetCode-热题-100", "题单/LeetCode-热题-100/堆"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/163541377"
zhihu_id: "163541377"
zhihu_title: "yiduobo的每日leetcode 347.前K个高频元素"
question_id: "347"
question: "前 K 个高频元素"
problem_url: "https://leetcode.cn/problems/top-k-frequent-elements/"
difficulty: "Medium"
created: "2020-07-24T23:24:37+08:00"
updated: "2020-07-24T23:24:37+08:00"
upvotes: 0
comments: 0
---

# 347. 前K个高频元素

> **[yiduobo的每日leetcode 347.前K个高频元素](https://zhuanlan.zhihu.com/p/163541377) · 知乎 · 2020-07-24 · 赞同 0**
> 力扣：[347. 前 K 个高频元素](https://leetcode.cn/problems/top-k-frequent-elements/) · Medium · 灵茶山艾府：[桶排序，O(n) 线性做法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

347.前K个高频元素<https://leetcode-cn.com/problems/top-k-frequent-elements/submissions/>

题目要求时间复杂度优于nlogn，所以在这里不能直接运用排序来解决问题。由于这里只需要求前k个高频元素，于是很自然就想到了使用堆来解决问题。

于是具体做法为：

1、一趟扫描，统计每个元素出现的频率

2、若不同元素的个数正好等于k，那么返回所有的不同元素

3、否则就维护一个大小为k的小根堆，key为元素出现的频率。接下来一趟扫描，对于每个元素，如果其频率大于堆顶元素的频率，那么将堆顶元素弹出，并将当前元素加入到堆中。最后堆中所剩元素即为最后答案。

极端情况下，需要扫描n个元素，每次的代价为O(logk)，于是最终时间复杂度为O(nlogk)。当k等于n时，即为条件二的情况，此时将直接返回，因此总的时间复杂度一定优于nlogn。

最后附上python代码：

```python
import heapq

class Solution(object):
    def topKFrequent(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """

        weight_dict = {}
        for num in nums:
            weight_dict[num] = weight_dict.get(num, 0) + 1
        
        if k == len(weight_dict):
            return weight_dict.keys()

        heap = []
        for value, weight in weight_dict.items():
            if len(heap) == k:
                min_weight, min_value = heapq.heappop(heap)
                if min_weight > weight:
                    weight = min_weight
                    value = min_value
            heapq.heappush(heap, [weight, value])
            
        return [x[1] for x in heap]
```
