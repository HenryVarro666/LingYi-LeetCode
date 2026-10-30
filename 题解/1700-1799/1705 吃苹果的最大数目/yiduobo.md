---
title: "1705. 吃苹果的最大数目"
aliases: ["yiduobo的每日leetcode 1705.吃苹果的最大数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/五-堆-优先队列", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/449195181"
zhihu_id: "449195181"
zhihu_title: "yiduobo的每日leetcode 1705.吃苹果的最大数目"
question_id: "1705"
question: "吃苹果的最大数目"
problem_url: "https://leetcode.cn/problems/maximum-number-of-eaten-apples/"
difficulty: "Medium"
rating: 1930
created: "2021-12-24T00:18:12+08:00"
updated: "2021-12-24T00:18:12+08:00"
upvotes: 0
comments: 0
---

# 1705. 吃苹果的最大数目

> **[yiduobo的每日leetcode 1705.吃苹果的最大数目](https://zhuanlan.zhihu.com/p/449195181) · 知乎 · 2021-12-24 · 赞同 0**
> 力扣：[1705. 吃苹果的最大数目](https://leetcode.cn/problems/maximum-number-of-eaten-apples/) · Medium · 灵茶山艾府：[吃最早腐烂的苹果（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1704.吃苹果的最大数目

[力扣](https://leetcode-cn.com/problems/maximum-number-of-eaten-apples/)

由于题目中的苹果都是由保质期的，为了吃到最多的苹果，显然应该先吃掉过期时间最早的苹果，那么一个自然的想法就是使用一个堆来维护当前剩下的苹果。

现在就有了一种做法：

从第1天开始向后枚举到第n天，对于第i天：

1、若apples\[i - 1\] > 0，那么说明第i天会有apples\[i - 1\]颗新苹果长出来，这些苹果的过期时间为i + days\[i - 1\]，于是应该将\[i + days\[i - 1\], apples\[i - 1\]\]这个二元组加入到堆中

2、接下来考察第i天能否吃到苹果。若此时堆不为空，且堆顶二元组中的过期日期小于等于i，说明堆顶表示的苹果已经过期了，应该将其从堆中弹出。重复此过程直到堆为空或者堆顶二元组的过期日期大于i。

若此时的堆不为空，那么说明第i天应该吃掉堆顶对应的苹果，此时应该将堆顶二元组中的苹果数量减去1，并将答案加上1。若减去1之后苹果数量依然大于0，那么就需要将这个二元组再重新加入到堆中

当处理完n天之后，此时堆中可能还有苹果，不过有一个好消息是由于没有新的苹果加入，因此在堆顶苹果全部吃完或者过期之前，是无需考虑堆中其他苹果的，因为其他苹果的过期时间必然是大于等于堆顶苹果的。

那么此时的做法如下：

与上面类似，若此时堆不为空，且堆顶二元组中的过期日期小于等于i，说明堆顶表示的苹果已经过期了，应该将其从堆中弹出。重复此过程直到堆为空或者堆顶二元组的过期日期大于i。

若堆不为空，说明堆顶的苹果还能吃。分别记过期时间和苹果数量为day和apple，那么又可以分为两种情况：

1、若当前日期date + apple - 1 \< day，说明从date开始每天吃掉一个苹果，一共需要apple天才能吃完堆顶的苹果，此时的日期来到了date + apple - 1。若这个日期小于day，说明这些苹果都没有过期，是可以这么吃的。此时应该更新date为date + apple，同时将答案加上apple

2、若当前日期date + apple - 1 >\= day，说明堆顶的有些苹果会来不及吃。那么反过来计算，从date到苹果过期的前一天，也就是day - 1之间一共有day - date天，因此可以吃day - date个苹果。此时应该更新date为day，同时将答案加上day - date。

无论哪种情况，堆顶的苹果就处理完了，也就无需再将其加回到堆中。

重复上面的操作，直到堆为空。

最后附上python代码：

```python
class Solution(object):
    def eatenApples(self, apples, days):
        """
        :type apples: List[int]
        :type days: List[int]
        :rtype: int
        """

        heap = []
        n = len(apples)
        res = 0
        for index in range(n):
            date = index + 1
            if apples[index] > 0:
                heapq.heappush(heap, [days[index] + date, apples[index]])

            while heap and heap[0][0] <= date:
                heapq.heappop(heap)

            if heap:
                day, apple = heapq.heappop(heap)
                res += 1
                apple -= 1
                if apple > 0:
                    heapq.heappush(heap, [day, apple])
                    
        date = n + 1
        while heap:
            while heap and heap[0][0] <= date:
                heapq.heappop(heap)
            
            if heap:
                day, apple = heapq.heappop(heap)
                if date + apple - 1 < day:
                    res += apple
                    date += apple
                else:
                    res += day - date
                    date = day
        
        return res
```
