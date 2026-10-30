---
title: "3477. 将水果放入篮子II & 3479. 将水果装入篮子III"
aliases: ["yiduobo的每日leetcode 3477.将水果放入篮子II && 3479.将水果装入篮子III", "3477. 将水果放入篮子II", "3479. 将水果装入篮子III"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/segment-tree", "leetcode/binary-search", "leetcode/medium", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1897260370260886422"
zhihu_id: "1897260370260886422"
zhihu_title: "yiduobo的每日leetcode 3477.将水果放入篮子II && 3479.将水果装入篮子III"
question_id: ["3477", "3479"]
question: ["水果成篮 II", "水果成篮 III"]
problem_url: ["https://leetcode.cn/problems/fruits-into-baskets-ii/", "https://leetcode.cn/problems/fruits-into-baskets-iii/"]
difficulty: ["Easy", "Medium"]
rating: 2178
created: "2025-04-20T12:29:53+08:00"
updated: "2025-04-20T12:29:53+08:00"
upvotes: 1
comments: 0
---

# 3477. 将水果放入篮子II & 3479. 将水果装入篮子III

> **[yiduobo的每日leetcode 3477.将水果放入篮子II && 3479.将水果装入篮子III](https://zhuanlan.zhihu.com/p/1897260370260886422) · 知乎 · 2025-04-20 · 赞同 1**
> 力扣：[3477. 水果成篮 II](https://leetcode.cn/problems/fruits-into-baskets-ii/) · Easy · 灵茶山艾府：[非暴力做法（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3479. 水果成篮 III](https://leetcode.cn/problems/fruits-into-baskets-iii/) · Medium · 灵茶山艾府：[线段树二分（Python/Java/C++/Go）](../3479%20水果成篮%20III/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3477.将水果放入篮子II

[3477. 将水果放入篮子 II - 力扣（LeetCode）](https://leetcode.cn/problems/fruits-into-baskets-ii/description/)

3479.将水果装入篮子III

[3479. 将水果装入篮子 III - 力扣（LeetCode）](https://leetcode.cn/problems/fruits-into-baskets-iii/)

题目给出两个长度为n的整数数组fruits以及baskets，其中fruits[index]表示第index种水果的数目，baskets[index]表示第index个篮子的容量。

现在要求按从左往右的顺序，将fruits中的水果放置到篮子中。每种水果必须放到最左侧的容量大于等于该水果数量的可用篮子中，同时每个篮子只能放置一种水果。如果某种水果找不到可用的篮子，则保持未放置的状态。

问最终有多少种水果是未放置的。

两题的题设相同，第二题的数据规模较大，n的规模可达10^5，而两个数中的元素大小可达10^9。

题目的数据规模很大，直接使用暴力法显然是不行的。

对于寻找数组中最左侧的大于等于指定值的下标这一问题，可以利用二分的思路。具体来说，对于区间[left, right]，若区间最大值ma大于等于指定值v，说明区间中至少存在一处可用的下标。现在要求找出最左侧的可用下标，那么在这里可以先递归求解左半区间[left, mid]中的最左侧的可用下标，若不存在，再递归求解右半区间[mid + 1, right]中的最左侧的可用下标。也就是说，在这里需要维护区间的最大值。

另一方面，由于每个篮子只能放置一种水果，那么可以认为某个篮子在放置水果后，其容量将被修改为0，这样做的好处是不会影响上面区间最大值的逻辑。

综合以上两点，这是一个动态区间最大值，以及单点修改的问题，在这里使用线段树是比较合适的。线段树有关的内容可以参考之前的699题，这里就不展开了。

[yiduobo：yiduobo的每日leetcode 699.掉落的方块](https://zhuanlan.zhihu.com/p/316523832)

最后附上python代码：

```python
class Solution(object):
    def numOfUnplacedFruits(self, fruits, baskets):
        """
        :type fruits: List[int]
        :type baskets: List[int]
        :rtype: int
        """
        
        n = len(baskets)
        ma = [0] * (n * 4)

        def update(p, left, right, index, v):
            if left == right:
                ma[p] = v
                return

            mid = (left + right) // 2
            if index <= mid:
                update(p * 2 + 1, left, mid, index, v)
            else:
                update(p * 2 + 2, mid + 1, right, index, v)
            ma[p] = max(ma[p * 2 + 1], ma[p * 2 + 2])

        def find(p, left, right, v):
            if left == right:
                return left
            mid = (left + right) // 2
            if ma[p * 2 + 1] >= v:
                return find(p * 2 + 1, left, mid, v)
            else:
                return find(p * 2 + 2, mid + 1, right, v)

        for index, b in enumerate(baskets):
            update(0, 0, n - 1, index, b)
        
        res = 0
        for index, f in enumerate(fruits):
            if ma[0] < f:
                res += 1
            else:
                p = find(0, 0, n - 1, f)
                update(0, 0, n - 1, p, 0)
        
        return res
```
