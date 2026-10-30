---
title: "3765. 完全质数"
aliases: ["yiduobo的每日leetcode 3765.完全质数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/enumeration", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1981114672460604835"
zhihu_id: "1981114672460604835"
zhihu_title: "yiduobo的每日leetcode 3765.完全质数"
question_id: "3765"
question: "完全质数"
problem_url: "https://leetcode.cn/problems/complete-prime-number/"
difficulty: "Medium"
rating: 1378
created: "2025-12-07T21:45:18+08:00"
updated: "2025-12-07T21:45:19+08:00"
upvotes: 1
comments: 0
---

# 3765. 完全质数

> **[yiduobo的每日leetcode 3765.完全质数](https://zhuanlan.zhihu.com/p/1981114672460604835) · 知乎 · 2025-12-07 · 赞同 1**
> 力扣：[3765. 完全质数](https://leetcode.cn/problems/complete-prime-number/) · Medium · 灵茶山艾府：[如何判断质数？（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3765.完全质数

[3765. 完全质数 - 力扣（LeetCode）](https://leetcode.cn/problems/complete-prime-number/description/)

题目给出一个整数num，大小在1到10^9之间。

若num的所有前缀和所有后缀都是质数，那么就称这个数为完全质数。

若num为完全质数，则返回true，否则返回false。

由于num的大小不超过10^9，那么其前缀和后缀最多只有20个，同时每个前缀或后缀都不会超过num的大小，也就是说对于一个前缀或者后缀v，可以通过枚举2到sqrt(v)中的所有元素x，判断v是否为x的倍数来确定v是否为质数。

具体实现上，可以先通过模10除以10的方法分离出num的所有数位。

对于num的后缀，最后k位形成的后缀，就等于最后k - 1位形成的后缀，再加上digits[k - 1] \* 10^(k - 1)。于是只需一趟遍历，一边计算10的幂次，一边利用上一轮的后缀值来更新当前的后缀值，然后检测其是否为质数。

对于num的前缀，则可以倒序遍历digits，那么前k位形成的前缀，就等于前k - 1形成的前缀乘以10，再加上digits[-k]，同样只需一趟遍历，利用上一轮的前缀值来更新当前的前缀值，然后检测其是否为质数。

最后附上python代码：

```python
class Solution(object):
    def completePrime(self, num):
        """
        :type num: int
        :rtype: bool
        """
        
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        
        def check(v):
            if v == 1:
                return False
            
            x = 2
            while x * x <= v:
                if v % x == 0:
                    return False
                x += 1
            
            return True

        v = 0
        p10 = 1
        for d in digits:
            v = v + p10 * d
            p10 *= 10
            if not check(v):
                return False
        
        v = 0
        for d in digits[::-1]:
            v = v * 10 + d
            if not check(v):
                return False
        
        return True
```
