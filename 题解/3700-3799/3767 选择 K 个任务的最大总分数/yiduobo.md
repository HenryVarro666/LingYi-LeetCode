---
title: "3767. 选择K个任务的最大总分数"
aliases: ["yiduobo的每日leetcode 3767.选择K个任务的最大总分数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/quickselect", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1981121604063885030"
zhihu_id: "1981121604063885030"
zhihu_title: "yiduobo的每日leetcode 3767.选择K个任务的最大总分数"
question_id: "3767"
question: "选择 K 个任务的最大总分数"
problem_url: "https://leetcode.cn/problems/maximize-points-after-choosing-k-tasks/"
difficulty: "Medium"
rating: 1704
created: "2025-12-08T22:38:55+08:00"
updated: "2025-12-08T22:39:04+08:00"
upvotes: 1
comments: 0
---

# 3767. 选择K个任务的最大总分数

> **[yiduobo的每日leetcode 3767.选择K个任务的最大总分数](https://zhuanlan.zhihu.com/p/1981121604063885030) · 知乎 · 2025-12-08 · 赞同 1**
> 力扣：[3767. 选择 K 个任务的最大总分数](https://leetcode.cn/problems/maximize-points-after-choosing-k-tasks/) · Medium · 灵茶山艾府：[贪心 + 排序 / 快速选择（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3767.选择K个任务的最大总分数

[3767. 选择 K 个任务的最大总分数 - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-points-after-choosing-k-tasks/)

题目给出两个长度为n的整数数组technique1和technique2，表示有n个任务需要完成。

对于第index个任务，如果使用技巧1完成，可以得到technique1[index]的得分；如果使用技巧2，则可以得到technique2[index]的得分。

另外给出一个整数k，表示需要使用技巧1完成至少k个任务，其他的任务则可以用任意技巧完成。

问如何完成任务才能使得得分最大。

对于这类二选一的问题，一种常用的处理方法是初始状态下全部选择一边，然后计算每种选择的得分之差数组diff，那么问题就相当于在符合题目要求的前提下从diff中选择一些元素，使得选出来的这些元素之和最优。从diff中选出来的这些元素就相当于改成了另一边。

对于本题，由于要求至少选择k个技巧1，那么在这里可以先全部选择技巧2，然后计算出得分之差数组diff。

接下来，问题就转化成了在diff中选择至少k个元素，使得这些元素之和最大。很明显，在这里就应该优先选择diff中最大的k个元素，于是可以先将diff从大到小进行排序，然后选择其中最大的k个元素累加起来。

需要特别注意的是，如果此时diff中还存在没有选择的正数，也应该一并选择，于是可以从下标k开始向后遍历，将剩余元素中的整数也累加起来。

最后附上python代码：

```python
class Solution(object):
    def maxPoints(self, technique1, technique2, k):
        """
        :type technique1: List[int]
        :type technique2: List[int]
        :type k: int
        :rtype: int
        """
        
        diff = sorted([x - y for x, y in zip(technique1, technique2)], reverse=True)
        res = sum(technique2) + sum(diff[:k])
        p = k
        while p < len(diff) and diff[p] > 0:
            res += diff[p]
            p += 1
        
        return res
```
