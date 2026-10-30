---
title: "480. 滑动窗口中位数"
aliases: ["yiduobo的每日leetcode 480.滑动窗口中位数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/sliding-window", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/246224986"
zhihu_id: "246224986"
zhihu_title: "yiduobo的每日leetcode 480.滑动窗口中位数"
question_id: "480"
question: "滑动窗口中位数"
problem_url: "https://leetcode.cn/problems/sliding-window-median/"
difficulty: "Hard"
created: "2020-09-15T21:23:53+08:00"
updated: "2020-09-15T21:23:53+08:00"
upvotes: 0
comments: 0
---

# 480. 滑动窗口中位数

> **[yiduobo的每日leetcode 480.滑动窗口中位数](https://zhuanlan.zhihu.com/p/246224986) · 知乎 · 2020-09-15 · 赞同 0**
> 力扣：[480. 滑动窗口中位数](https://leetcode.cn/problems/sliding-window-median/) · Hard · 灵茶山艾府：[295 题 + 懒删除堆（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

480.滑动窗口中位数<https://leetcode-cn.com/problems/sliding-window-median/>

这一题与之前做过的数据流的中位数（传送门在这里：[yiduobo：yiduobo的每日leetcode 295.数据流的中位数](https://zhuanlan.zhihu.com/p/157331072)）很像，同样可以使用平衡树或者大小堆来做。我在这里使用的是大小堆的方法，不过需要注意的是，这里随着窗口往右滑动，每次需要从堆中删除窗口左侧的数。目前python中的heapq似乎只支持删除堆顶元素，因此需要在删除元素之后自行维护。不过注意到这里两个堆中的元素数目是恒定的，因此可以通过记录堆中元素变化的数目来维护堆中元素的平衡，因此不需要立即删除某个元素，而是将其记录下来，直到其被推到堆顶时再一次性删除。

具体来说，当窗口往右移动时，需要从堆中移除左侧的元素，然后往堆中加入右侧的元素，那么有四种情况：

1、从小堆中移除元素，往小堆中加入元素

2、从大堆中移除元素，往大堆中加入元素

3、从小堆中移除元素，往大堆中加入元素

4、从大堆中一处元素，往小堆中加入元素

可以发现，前两种情况下堆中元素依然是平衡的，而对于情况3，需要将大堆的堆顶移动到小堆，对于情况4，需要将小堆的堆顶移动到大顶堆，这样一来就能保持堆中元素数量平衡了。

每完成一次移动，都需要检测两个堆的堆顶是否是要删除的元素，如果是，那么就将其从堆中pop出来。

最后附上python代码：

```python
import heapq

class Solution(object):
    def medianSlidingWindow(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[float]
        """

        min_heap = []
        max_heap = []

        for num in nums[:k]:
            heapq.heappush(min_heap, -num)

        for index in range(k / 2):
            heapq.heappush(max_heap, -min_heap[0])
            heapq.heappop(min_heap)

        res = []
        del_dict = {}
        for index in range(k, len(nums)):
            if k % 2 == 1:
                res.append(float(-min_heap[0]))
            else:
                res.append((max_heap[0] - min_heap[0]) / 2.0)
            del_num = nums[index - k]
            del_dict[del_num] = del_dict.get(del_num, 0) + 1

            delta = 0
            if max_heap and del_num >= max_heap[0]:
                delta = 1
            else:
                delta = -1

            add_num = nums[index]
            if max_heap and add_num >= max_heap[0]:
                heapq.heappush(max_heap, add_num)
                delta -= 1
            else:
                heapq.heappush(min_heap, -add_num)
                delta += 1
            
            if delta > 0:
                heapq.heappush(max_heap, -min_heap[0])
                heapq.heappop(min_heap)
            elif delta < 0:
                heapq.heappush(min_heap, -max_heap[0])
                heapq.heappop(max_heap)

            while max_heap and del_dict.get(max_heap[0], 0) > 0:
                del_dict[max_heap[0]] -= 1
                heapq.heappop(max_heap)

            while min_heap and del_dict.get(-min_heap[0], 0) > 0:
                del_dict[-min_heap[0]] -= 1
                heapq.heappop(min_heap)

        if k % 2 == 1:
            res.append(float(-min_heap[0]))
        else:
            res.append((max_heap[0] - min_heap[0]) / 2.0)

        return res
```
