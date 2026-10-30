---
title: "757. 设置交集大小至少为2"
aliases: ["yiduobo的每日leetcode 757.设置交集大小至少为2"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/greedy", "leetcode/binary-search", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/338323748"
zhihu_id: "338323748"
zhihu_title: "yiduobo的每日leetcode 757.设置交集大小至少为2"
question_id: "757"
question: "设置交集大小至少为2"
problem_url: "https://leetcode.cn/problems/set-intersection-size-at-least-two/"
difficulty: "Hard"
rating: 2379
created: "2020-12-20T23:48:05+08:00"
updated: "2020-12-20T23:48:05+08:00"
upvotes: 0
comments: 0
---

# 757. 设置交集大小至少为2

> **[yiduobo的每日leetcode 757.设置交集大小至少为2](https://zhuanlan.zhihu.com/p/338323748) · 知乎 · 2020-12-20 · 赞同 0**
> 力扣：[757. 设置交集大小至少为2](https://leetcode.cn/problems/set-intersection-size-at-least-two/) · Hard · 灵茶山艾府：[通用解法：栈+二分查找（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

757.设置交集大小至少为2

[力扣](https://leetcode-cn.com/problems/set-intersection-size-at-least-two/)

贪心法的题目。

首先，我们根据区间的末尾从小到大进行排序。接下来，对于第0个区间，我们需要从中间选择两个数加入到S中。由于我们已经按末尾从小到大进行了排序，那么在这里我们很明显应该选择第0个区间中最右侧的两个数加入到S中，因为这两个数相比前面的数出现在后续区间中的可能性更大。

设选取的两个数分别为min和max，此时的答案为2，接下来我们遍历后续的所有区间，对于当前区间的起点x和终点y，有以下几种情况：

1、x \<\= min：

由于当前区间的终点y大于等于之前所有区间的终点，因此必然有y >\= max，那么综合起来就有x \<\= min \< max \<\= y，即当前区间中至少包含了min和max，已经满足条件。

2、x > min且x \<\= max：

当前区间仅有max一个数在S中，那么若y等于max，我们可以将y - 1也加入S中，同时更新min为y - 1；若y大于max，那么我们就将y加入到S中，同时更新min为老的max，新的max则是y。

这种情况下新加入了一个数到S当中，因此答案要加一。

3、x > max：

当前区间中没有任何数在S中，因此需要将当前区间最大的两个数y以及y - 1加入到S中，同时更新min为y - 1，max为y。

这种情况下新加入了两个数到S当中，因此答案要加二。

最后附上python代码：

```python
class Solution(object):
    def intersectionSizeTwo(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: int
        """

        intervals = sorted(intervals, key=lambda d:d[1])
        min_num = intervals[0][1] - 1
        max_num = intervals[0][1]
        res = 2
        for (x, y) in intervals[1:]:
            if x <= min_num:
                continue
            elif x <= max_num:
                if y == max_num:
                    min_num = max_num - 1
                else:
                    min_num = max_num
                    max_num = y

                res += 1
            else:
                min_num = y - 1
                max_num = y
                res += 2
        
        return res
```
