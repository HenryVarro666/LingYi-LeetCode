---
title: "3896. 将数组转换为交替质数数组的最少操作次数"
aliases: ["yiduobo的每日leetcode 3896.将数组转换为交替质数数组的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/number-theory", "leetcode/bao-li", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2027507579719357643"
zhihu_id: "2027507579719357643"
zhihu_title: "yiduobo的每日leetcode 3896.将数组转换为交替质数数组的最少操作次数"
question_id: "3896"
question: "将数组转换为交替质数数组的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-transform-array-into-alternating-prime/"
difficulty: "Medium"
rating: 1435
created: "2026-04-14T22:10:14+08:00"
updated: "2026-04-14T22:10:14+08:00"
upvotes: 1
comments: 0
---

# 3896. 将数组转换为交替质数数组的最少操作次数

> **[yiduobo的每日leetcode 3896.将数组转换为交替质数数组的最少操作次数](https://zhuanlan.zhihu.com/p/2027507579719357643) · 知乎 · 2026-04-14 · 赞同 1**
> 力扣：[3896. 将数组转换为交替质数数组的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-transform-array-into-alternating-prime/) · Medium · 灵茶山艾府：[筛质数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3896.将数组转换为交替质数数组的最少操作次数

<https://leetcode.cn/problems/minimum-operations-to-transform-array-into-alternating-prime/description/>

题目给出一个整数数组nums，其长度以及其中元素的大小都不超过10^5。

若其中所有偶数下标处的元素都是质数，且所有奇数下标处的元素都是非质数，那么就称这个数组为交替质数数组。

在一次操作中，可以将其中的任意元素增加1。问将nums变为交替质数数组所需的最少操作次数。

基于质数分布的认识，在这里可以直接一趟遍历，然后检测当前位置上的元素是否满足条件。若不满足，则不断加1直到满足条件。因为质数的分布不会太过离散，因此这里加1的次数不会太多。

而对于质数的检测，在这里可以先用筛法找出范围内的所有质数，也可以枚举约数暴力检测。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        def check(v, p):
            if v not in p:
                if v == 1:
                    p[v] = False
                else:
                    x = 2
                    p[v] = True
                    while x * x <= v:
                        if v % x == 0:
                            p[v] = False
                            break
                        x += 1
            
            return p[v]

        p = {}
        res = 0
        for index, v in enumerate(nums):
            flag = check(v, p)
            if index % 2 == 0:
                while not flag:
                    res += 1
                    v += 1
                    flag = check(v, p)
            else:
                while flag:
                    res += 1
                    v += 1
                    flag = check(v, p)
        
        return res
```
