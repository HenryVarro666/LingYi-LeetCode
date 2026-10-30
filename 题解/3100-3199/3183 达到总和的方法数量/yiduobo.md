---
title: "3183. 达到总和的方法数量"
aliases: ["yiduobo的每日leetcode 3183.达到总和的方法数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/706067512"
zhihu_id: "706067512"
zhihu_title: "yiduobo的每日leetcode 3183.达到总和的方法数量"
question_id: "3183"
question: "达到总和的方法数量"
problem_url: "https://leetcode.cn/problems/the-number-of-ways-to-make-the-sum/"
created: "2024-06-29T03:33:19+08:00"
updated: "2024-06-29T03:33:19+08:00"
upvotes: 1
comments: 0
---

# 3183. 达到总和的方法数量

> **[yiduobo的每日leetcode 3183.达到总和的方法数量](https://zhuanlan.zhihu.com/p/706067512) · 知乎 · 2024-06-29 · 赞同 1**
> 力扣：[3183. 达到总和的方法数量](https://leetcode.cn/problems/the-number-of-ways-to-make-the-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3183.达到总和的方法数量

[. - 力扣（LeetCode）](https://leetcode.cn/problems/the-number-of-ways-to-make-the-sum/description/)

题目给出不限量的面值为1、2、6的硬币，以及两枚面值为4的硬币，接下来给出一个整数n，问通过这些硬币构成和为n的方案数。

注意到面值为4的硬币只有两枚，那么就只有全用了、只用一枚、全都不用三种情况，分别对应的就是通过1、2、6构成面试和为n - 8、n - 4、n的方案数。

而对于这个问题，则是一个经典的背包问题。令f[index]表示仅通过1、2、6构成面值和为index的方案数，初始状态下有f[0] \= 1，接下来对于index > 0的f[index]：

1、若index >\= 1，那么就有f[index] +\= f[index - 1]，表示新增了面值为1的硬币

2、若index >\= 2，那么就有f[index] +\= f[index - 2]，表示新增了面值为2的硬币

3、若index >\= 6，那么就有f[index] +\= f[index - 6]，表示新增了面值为6的硬币

计算f[1]到f[n]的结果，初始化答案为f[n]，然后根据n与4和8的大小关系，来确定是否应该将f[n - 4]与f[n - 8]累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def numberOfWays(self, n):
        """
        :type n: int
        :rtype: int
        """

        mod = 10 ** 9 + 7
        
        f = [0] * (n + 1)
        f[0] = 1
        for index in range(1, n + 1):
            f[index] += f[index - 1]
        for index in range(2, n + 1):
            f[index] += f[index - 2]
        for index in range(6, n + 1):
            f[index] += f[index - 6]
            if f[index] >= mod:
                f[index] -= mod

        res = f[n]
        if n >= 4:
            res += f[n - 4]
            if n >= 8:
                res += f[n - 8]
        
        return res % mod
```
