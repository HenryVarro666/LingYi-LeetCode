---
title: "3572. 选择不同X值三元组使Y值之和最大"
aliases: ["yiduobo的每日leetcode 3572.选择不同X值三元组使Y值之和最大"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/hash-table", "leetcode/quickselect", "leetcode/sorting", "leetcode/heap-priority-queue"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1936558269603771051"
zhihu_id: "1936558269603771051"
zhihu_title: "yiduobo的每日leetcode 3572.选择不同X值三元组使Y值之和最大"
question_id: "3572"
question: "选择不同 X 值三元组使 Y 值之和最大"
problem_url: "https://leetcode.cn/problems/maximize-ysum-by-picking-a-triplet-of-distinct-xvalues/"
difficulty: "Medium"
created: "2025-08-06T22:49:36+08:00"
updated: "2025-08-06T22:49:36+08:00"
upvotes: 0
comments: 0
---

# 3572. 选择不同X值三元组使Y值之和最大

> **[yiduobo的每日leetcode 3572.选择不同X值三元组使Y值之和最大](https://zhuanlan.zhihu.com/p/1936558269603771051) · 知乎 · 2025-08-06 · 赞同 0**
> 力扣：[3572. 选择不同 X 值三元组使 Y 值之和最大](https://leetcode.cn/problems/maximize-ysum-by-picking-a-triplet-of-distinct-xvalues/) · Medium · 灵茶山艾府：[哈希表分组，维护每组最大值（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3572.选择不同X值三元组使Y值之和最大

[3572. 选择不同 X 值三元组使 Y 值之和最大 - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-ysum-by-picking-a-triplet-of-distinct-xvalues/description/)

题目给出两个整数数组x和y，长度均为n。现在要求从中选出三个不同的下标i、j、k，满足x[i]、x[j]、x[k]这三者间两两互不相同，同时使得y[i] + y[j] + y[k]最大。问最大可能得和为多少。

由于题目要求选择三个对应的x不同的下标，因此对于某个x值，若其被选择了，就应该选择对应的y最大的那个x。于是可以先一趟遍历，使用哈希表记录每种x对应的y的最大值，接下来问题就变成从这个哈希表对应的值中选出三个数，使得它们的和最大。对于这个问题，只需再对哈希表的值进行一趟遍历，选出其中最大的三个数累加起来即可。

最后附上python代码：

```python
class Solution(object):
    def maxSumDistinctTriplet(self, x, y):
        """
        :type x: List[int]
        :type y: List[int]
        :rtype: int
        """
        
        value_dict = {}
        for x_v, y_v in zip(x, y):
            if x_v not in value_dict or value_dict[x_v] < y_v:
                value_dict[x_v] = y_v
        
        first, second, third = None, None, None
        for v in value_dict.values():
            if first is None or first < v:
                first, second, third = v, first, second
            elif second is None or second < v:
                second, third = v, second
            elif third is None or third < v:
                third = v
        
        if third is None:
            return -1
        
        return first + second + third
```
