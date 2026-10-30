---
title: "2521. 数组乘积中的不同质因数数目"
aliases: ["yiduobo的每日leetcode 2521.数组乘积中的不同质因数数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/634863216"
zhihu_id: "634863216"
zhihu_title: "yiduobo的每日leetcode 2521.数组乘积中的不同质因数数目"
question_id: "2521"
question: "数组乘积中的不同质因数数目"
problem_url: "https://leetcode.cn/problems/distinct-prime-factors-of-product-of-array/"
difficulty: "Medium"
rating: 1413
created: "2023-06-09T22:49:04+08:00"
updated: "2023-06-09T22:49:04+08:00"
upvotes: 0
comments: 0
---

# 2521. 数组乘积中的不同质因数数目

> **[yiduobo的每日leetcode 2521.数组乘积中的不同质因数数目](https://zhuanlan.zhihu.com/p/634863216) · 知乎 · 2023-06-09 · 赞同 0**
> 力扣：[2521. 数组乘积中的不同质因数数目](https://leetcode.cn/problems/distinct-prime-factors-of-product-of-array/) · Medium · 灵茶山艾府：[分解质因数](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2521.数组乘积中的不同质因数数目

[力扣](https://leetcode.cn/problems/distinct-prime-factors-of-product-of-array/)

题目给出一个数组，要求找出数组中所有数的乘积包含哪些质因子。对于这个问题，只需找出数组中每个数包含的质因子，利用集合给这些质因子去重就行了。

对于寻找质因子这个操作，对于本题的数据规模可以直接暴力计算。我在这里采用的是先执行一次筛法，找出每个数最大的质因子，然后对于数组中的每个数通过这个最大值质因子来分解质因数。

最后附上python代码：

```python
class Solution(object):
    def distinctPrimeFactors(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        f = range(1001)

        x = 2
        while x * x <= 1000:
            if f[x] == x:
                now = x + x
                while now <= 1000:
                    f[now] = x
                    now += x
            
            x += 1
        
        prime = set()
        for num in nums:
            while num > 1:
                prime.add(f[num])
                num /= f[num]

        return len(prime)
```
