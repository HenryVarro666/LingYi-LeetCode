---
title: "3679. 使库存平衡的最少丢弃次数"
aliases: ["yiduobo的每日leetcode 3679.使库存平衡的最少丢弃次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1953190688586957164"
zhihu_id: "1953190688586957164"
zhihu_title: "yiduobo的每日leetcode 3679.使库存平衡的最少丢弃次数"
question_id: "3679"
question: "使库存平衡的最少丢弃次数"
problem_url: "https://leetcode.cn/problems/minimum-discards-to-balance-inventory/"
difficulty: "Medium"
rating: 1639
created: "2025-09-23T23:38:09+08:00"
updated: "2025-09-23T23:38:09+08:00"
upvotes: 0
comments: 0
---

# 3679. 使库存平衡的最少丢弃次数

> **[yiduobo的每日leetcode 3679.使库存平衡的最少丢弃次数](https://zhuanlan.zhihu.com/p/1953190688586957164) · 知乎 · 2025-09-23 · 赞同 0**
> 力扣：[3679. 使库存平衡的最少丢弃次数](https://leetcode.cn/problems/minimum-discards-to-balance-inventory/) · Medium · 灵茶山艾府：[贪心 + 定长滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3679.使库存平衡的最少丢弃次数

[3679. 使库存平衡的最少丢弃次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-discards-to-balance-inventory/description/)

题目给出两个整数w和m，以及一个整数数组arrivals，其中arrivals[index]表示第index天到达的物品类型(天数从1开始编号)。

每个到达的物品可以被保留或者丢弃，物品只能在到达的当前被丢弃。对于index这一天，直到这一天为止最近的w天之内，每种类型的物品最多只能出现m次，若第index天到达的物品会使得最近w天之内该物品出现的次数超过m次，那么该物品必须被丢弃。

问最少需要丢弃的物品数量。

题目为了使得丢弃的物品数量最少，那么就应该按照到达顺序，在不得不丢弃的时候才丢弃，理由只有当连续w天之内同类型物品出现超过m次时才需要执行丢弃，丢弃的物品越靠后，更后面的物品重复的次数就越少，丢弃的可能性就越小。

基于这一点，只需使用一个长度为w的滑动窗口从左向右滑动，同时使用一个哈希表记录其中每种类型物品出现的次数。需要特别注意的是，由于窗口内有些物品已经被丢弃了，因此还需要额外使用一个哈希表或者队列来记录窗口内没有被丢弃掉的物品，这样一来才能在窗口移动时判断是否需要修改窗口左边界对应的物品在哈希表中出现的次数。

最后附上python代码：

```python
class Solution(object):
    def minArrivalsToDiscard(self, arrivals, w, m):
        """
        :type arrivals: List[int]
        :type w: int
        :type m: int
        :rtype: int
        """
        
        freq = {}
        res = 0
        q = deque()

        for index, v in enumerate(arrivals[:w]):
            if freq.get(v, 0) + 1 > m:
                res += 1
            else:
                freq[v] = freq.get(v, 0) + 1
                q.append(index)
        
        for index, v in enumerate(arrivals[w:]):
            if q and q[0] == index:
                freq[arrivals[index]] -= 1
                q.popleft()

            if freq.get(v, 0) + 1 > m:
                res += 1
            else:
                freq[v] = freq.get(v, 0) + 1
                q.append(index + w)
        
        return res
```
