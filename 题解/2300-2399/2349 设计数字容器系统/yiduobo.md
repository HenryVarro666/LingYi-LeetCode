---
title: "2349. 设计数字容器系统"
aliases: ["yiduobo的每日leetcode 2349.设计数字容器系统"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/ordered-set", "leetcode/simulation", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/561017372"
zhihu_id: "561017372"
zhihu_title: "yiduobo的每日leetcode 2349.设计数字容器系统"
question_id: "2349"
question: "设计数字容器系统"
problem_url: "https://leetcode.cn/problems/design-a-number-container-system/"
difficulty: "Medium"
rating: 1540
created: "2022-09-04T00:10:50+08:00"
updated: "2022-09-04T00:10:50+08:00"
upvotes: 0
comments: 0
---

# 2349. 设计数字容器系统

> **[yiduobo的每日leetcode 2349.设计数字容器系统](https://zhuanlan.zhihu.com/p/561017372) · 知乎 · 2022-09-04 · 赞同 0**
> 力扣：[2349. 设计数字容器系统](https://leetcode.cn/problems/design-a-number-container-system/) · Medium · 灵茶山艾府：[两种方法：有序集合 / 懒删除堆（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2349.设计数字容器系统

[力扣](https://leetcode.cn/problems/design-a-number-container-system/)

题目需要实现两种操作：

1、将某个下标置为指定的数字。

由于下标可达10^9，因此需要使用哈希表而不能直接使用数组下标。

2、给定数字，返回所有等于该数字的下标中的最小值。

由于是动态的最小值，那么第一想法就是使用堆来维护这些下标。在这里可以使用若干个堆，每个堆单独维护某一个特定数字的所有下标，那么堆顶自然就是要找的最小值了。

需要注意的是，由于题目可能出现替换操作，那么就需要将被替换掉的数对应的堆中删除当前下标。当然，在这里也可以懒处理，并不进行即时删除，而是当某次返回结果时，若返回的结果与哈希表中的记录不一致，那么说明当前这个值是应该被删除的，此时再进行删除。

最后附上python代码：

```python
class NumberContainers(object):

    def __init__(self):
        self.heap_dict = {}
        self.pos = {}

    def change(self, index, number):
        """
        :type index: int
        :type number: int
        :rtype: None
        """
        if self.pos.get(index, 0) == number:
            return
        
        if number not in self.heap_dict:
            self.heap_dict[number] = []

        self.pos[index] = number
        heapq.heappush(self.heap_dict[number], index)

    def find(self, number):
        """
        :type number: int
        :rtype: int
        """
        while number in self.heap_dict and self.heap_dict[number] and self.pos.get(self.heap_dict[number][0], 0) != number:
            heapq.heappop(self.heap_dict[number])
        
        if number in self.heap_dict and self.heap_dict[number]:
            res = self.heap_dict[number][0]
        else:
            res = -1
        
        return res

# Your NumberContainers object will be instantiated and called as such:
# obj = NumberContainers()
# obj.change(index,number)
# param_2 = obj.find(number)
```
