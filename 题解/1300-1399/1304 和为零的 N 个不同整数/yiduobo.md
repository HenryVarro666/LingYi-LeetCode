---
title: "1304. 和为零的N个唯一整数"
aliases: ["yiduobo的每日leetcode 1304.和为零的N个唯一整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "题单/贪心算法", "题单/贪心算法/六-构造题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/391232221"
zhihu_id: "391232221"
zhihu_title: "yiduobo的每日leetcode 1304.和为零的N个唯一整数"
question_id: "1304"
question: "和为零的 N 个不同整数"
problem_url: "https://leetcode.cn/problems/find-n-unique-integers-sum-up-to-zero/"
difficulty: "Easy"
rating: 1167
created: "2021-07-19T22:27:51+08:00"
updated: "2021-07-19T22:27:51+08:00"
upvotes: 0
comments: 0
---

# 1304. 和为零的N个唯一整数

> **[yiduobo的每日leetcode 1304.和为零的N个唯一整数](https://zhuanlan.zhihu.com/p/391232221) · 知乎 · 2021-07-19 · 赞同 0**
> 力扣：[1304. 和为零的 N 个不同整数](https://leetcode.cn/problems/find-n-unique-integers-sum-up-to-zero/) · Easy · 灵茶山艾府：[两种方法：对称/等差数列和（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1304.和为零的N个唯一整数

[力扣](https://leetcode-cn.com/problems/find-n-unique-integers-sum-up-to-zero/)

题目只要求给出一个可行解，构造的方法有很多，我在这里采用的方法是先将前n - 1个数设为1到n - 1，此时的和为n \* (n - 1) / 2，那么最后再添加一个 -n \* (n - 1) / 2即可，此时前n - 1个数都是正数，且各不相同，而最后一个数为负数，因此符合题目要求。

最后附上python代码：

```python
class Solution(object):
    def sumZero(self, n):
        """
        :type n: int
        :rtype: List[int]
        """

        res = range(1, n)
        res.append(-(n - 1) * n / 2)
        return res
```
