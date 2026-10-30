---
title: "703. 数据流中的第K大元素"
aliases: ["yiduobo的每日leetcode 703.数据流中的第K大元素"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/320136208"
zhihu_id: "320136208"
zhihu_title: "yiduobo的每日leetcode 703.数据流中的第K大元素"
question_id: "703"
question: "数据流中的第K大元素"
problem_url: "https://leetcode.cn/problems/kth-largest-element-in-a-stream/"
created: "2020-11-29T18:48:40+08:00"
updated: "2020-11-29T18:48:40+08:00"
upvotes: 0
comments: 0
---

# 703. 数据流中的第K大元素

> **[yiduobo的每日leetcode 703.数据流中的第K大元素](https://zhuanlan.zhihu.com/p/320136208) · 知乎 · 2020-11-29 · 赞同 0**
> 力扣：[703. 数据流中的第K大元素](https://leetcode.cn/problems/kth-largest-element-in-a-stream/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

703.数据流中的第K大元素

[力扣](https://leetcode-cn.com/problems/kth-largest-element-in-a-stream/)

对于第k大或者第k小这类问题，经典的做法就是维护一个大小为k的堆来储存当前前k大或者前k小的元素。

回到题目，对于每一个新来的元素：

1、若当前堆的大小不到k，那么将新来的元素加入到堆中

2、若当前堆的大小等于k，且堆顶元素小于当前元素，此时应该将堆顶元素弹出，然后将当前元素加入到堆中

3、其他情况下则不进行任何操作

每一轮操作过后，若当前堆中的元素有k个，那么其堆顶元素就是当前第k大元素。

最后附上python代码：

```python
import heapq
class KthLargest(object):

    def __init__(self, k, nums):
        """
        :type k: int
        :type nums: List[int]
        """
        self.heap = nums[:k]
        self.k = k
        heapq.heapify(self.heap)
        for index in range(k, len(nums)):
            if self.heap[0] < nums[index]:
                heapq.heappop(self.heap)
                heapq.heappush(self.heap, nums[index])

    def add(self, val):
        """
        :type val: int
        :rtype: int
        """
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, val)
        elif self.heap[0] < val:
            heapq.heappop(self.heap)
            heapq.heappush(self.heap, val)
        
        return self.heap[0]

# Your KthLargest object will be instantiated and called as such:
# obj = KthLargest(k, nums)
# param_1 = obj.add(val)
```
