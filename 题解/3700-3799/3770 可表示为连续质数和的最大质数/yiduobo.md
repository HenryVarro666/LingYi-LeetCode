---
title: "3770. 可表示为连续质数和的最大质数"
aliases: ["yiduobo的每日leetcode 3770.可表示为连续质数和的最大质数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/two-pointers", "leetcode/binary-search", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1981134253312996764"
zhihu_id: "1981134253312996764"
zhihu_title: "yiduobo的每日leetcode 3770.可表示为连续质数和的最大质数"
question_id: "3770"
question: "可表示为连续质数和的最大质数"
problem_url: "https://leetcode.cn/problems/largest-prime-from-consecutive-prime-sum/"
difficulty: "Medium"
rating: 1547
created: "2025-12-10T21:06:36+08:00"
updated: "2025-12-10T21:06:40+08:00"
upvotes: 3
comments: 0
---

# 3770. 可表示为连续质数和的最大质数

> **[yiduobo的每日leetcode 3770.可表示为连续质数和的最大质数](https://zhuanlan.zhihu.com/p/1981134253312996764) · 知乎 · 2025-12-10 · 赞同 3**
> 力扣：[3770. 可表示为连续质数和的最大质数](https://leetcode.cn/problems/largest-prime-from-consecutive-prime-sum/) · Medium · 灵茶山艾府：[两种写法：预处理 + 二分查找 / 双指针（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3770.可表示为连续质数和的最大质数

[3770. 可表示为连续质数和的最大质数 - 力扣（LeetCode）](https://leetcode.cn/problems/largest-prime-from-consecutive-prime-sum/description/)

题目给出一个整数n，大小不超过5 \* 10^5。

要求找出小等于等于n的最大质数，这个质数可以表示为从2开始的一个或多个连续质数之和。若不存在这样的质数，则返回0。

由于n的大小不超过5 \* 10^5，本题最优的处理方法实际上是打表。

如果不使用打表法，则可以先通过筛法找出所有小于等于n的质数。接下来从小到大遍历这些质数，并累加到一个变量s中，直到s大于等于n为止。若当前的s也是质数，则使用s更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def largestPrime(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        prime = [True] * (n + 1)
        p_list = []
        x = 2
        while x * x <= n:
            if prime[x]:
                for v in range(x + x, n + 1, x):
                    prime[v] = False
            x += 1
        
        s = 0
        res = 0
        for v in range(2, n + 1):
            if prime[v]:
                s += v
                if s > n:
                    break
                
                if prime[s]:
                    res = s
        
        return res
```
