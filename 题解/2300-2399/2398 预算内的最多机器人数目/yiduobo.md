---
title: "2398. 预算内的最多机器人数目"
aliases: ["yiduobo的每日leetcode 2398.预算内的最多机器人数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/array", "leetcode/sliding-window", "leetcode/monotonic-queue", "题单/常用数据结构", "题单/常用数据结构/四-队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/566904489"
zhihu_id: "566904489"
zhihu_title: "yiduobo的每日leetcode 2398.预算内的最多机器人数目"
question_id: "2398"
question: "预算内的最多机器人数目"
problem_url: "https://leetcode.cn/problems/maximum-number-of-robots-within-budget/"
difficulty: "Hard"
rating: 1917
created: "2022-09-22T01:10:54+08:00"
updated: "2022-09-22T01:10:54+08:00"
upvotes: 1
comments: 0
---

# 2398. 预算内的最多机器人数目

> **[yiduobo的每日leetcode 2398.预算内的最多机器人数目](https://zhuanlan.zhihu.com/p/566904489) · 知乎 · 2022-09-22 · 赞同 1**
> 力扣：[2398. 预算内的最多机器人数目](https://leetcode.cn/problems/maximum-number-of-robots-within-budget/) · Hard · 灵茶山艾府：[O(n) 做法：单调队列（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2398.预算内的最多机器人数目

[力扣](https://leetcode.cn/problems/maximum-number-of-robots-within-budget/)

题目给出充电时间和运行开销两个数组，要求找出一个区间，满足运行开销中对应子区间之和乘以区间长度，再加上充电时间对应子区间中的最大值得到的结果小于等于budget。

对于数组中的某个位置l，设其作为最长的合法子区间的左边界时，其对应的右边界为r，那么就有三种情况：

1、l因为充电时间太长，天然就无法加入到区间中，此时r不存在

2、l自己加入区间后无法加入其他机器人，即对应的区间为[l, l]，此时r \= l

3、l可以连通后续一些机器人一起加入到区间中，即r > l

在这里不妨分析对于l' \= l + 1而言，当l'作为左边界是对应的右边界r'位置：

1、当l对应的r不存在时，l'对应的r'就必须从l'，也就是l + 1开始找起

2、当l对应的r就等于l时，l'对应的r'同样需要从l + 1开始找起

3、当l对应的r > l时，说明l'\= l + 1是被包含在[l, r]中的，那么以l'为左边界对应的r'至少就可以选择r，因为这样一来无论是充电数组的区间最大值，还是运行开销数组的区间和以及区间长度都是有所减小的，因此必然满足总花销小于等于budget的条件，因此在这类l'对应的r'可以从r开始往后找

综合上面说的三种情况可知，当上一轮对应的r \<\= l时，当前这一轮的r'就应该从l' \= l + 1开始向后找，否则就直接从上一轮的r开始向后找。这样一来，就可以在一趟遍历的时间内找出所有l对应的r，并通过l和r形成的区间长度来更新答案。

接下来的问题就变成了如何高效计算组成总花销的两个部分。其中运行开销数组区间和这一项是比较好处理的，在知道了区间左右边界的情况下，可以直接计算区间长度，同时利用前缀和也可以高效计算出区间和。而对于充电时间区间的最大值，则可以使用类似之前遇到过的滑动窗口最大值的做法，使用一个堆来维护区间中的最大值。

[yiduobo：yiduobo的每日leetcode 239.滑动窗口最大值](https://zhuanlan.zhihu.com/p/150719702)

需要注意的是，这里有一些区别是滑动窗口最大值是定长滑动窗口，进出堆的时机是固定的，而对于本题，某个值是否能进入堆都是不确定的，因此还需要额外使用哈希表记录哪些位置在堆中，而弹出时也需要根据这个来进行操作，防止误删其他位置的数。

最后附上python代码：

```python
class Solution(object):
    def maximumRobots(self, chargeTimes, runningCosts, budget):
        """
        :type chargeTimes: List[int]
        :type runningCosts: List[int]
        :type budget: int
        :rtype: int
        """

        heap = []
        remove_dict = {}
        s = [runningCosts[0]]
        for cost in runningCosts[1:]:
            s.append(s[-1] + cost)
        
        n = len(chargeTimes)
        in_heap = set()
        r = 0
        res = 0
        for index in range(n):
            r = max(index, r)
            while r < n:
                while heap and remove_dict.get(-heap[0], 0) > 0:
                    remove_dict[-heap[0]] -= 1
                    heapq.heappop(heap)
                
                cost = chargeTimes[r]
                if heap:
                    cost = max(-heap[0], cost)

                cost += s[r] * (r - index + 1)
                if index > 0:
                    cost -= s[index - 1] * (r - index + 1)

                if cost <= budget:
                    heapq.heappush(heap, -chargeTimes[r])
                    in_heap.add(r)
                    r += 1
                else:
                    break

            res = max(res, r - index)
            if index in in_heap:
                remove_dict[chargeTimes[index]] = remove_dict.get(chargeTimes[index], 0) + 1

        return res
```
