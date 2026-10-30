---
title: "2336. 无限集中的最小数字"
aliases: ["yiduobo的每日leetcode 2236.无限集中的最小数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/559255777"
zhihu_id: "559255777"
zhihu_title: "yiduobo的每日leetcode 2236.无限集中的最小数字"
question_id: "2336"
question: "无限集中的最小数字"
problem_url: "https://leetcode.cn/problems/smallest-number-in-infinite-set/"
title_number_fixed: ["2236→2336"]
created: "2022-08-30T00:59:25+08:00"
updated: "2022-08-30T00:59:25+08:00"
upvotes: 0
comments: 0
---

# 2336. 无限集中的最小数字

> **[yiduobo的每日leetcode 2236.无限集中的最小数字](https://zhuanlan.zhihu.com/p/559255777) · 知乎 · 2022-08-30 · 赞同 0**
> 力扣：[2336. 无限集中的最小数字](https://leetcode.cn/problems/smallest-number-in-infinite-set/)
> 原文标题里的题号写作 2236，这里改成 2336：文章里的力扣链接是 smallest-number-in-infinite-set，也就是 2336

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2236.无限集中的最小数字

[力扣](https://leetcode.cn/problems/smallest-number-in-infinite-set/)

题目中每次取数操作都会将当前集合中的最小值拿走，那么一个自然的想法就是使用一个变量mi记录当前还未被拿走的数中的最小值。每次拿走当前的mi之后，mi + 1就成为了新的mi。

不过本题中还有一个加回操作，可能会影响到mi的迭代，因此在这里可以修改一下mi的定义，表示当前还从未被拿走过的数中的最小值，这样一来即使有加回操作，mi的迭代方式依然是不受影响的。

接下来需要考虑如何处理加回操作。由于加回的数是不一定的，为了高效取得其中的最小值，那么就需要使用一个堆back_heap来维护这些加回的数。另一方面，只有被拿走过，且还未被加回的数才能被加回，因此还需要使用一个集合back_set来储存当前已经被加回的数。

到了这里就有了大致的解法：

1、对于取数操作：

若back_heap不为空，那么答案必然是back_heap堆顶的元素back_heap[0]。这里的隐藏条件是因为加回的数都是被拿走过的数，那么这些数必然都是小于当前的mi的。此时需要将back_heap[0]弹出，同时将该元素从back_set中删除，然后再返回该元素。

反之，若加回的堆为空，那么答案就是mi。此时则需要将mi更新为mi + 1，然后返回mi。

2、对于加回操作：

加回操作没什么好说的。若加回的数小于当前的mi，同时也没有出现在back_set中，那么就将其加入到back_heap和back_set当中。

最后附上python代码：

```python
class SmallestInfiniteSet(object):

    def __init__(self):
        self.mi = 1
        self.back_heap = []
        self.back_set = set()

    def popSmallest(self):
        """
        :rtype: int
        """
        if not self.back_heap:
            res = self.mi
            self.mi += 1
        else:
            res = heapq.heappop(self.back_heap)
            self.back_set.remove(res)
        
        return res

    def addBack(self, num):
        """
        :type num: int
        :rtype: None
        """
        if num >= self.mi or num in self.back_set:
            return
        
        self.back_set.add(num)
        heapq.heappush(self.back_heap, num)

# Your SmallestInfiniteSet object will be instantiated and called as such:
# obj = SmallestInfiniteSet()
# param_1 = obj.popSmallest()
# obj.addBack(num)
```
