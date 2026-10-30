---
title: "4000. 给定数位和的最大整数"
aliases: ["yiduobo的每日leetcode 4000.给定数位和的最大整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/math", "leetcode/string", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2065236106623427142"
zhihu_id: "2065236106623427142"
zhihu_title: "yiduobo的每日leetcode 4000.给定数位和的最大整数"
question_id: "4000"
question: "给定数位和的最大整数"
problem_url: "https://leetcode.cn/problems/largest-integer-with-given-digit-sum/"
difficulty: "Easy"
rating: 1200
created: "2026-07-28T00:49:43+08:00"
updated: "2026-07-28T00:49:43+08:00"
upvotes: 1
comments: 0
---

# 4000. 给定数位和的最大整数

> **[yiduobo的每日leetcode 4000.给定数位和的最大整数](https://zhuanlan.zhihu.com/p/2065236106623427142) · 知乎 · 2026-07-28 · 赞同 1**
> 力扣：[4000. 给定数位和的最大整数](https://leetcode.cn/problems/largest-integer-with-given-digit-sum/) · Easy · 灵茶山艾府：[两种方法：字符串 / 数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4000.给定数位和的最大整数

<https://leetcode.cn/problems/largest-integer-with-given-digit-sum/description/>

题目给出两个非负整数n和s，要求返回满足以下条件的最大整数：

- 最多有n为数字
- 其各位数字之和等于s

若不存在这样的整数，则返回-1。

首先，这个整数的位数在1到n之间，且0没有被禁用，因此数位和的可能范围就是0到9 \* n，因此当s大于9 \* n时，答案必然为-1，否则一定有符合条件的整数。

接下来，为了使得这个整数尽量大，就应该让这个整数的位数打满n，同时高位上尽可能大。于是可以先假设这是一个n位数，然后不断从s中分离出9填充到这个数的高位上，若s不足9，就全部填进去。这样一来，就构造出了最大的整数。

具体实现上，可以先维护一个p10，初始值为10的n - 1次方，表示当前填充的位数对应的10的幂。接下来从高到低逐位填充，将计划填进去的数字乘以p10累加到答案中，将p10除以10然后考虑下一位即可。

最后附上python代码：

```python
class Solution(object):
    def largestInteger(self, n, s):
        """
        :type n: int
        :type s: int
        :rtype: int
        """
        
        if s > n * 9:
            return -1
        
        if s == 0:
            return 0
        
        res = 0
        p10 = 10 ** (n - 1)
        for _ in range(n):
            d = min(s, 9)
            res += d * p10
            p10 //= 10
            s -= d
        
        return res
```
