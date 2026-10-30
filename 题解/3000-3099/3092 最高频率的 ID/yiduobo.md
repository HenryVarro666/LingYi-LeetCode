---
title: "3092. 最高频率的ID"
aliases: ["yiduobo的每日leetcode 3092.最高频率的ID"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/ordered-set", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/699300049"
zhihu_id: "699300049"
zhihu_title: "yiduobo的每日leetcode 3092.最高频率的ID"
question_id: "3092"
question: "最高频率的 ID"
problem_url: "https://leetcode.cn/problems/most-frequent-ids/"
difficulty: "Medium"
rating: 1793
created: "2024-05-23T00:18:07+08:00"
updated: "2024-05-23T00:18:07+08:00"
upvotes: 0
comments: 0
---

# 3092. 最高频率的ID

> **[yiduobo的每日leetcode 3092.最高频率的ID](https://zhuanlan.zhihu.com/p/699300049) · 知乎 · 2024-05-23 · 赞同 0**
> 力扣：[3092. 最高频率的 ID](https://leetcode.cn/problems/most-frequent-ids/) · Medium · 灵茶山艾府：[两种方法：哈希表+有序集合/懒删除堆（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3092.最高频率的ID

[. - 力扣（LeetCode）](https://leetcode.cn/problems/most-frequent-ids/description/)

题目给出一系列的id增减操作，问每次操作后当前频率最高的id是什么。

对于频率的增减，使用哈希表是非常合适的，而对于动态的询问最大值，则可以使用堆。不过在这里需要注意的是，在每次增减频率时，如果操作的id之前出现过，那么就需要先将之前的记录从堆中删掉再将新的记录加入到堆中，为了保证复杂度，在删除时就需要用到懒删除的技巧。

最后附上python代码：

```python
class Solution(object):
    def mostFrequentIDs(self, nums, freq):
        """
        :type nums: List[int]
        :type freq: List[int]
        :rtype: List[int]
        """

        heap = []
        res = []
        freq_dict = Counter()
        remove_dict = Counter()
        for v, f in zip(nums, freq):
            if freq_dict[v] > 0:
                remove_dict[(-freq_dict[v], v)] += 1

            while heap and remove_dict[heap[0]] > 0:
                remove_dict[heap[0]] -= 1
                heapq.heappop(heap)

            freq_dict[v] += f
            heapq.heappush(heap, (-freq_dict[v], v))
            if heap:
                res.append(-heap[0][0])
            else:
                res.append(0)
        
        return res
```
