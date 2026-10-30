---
title: "3695. 交换元素后的最大交替和"
aliases: ["yiduobo的每日leetcode 3695.交换元素后的最大交替和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/union-find", "leetcode/graph", "leetcode/sorting", "题单/常用数据结构", "题单/图论算法", "题单/贪心算法", "题单/常用数据结构/七-并查集", "题单/图论算法/一-图的遍历", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1956124494881097673"
zhihu_id: "1956124494881097673"
zhihu_title: "yiduobo的每日leetcode 3695.交换元素后的最大交替和"
question_id: "3695"
question: "交换元素后的最大交替和"
problem_url: "https://leetcode.cn/problems/maximize-alternating-sum-using-swaps/"
difficulty: "Hard"
rating: 1984
created: "2025-10-01T21:57:39+08:00"
updated: "2025-10-01T21:57:39+08:00"
upvotes: 1
comments: 0
---

# 3695. 交换元素后的最大交替和

> **[yiduobo的每日leetcode 3695.交换元素后的最大交替和](https://zhuanlan.zhihu.com/p/1956124494881097673) · 知乎 · 2025-10-01 · 赞同 1**
> 力扣：[3695. 交换元素后的最大交替和](https://leetcode.cn/problems/maximize-alternating-sum-using-swaps/) · Hard · 灵茶山艾府：[同一集合中的元素可以随意交换（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3695.交换元素后的最大交替和

[3695. 交换元素后的最大交替和 - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-alternating-sum-using-swaps/description/)

题目给出一个整数数组nums，要求最大化nums的交替和，这里的交替和指的是偶数下标元素之和减去奇数下标元素之和。

另外给出一个二维整数数组swaps，其中swaps\[index\] \= \[p\[index\], q\[index\]\]，表示可以交换下标在p\[index\]与q\[index\]的元素。这些交换可以以任意顺序进行任意次。

问可能得到的最大和是多少。

如果将数组下标视为图中的点，那么一组swaps中的下标对就相当于在图中对应的点间连上了一条边。由于题目中的交换可以按任意顺序进行任意次，这也就意味着图中同一连通块中的点可以随意排列。为了使得最终的交替和最大，在这里就应该将较大的元素放到偶数坐标，将较小的元素放到奇数坐标。

基于上面的结论，就得到了一种做法：

先遍历所有的swaps，使用并查集维护所有下标间的连通性。接下来一趟遍历，使用哈希表记录每个连通块中的下标列表，再遍历每个连通块对应的列表，收集其中下标对应的元素并从大到小排序，同时统计其中偶数下标的数量even。排序完成后，将前even个元素累加到答案中，表示这部分元素将安排到偶数下标中，然后从even开始的其他元素从答案中减去，表示这部分元素安排到奇数下标中。

最后附上python代码：

```python
class Solution(object):
    def maxAlternatingSum(self, nums, swaps):
        """
        :type nums: List[int]
        :type swaps: List[List[int]]
        :rtype: int
        """
        
        n = len(nums)
        fa = [index for index in range(n)]

        def find(fa, x):
            if fa[x] != x:
                fa[x] = find(fa, fa[x])
            return fa[x]

        for x, y in swaps:
            fa_x = find(fa, x)
            fa_y = find(fa, y)
            if fa_x != fa_y:
                fa[fa_x] = fa_y
        
        group = {}
        for index in range(n):
            fa_index = find(fa, index)
            if fa_index not in group:
                group[fa_index] = []
            group[fa_index].append(index)

        res = 0
        for index_list in group.values():
            num_list = [nums[index] for index in index_list]
            even = sum([index % 2 == 0 for index in index_list])
            num_list.sort(reverse=True)
            res += sum(num_list[:even])
            res -= sum(num_list[even:])
        
        return res
```
