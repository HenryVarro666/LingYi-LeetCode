---
title: "2102. 序列顺序查询"
aliases: ["yiduobo的每日leetcode 2102.序列顺序查询"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/design", "leetcode/brainteaser", "leetcode/ordered-set", "leetcode/set", "leetcode/hong-hei-shu", "leetcode/ping-heng-shu", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/521690658"
zhihu_id: "521690658"
zhihu_title: "yiduobo的每日leetcode 2102.序列顺序查询"
question_id: "2102"
question: "序列顺序查询"
problem_url: "https://leetcode.cn/problems/sequentially-ordinal-rank-tracker/"
difficulty: "Hard"
rating: 2159
created: "2022-05-29T20:23:15+08:00"
updated: "2022-05-29T20:23:15+08:00"
upvotes: 0
comments: 0
---

# 2102. 序列顺序查询

> **[yiduobo的每日leetcode 2102.序列顺序查询](https://zhuanlan.zhihu.com/p/521690658) · 知乎 · 2022-05-29 · 赞同 0**
> 力扣：[2102. 序列顺序查询](https://leetcode.cn/problems/sequentially-ordinal-rank-tracker/) · Hard · 灵茶山艾府：[巧妙利用查询的特殊性](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2102.序列顺序查询

[力扣](https://leetcode.cn/problems/sequentially-ordinal-rank-tracker/)

题目相当于给出一个动态变化的数组和若干询问，要求找出第k次询问时数组中的第k大值是多少。这是一个典型的区间第k大值的问题，王道做法自然是平衡二叉树。

不过在这里k是从1开始逐1递增的，因此带来了操作的空间。使用一个变量记录下一次询问时k的大小，然后维护大小为k的小根堆top，其中储存了当前数组中最大的k个值，那么这个堆的堆顶就是当前所有值中第k大的，也就是下一次询问要求的值。当然，除了这k个值还可能有其他的值，因此需要额外使用一个大根堆rest来维护这些剩下的值。接下来：

1、对于插入操作：

1-1）若此时top中的元素少于k个，那么就直接将这个值插入到top中

1-2）若此时要插入的值大于top的堆顶元素，那么就top的堆顶弹出，并将当前值插入到top中，然后将top原来的堆顶插入到rest中

1-3）若不满足上面两种情况，就将当前值插入到rest中

2、对于询问操作：

首先根据top的定义，这次询问的结果就是top的堆顶元素。

询问过后，下一次询问的是第k + 1大的值，因此需要将k加上1。另一方面，此时top中的元素只有k个，需要新添加一个元素进来，那么若此时的rest不为空，则需要将rest中最大的值，也就是rest的堆顶调整到top中去。

需要注意的是，python原生的堆都是小顶堆，由于题目中还存在字符串的比价，因此通过取相反数来实现大顶堆的操作就不能用了，必须重载方法\_\_lt\_\_。

最后附上python代码：

```python
class Top(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score
    
    def __lt__(self, other):
        if self.score < other.score or (self.score == other.score and self.name > other.name):
            return True
        return False

class Rest(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score
    
    def __lt__(self, other):
        if self.score > other.score or (self.score == other.score and self.name < other.name):
            return True
        return False

class SORTracker(object):

    def __init__(self):
        self.top_heap = []
        self.rest_heap = []
        self.k = 1

    def add(self, name, score):
        """
        :type name: str
        :type score: int
        :rtype: None
        """

        if len(self.top_heap) < self.k:
            heapq.heappush(self.top_heap, Top(name, score))
        else:
            if score > self.top_heap[0].score or (score == self.top_heap[0].score and name < self.top_heap[0].name):
                heapq.heappush(self.top_heap, Top(name, score))
                min_top = heapq.heappop(self.top_heap)
                name, score = min_top.name, min_top.score
            
            heapq.heappush(self.rest_heap, Rest(name, score))

    def get(self):
        """
        :rtype: str
        """
        res = heapq.heappop(self.top_heap)
        heapq.heappush(self.top_heap, res)
        self.k += 1
        if self.rest_heap:
            max_rest = heapq.heappop(self.rest_heap)
            heapq.heappush(self.top_heap, Top(max_rest.name, max_rest.score))

        return res.name

# Your SORTracker object will be instantiated and called as such:
# obj = SORTracker()
# obj.add(name,score)
# param_2 = obj.get()
```
