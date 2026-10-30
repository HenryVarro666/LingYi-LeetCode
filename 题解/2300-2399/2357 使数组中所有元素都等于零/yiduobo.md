---
title: "2357. 使数组中所有元素都等于零"
aliases: ["yiduobo的每日leetcode 2357.使数组中所有元素都等于零"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/561980935"
zhihu_id: "561980935"
zhihu_title: "yiduobo的每日leetcode 2357.使数组中所有元素都等于零"
question_id: "2357"
question: "使数组中所有元素都等于零"
problem_url: "https://leetcode.cn/problems/make-array-zero-by-subtracting-equal-amounts/"
difficulty: "Easy"
created: "2022-09-06T23:47:13+08:00"
updated: "2022-09-06T23:47:13+08:00"
upvotes: 1
comments: 0
---

# 2357. 使数组中所有元素都等于零

> **[yiduobo的每日leetcode 2357.使数组中所有元素都等于零](https://zhuanlan.zhihu.com/p/561980935) · 知乎 · 2022-09-06 · 赞同 1**
> 力扣：[2357. 使数组中所有元素都等于零](https://leetcode.cn/problems/make-array-zero-by-subtracting-equal-amounts/) · Easy · 灵茶山艾府：[转换成求不同元素的个数](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2357.使数组中所有元素都等于零

[力扣](https://leetcode.cn/problems/make-array-zero-by-subtracting-equal-amounts/)

由于题目中的单次操作减去的x必须小于等于当前数组中的最小元素，那么至少就需要一次操作将当前数组中的最小元素变为0。同样的，在本次操作后，数组中新的最小元素也至少需要一次操作才能变为零，依次类推。

可以发现，数组中有多少种不同的正数就需要操作多少次，因此可以将数组中所有数都加入到集合中，集合的长度就是数组中不同整数的数目。如果0也在集合中，那么答案就是集合的长度减1，否则答案就是集合的长度。

最后附上python代码：

```python
class Solution(object):
    def minimumOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        num_set = set(nums)
        res = len(num_set)
        if 0 in num_set:
            res -= 1
        
        return res
```
