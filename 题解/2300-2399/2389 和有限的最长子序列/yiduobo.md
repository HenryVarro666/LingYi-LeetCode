---
title: "2389. 和有限的最长子序列"
aliases: ["yiduobo的每日leetcode 2389.和有限的最长子序列"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/binary-search", "leetcode/prefix-sum", "leetcode/sorting", "题单/二分算法", "题单/常用数据结构", "题单/二分算法/一-二分查找", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/565764948"
zhihu_id: "565764948"
zhihu_title: "yiduobo的每日leetcode 2389.和有限的最长子序列"
question_id: "2389"
question: "和有限的最长子序列"
problem_url: "https://leetcode.cn/problems/longest-subsequence-with-limited-sum/"
difficulty: "Easy"
created: "2022-09-19T00:47:11+08:00"
updated: "2022-09-19T00:47:11+08:00"
upvotes: 0
comments: 0
---

# 2389. 和有限的最长子序列

> **[yiduobo的每日leetcode 2389.和有限的最长子序列](https://zhuanlan.zhihu.com/p/565764948) · 知乎 · 2022-09-19 · 赞同 0**
> 力扣：[2389. 和有限的最长子序列](https://leetcode.cn/problems/longest-subsequence-with-limited-sum/) · Easy · 灵茶山艾府：[非暴力做法：前缀和 + 二分查找 + 原地 O(1) 空间（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2389.和有限的最长子序列

[力扣](https://leetcode.cn/problems/longest-subsequence-with-limited-sum/)

注意题目要选的子序列，那么为了使得子序列尽量长，就应该优先选择较小的数字。另一方面，对于较大的query而言，其对应的子序列必然是在较小的query对应的子序列基础上再添加一些没使用过的较小的数。

基于上面两点，就可以将nums和queries分别从小到大进行排序，然后遍历排序后的queries，利用单调性在一趟遍历内确定每个query对应的子序列之和。

最后附上python代码：

```python
class Solution(object):
    def answerQueries(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[int]
        :rtype: List[int]
        """

        nums.sort()
        queries_with_index = [[query, index] for index, query in enumerate(queries)]
        queries_with_index.sort(key = lambda d:d[0])
        
        n = len(nums)
        m = len(queries_with_index)
        res = [0] * m
        p = 0
        s = 0
        for query, index in queries_with_index:
            while p < n and s + nums[p] <= query:
                s += nums[p]
                p += 1
            res[index] = p
        
        return res
```
