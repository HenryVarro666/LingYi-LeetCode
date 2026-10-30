---
title: "3091. 执行操作使数据元素之和大于等于K"
aliases: ["yiduobo的每日leetcode 3091.执行操作使数据元素之和大于等于K"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/math", "leetcode/enumeration", "题单/数学算法", "题单/贪心算法", "题单/数学算法/七-杂项", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/699080106"
zhihu_id: "699080106"
zhihu_title: "yiduobo的每日leetcode 3091.执行操作使数据元素之和大于等于K"
question_id: "3091"
question: "执行操作使数据元素之和大于等于 K"
problem_url: "https://leetcode.cn/problems/apply-operations-to-make-sum-of-array-greater-than-or-equal-to-k/"
difficulty: "Medium"
rating: 1522
created: "2024-05-21T22:30:15+08:00"
updated: "2024-05-21T22:30:15+08:00"
upvotes: 0
comments: 0
---

# 3091. 执行操作使数据元素之和大于等于K

> **[yiduobo的每日leetcode 3091.执行操作使数据元素之和大于等于K](https://zhuanlan.zhihu.com/p/699080106) · 知乎 · 2024-05-21 · 赞同 0**
> 力扣：[3091. 执行操作使数据元素之和大于等于 K](https://leetcode.cn/problems/apply-operations-to-make-sum-of-array-greater-than-or-equal-to-k/) · Medium · 灵茶山艾府：[两种方法：枚举 / O(1) 数学公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3091.执行操作使数据元素之和大于等于K

[. - 力扣（LeetCode）](https://leetcode.cn/problems/apply-operations-to-make-sum-of-array-greater-than-or-equal-to-k/)

题目给出加一操作和复制操作，分别可以将数组中任意元素加一，或者复制数组中任意元素添加到数组末尾，问至少要多少次操作才能使得数组之和大于等于k。

首先可以明确的是，所有的加一操作都应该在复制操作之前，因为先复制再加一，相当于浪费了一。

接下来，不妨设两种操作一共进行了t次，其中加一操作执行了a次，那么数组中的元素就是a + 1，而复制操作执行了t - a次，因此数组中一共有t - a + 1个a + 1，这些元素之和就是(a + 1)(t - a + 1)。可以发现，当t固定时，让a尽可能接近t / 2是最优的选择。

方便起见，令x \= a + 1，y \= t - a + 1，那么在这里就是要找出一组尽量接近的x和y，满足xy >\= k。于是只需对k开根号向上取整作为x，然后通过k除以x向上取整得到y，最后返回x + y - 2即可。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, k):
        """
        :type k: int
        :rtype: int
        """

        x = int(k ** 0.5)
        if x * x < k:
            x += 1
        
        y = (k - 1) // x + 1
        return x + y - 2
```
