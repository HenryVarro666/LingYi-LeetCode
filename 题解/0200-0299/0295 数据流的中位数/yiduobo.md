---
title: "295. 数据流的中位数"
aliases: ["yiduobo的每日leetcode 295.数据流的中位数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/design", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/常用数据结构/五-堆-优先队列", "题单/LeetCode-热题-100/堆", "题单/面试经典-150-题/堆"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/157331072"
zhihu_id: "157331072"
zhihu_title: "yiduobo的每日leetcode 295.数据流的中位数"
question_id: "295"
question: "数据流的中位数"
problem_url: "https://leetcode.cn/problems/find-median-from-data-stream/"
difficulty: "Hard"
created: "2020-07-06T21:06:28+08:00"
updated: "2020-07-06T21:06:28+08:00"
upvotes: 0
comments: 0
---

# 295. 数据流的中位数

> **[yiduobo的每日leetcode 295.数据流的中位数](https://zhuanlan.zhihu.com/p/157331072) · 知乎 · 2020-07-06 · 赞同 0**
> 力扣：[295. 数据流的中位数](https://leetcode.cn/problems/find-median-from-data-stream/) · Hard · 灵茶山艾府：[如何自然引入大小堆？简洁写法！（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

295.数据流的中位数<https://leetcode-cn.com/problems/find-median-from-data-stream/>

乍一看感觉直接上平衡树可以解决，但是注意到实际上每次需要查找的只是当前数据结构中最中间的一个或者两个数，那么可以使用两个堆来解决。具体做法为维护两个堆，分别保存当前数据较大的n/2个数以及较小的n/2个数，分别称为大数堆和小数堆。

当n为偶数时，约定大数堆和小数堆中都有n/2个元素。

当n为奇数时，约定大数堆中为n/2 + 1，而小数堆中元素个数为n/2。

那么对于一次中位数的询问：

1、若n为奇数，那么答案就是第n/2 + 1大的数。已知小数堆中正好有n/2个数，那么第n/2 + 1大的数就是大数堆中最小的那个数min_of_max。

2、若n为偶数，那么答案就是第n/2大的数以及n/2 + 1大的数。同上，第n/2大的数正好就是小数堆中最大的数max_of_min，而n/2 + 1大的数则依然是大数堆中最小的数min_of_max。

这也是为什么要使用堆这种数据结构的原因。

查询的时候只需要判断元素个数以及获取堆顶元素，因此时间复杂度为O(1)。

接下来需要考虑当新来了一个数num时怎么办：

1、若大数堆以及小数堆中都没有元素，那么根据约定将其加入大数堆

2、若大数堆中有数，小数堆中没有，那么需要对比大数堆中最小的数min_of_max和num的大小。若num大于min_of_max，此时应该将num加入大数堆，而将min_of_max加入小数堆。

3‘若两个堆中都有数，那么就需要对比num，大数堆中最小的数min_of_max以及小数堆中最大的数max_of_min三个数的大小关系。这样做的理由是只有当num >\= min_of_max时，num才属于较大的那一部分；同理，只有当num \<\= max_of_min时，num才属于较大的那一部分。

由于max_of_min \<\= min_of_max，那么加入num后，可能出现三种大小关系：

1）num \<\= max_of_min \<\= min_of_max

若此时小数堆中元素数量等于大数堆中元素数量，为了n为奇数时的约定，则需要从小数堆中弹出max_of_min并将其加入大数堆。

然后将num加入小数堆。

2）max_of_min \<\= num \<\= min_of_max

此时num既可以加入小数堆，也可以加入大数堆。那么需要判断两个堆中元素数量是否相等。根据n为奇数时的约定，若相等，则将num加入大数堆中，否则将n加入小数堆中。

3）max_of_min \<\= min_of_max \<\= num

与情况1)类似，若此时小数堆中元素数量等于大数堆中元素数量，需要从大数堆中弹出min_of_max并将其加入小数堆。

然后将num加入大数堆。

新加入一个num最多需要三次堆操作，而堆的元素个数恒定为n/2，因此时间复杂度为O(logn)。

最后附上python代码：

```python
import heapq

class MedianFinder(object):

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.fisrt_heap = []
        self.second_heap = []

    def addNum(self, num):
        """
        :type num: int
        :rtype: None
        """
        if not self.fisrt_heap:
            if not self.second_heap:
                heapq.heappush(self.second_heap, num)
            else:
                if self.second_heap[0] < num:
                    min_of_second = heapq.heappop(self.second_heap)
                    num, min_of_second = min_of_second, num
                    heapq.heappush(self.second_heap, min_of_second)
                heapq.heappush(self.fisrt_heap, -num)
        else:
            if num >= self.second_heap[0]:
                if len(self.fisrt_heap) < len(self.second_heap):
                    min_of_second = heapq.heappop(self.second_heap)
                    heapq.heappush(self.fisrt_heap, -min_of_second)
                heapq.heappush(self.second_heap, num)
            elif num <= -self.fisrt_heap[0]:
                if len(self.fisrt_heap) == len(self.second_heap):
                    max_of_fisrt = heapq.heappop(self.fisrt_heap)
                    heapq.heappush(self.second_heap, -max_of_fisrt)
                heapq.heappush(self.fisrt_heap, -num)
            else:
                if len(self.fisrt_heap) < len(self.second_heap):
                    heapq.heappush(self.fisrt_heap, -num)
                else:
                    heapq.heappush(self.second_heap, num)

    def findMedian(self):
        """
        :rtype: float
        """
        if len(self.fisrt_heap) < len(self.second_heap):
            return self.second_heap[0]
        else:
            return (-self.fisrt_heap[0] + self.second_heap[0]) / 2.0

# Your MedianFinder object will be instantiated and called as such:
# obj = MedianFinder()
# obj.addNum(num)
# param_2 = obj.findMedian()
```
