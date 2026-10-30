---
title: "3745. 三元素表达式的最大值"
aliases: ["yiduobo的每日leetcode 3745.三元素表达式的最大值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1973427089446295286"
zhihu_id: "1973427089446295286"
zhihu_title: "yiduobo的每日leetcode 3745.三元素表达式的最大值"
question_id: "3745"
question: "三元素表达式的最大值"
problem_url: "https://leetcode.cn/problems/maximize-expression-of-three-elements/"
difficulty: "Easy"
rating: 1218
created: "2025-11-16T16:31:07+08:00"
updated: "2025-11-16T16:31:07+08:00"
upvotes: 2
comments: 0
---

# 3745. 三元素表达式的最大值

> **[yiduobo的每日leetcode 3745.三元素表达式的最大值](https://zhuanlan.zhihu.com/p/1973427089446295286) · 知乎 · 2025-11-16 · 赞同 2**
> 力扣：[3745. 三元素表达式的最大值](https://leetcode.cn/problems/maximize-expression-of-three-elements/) · Easy · 灵茶山艾府：[贪心，前二大之和减去最小值（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3745.三元素表达式的最大值

<https://leetcode.cn/problems/maximize-expression-of-three-elements/description/>

题目给出一个整数数组nums，要求从中选出三个下标互不相同的元素a、b和c，使得a + b - c的值最大。问这个值最大可能是多少。

为了使得最终答案最大，就应该让a和b尽量大，让c尽量小，于是只需一趟遍历，找出nums中的最大值以及次大值作为a和b，找出最小值作为c，然后计算最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def maximizeExpressionOfThree(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        ma1, ma2, mi = None, None, None
        for v in nums:
            if ma1 is None or ma1 < v:
                ma1, ma2 = v, ma1
            elif ma2 is None or ma2 < v:
                ma2 = v
            
            if mi is None or mi > v:
                mi = v
        
        return ma1 + ma2 - mi
```
