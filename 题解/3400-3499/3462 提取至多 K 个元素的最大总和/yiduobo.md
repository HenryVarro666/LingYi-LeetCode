---
title: "3462. 提取至多K个元素的最大总和"
aliases: ["yiduobo的每日leetcode 3462.提取至多K个元素的最大总和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/quickselect", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1895247527277740723"
zhihu_id: "1895247527277740723"
zhihu_title: "yiduobo的每日leetcode 3462.提取至多K个元素的最大总和"
question_id: "3462"
question: "提取至多 K 个元素的最大总和"
problem_url: "https://leetcode.cn/problems/maximum-sum-with-at-most-k-elements/"
difficulty: "Medium"
rating: 1416
created: "2025-04-14T22:57:48+08:00"
updated: "2025-04-14T22:57:48+08:00"
upvotes: 1
comments: 0
---

# 3462. 提取至多K个元素的最大总和

> **[yiduobo的每日leetcode 3462.提取至多K个元素的最大总和](https://zhuanlan.zhihu.com/p/1895247527277740723) · 知乎 · 2025-04-14 · 赞同 1**
> 力扣：[3462. 提取至多 K 个元素的最大总和](https://leetcode.cn/problems/maximum-sum-with-at-most-k-elements/) · Medium · 灵茶山艾府：[贪心+排序/快速选择（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3462.提取至多K个元素的最大总和

[3462. 提取至多 K 个元素的最大总和 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-sum-with-at-most-k-elements/description/)

题目给出一个大小为n \* m的二维矩阵grid，以及一个长度为n的整数数组limits，和一个整数k。现在要求从grid中提取至多k个元素，并计算这些元素的最大总和，要求从grid的第index行提取的元素个数不超过limits[index]。问最大总和为多少。

本题比较好的处理方法是先对每一行，分别找出这一行中的top limit个元素，然后对于所有行，使用一个堆来执行多路归并，获取其中的top k大的元素。

我在这里采用的是比较暴力的处理方法。先对每一行进行完整的排序，然后取出top limit，加入到一个数组candidate中，然后再对candidate排序，取出top k并求和。

最后附上python代码：

```python
class Solution(object):
    def maxSum(self, grid, limits, k):
        """
        :type grid: List[List[int]]
        :type limits: List[int]
        :type k: int
        :rtype: int
        """
        
        candidate = []
        m = len(grid)
        for index in range(m):
            candidate.extend(sorted(grid[index], reverse=True)[:limits[index]])
        
        return sum(sorted(candidate, reverse=True)[:k])
```
