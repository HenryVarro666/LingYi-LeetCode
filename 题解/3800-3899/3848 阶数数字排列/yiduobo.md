---
title: "3848. 阶数数字排列"
aliases: ["yiduobo的每日leetcode 3848.阶数数字排列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2011490979287409477"
zhihu_id: "2011490979287409477"
zhihu_title: "yiduobo的每日leetcode 3848.阶数数字排列"
question_id: "3848"
question: "阶数数字排列"
problem_url: "https://leetcode.cn/problems/check-digitorial-permutation/"
difficulty: "Medium"
created: "2026-03-02T22:08:30+08:00"
updated: "2026-03-02T22:08:30+08:00"
upvotes: 0
comments: 0
---

# 3848. 阶数数字排列

> **[yiduobo的每日leetcode 3848.阶数数字排列](https://zhuanlan.zhihu.com/p/2011490979287409477) · 知乎 · 2026-03-02 · 赞同 0**
> 力扣：[3848. 阶数数字排列](https://leetcode.cn/problems/check-digitorial-permutation/) · Medium · 灵茶山艾府：[不用字符串的写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3848.阶数数字排列

<https://leetcode.cn/problems/check-digitorial-permutation/description/>

题目给出一个整数n，其大小在1到10^9之间。

若一个数字的所有位数的阶乘之和，恰好等于数字本身，则称其为阶数数字。

现在要求判断将n进行任意排列后，能否得到阶数数字。

无论n如何排列，其中的数位不会产生变化，因此这些数的阶乘之和也不会变化。因此可以先将n的数位分离出来，计算阶乘并累加起来得到阶乘之和s。

接下来，则可以反过来思考：若可以通过将n进行排列得到s，那么反过来也可以通过将s重新排列得到n。于是只需将s的数位分离出来，判断s中每种数字出现的次数是否与n相同即可。

最后附上python代码：

```python
class Solution(object):
    def isDigitorialPermutation(self, n):
        """
        :type n: int
        :rtype: bool
        """
        
        fact = [1]
        for v in range(1, 10):
            fact.append(fact[-1] * v)
        
        d = []
        s = 0
        while n:
            d.append(n % 10)
            s += fact[d[-1]]
            n //= 10
        
        ds = []
        while s:
            ds.append(s % 10)
            s //= 10
        
        return sorted(d) == sorted(ds)
```
