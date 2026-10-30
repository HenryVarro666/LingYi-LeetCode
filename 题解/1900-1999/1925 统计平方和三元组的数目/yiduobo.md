---
title: "1925. 统计平方和三元组的数目"
aliases: ["yiduobo的每日leetcode 1925.统计平方和三元组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/combinatorics", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/485449614"
zhihu_id: "485449614"
zhihu_title: "yiduobo的每日leetcode 1925.统计平方和三元组的数目"
question_id: "1925"
question: "统计平方和三元组的数目"
problem_url: "https://leetcode.cn/problems/count-square-sum-triples/"
difficulty: "Easy"
created: "2022-03-22T15:56:33+08:00"
updated: "2022-03-22T15:56:33+08:00"
upvotes: 0
comments: 0
---

# 1925. 统计平方和三元组的数目

> **[yiduobo的每日leetcode 1925.统计平方和三元组的数目](https://zhuanlan.zhihu.com/p/485449614) · 知乎 · 2022-03-22 · 赞同 0**
> 力扣：[1925. 统计平方和三元组的数目](https://leetcode.cn/problems/count-square-sum-triples/) · Easy · 灵茶山艾府：[非暴力做法：本原勾股数组+数论分块+容斥（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1925.统计平方和三元组的数目

[力扣](https://leetcode-cn.com/problems/count-square-sum-triples/)

题目要求寻找一定范围内所有的勾股数对，感觉应该有数学方法来构造，不过没有什么思路。题目的范围很小，直接使用平方枚举加哈希表，甚至三次方枚举都可以。

最后附上python代码：

```python
class Solution(object):
    def countTriples(self, n):
        """
        :type n: int
        :rtype: int
        """

        pow_set = set()
        for c in range(1, n + 1):
            pow_set.add(c * c)
        
        res = 0
        for a in range(1, n + 1):
            for b in range(a + 1, n + 1):
                if a * a + b * b in pow_set:
                    res += 2
        
        return res
```
