---
title: "3918. 区间内的质数和"
aliases: ["yiduobo的每日leetcode 3918.区间内的质数和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/number-theory", "leetcode/prefix-sum", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2034997043878424629"
zhihu_id: "2034997043878424629"
zhihu_title: "yiduobo的每日leetcode 3918.区间内的质数和"
question_id: "3918"
question: "数与其逆序数之间的质数和"
problem_url: "https://leetcode.cn/problems/sum-of-primes-between-number-and-its-reverse/"
difficulty: "Medium"
rating: 1301
created: "2026-05-05T14:08:45+08:00"
updated: "2026-05-05T14:08:45+08:00"
upvotes: 2
comments: 0
---

# 3918. 区间内的质数和

> **[yiduobo的每日leetcode 3918.区间内的质数和](https://zhuanlan.zhihu.com/p/2034997043878424629) · 知乎 · 2026-05-05 · 赞同 2**
> 力扣：[3918. 数与其逆序数之间的质数和](https://leetcode.cn/problems/sum-of-primes-between-number-and-its-reverse/) · Medium · 灵茶山艾府：[预处理 + 前缀和，O(log n) 时间（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3918.区间内的质数和

<https://leetcode.cn/problems/sum-of-primes-between-number-and-its-reverse/description/>

题目给出一个整数n。

令r表示将n的数字反转后得到的整数。

要求计算从min(n, r)到max(n, r)之间所有质数的总和。

通过模10除以10的方式将n的数位分离出来，在分离的过程中通过乘以10再加上当前位的方式计算得到r。

接下来从min(n, r)到max(n, r)一趟遍历，对于当前的v，若其不等于1，则从2到sqrt(v)遍历，检测其中是否存在v的约数。若不存在，说明v是质数，将其累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def sumOfPrimesInRange(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        r = 0
        x = n
        while x:
            r = r * 10 + x % 10
            x //= 10

        res = 0
        for v in range(min(r, n), max(r, n) + 1):
            if v == 1:
                continue
            
            x = 2
            flag = True
            while x * x <= v:
                if v % x == 0:
                    flag = False
                    break
                
                x += 1
            
            if flag:
                res += v
        
        return res
```
