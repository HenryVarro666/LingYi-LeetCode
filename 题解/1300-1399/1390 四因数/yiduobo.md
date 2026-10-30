---
title: "1390. 四因数"
aliases: ["yiduobo的每日leetcode 1390.四因数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/403605787"
zhihu_id: "403605787"
zhihu_title: "yiduobo的每日leetcode 1390.四因数"
question_id: "1390"
question: "四因数"
problem_url: "https://leetcode.cn/problems/four-divisors/"
difficulty: "Medium"
rating: 1478
created: "2021-08-25T23:34:37+08:00"
updated: "2021-08-25T23:34:37+08:00"
upvotes: 0
comments: 0
---

# 1390. 四因数

> **[yiduobo的每日leetcode 1390.四因数](https://zhuanlan.zhihu.com/p/403605787) · 知乎 · 2021-08-25 · 赞同 0**
> 力扣：[1390. 四因数](https://leetcode.cn/problems/four-divisors/) · Medium · 灵茶山艾府：[【模板】预处理每个数的因子个数、因子和（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1390.四因数

[力扣](https://leetcode-cn.com/problems/four-divisors/)

首先，1必然不是合法答案，而对于一个大于等于2的正整数num，将其因式分解后可以写成

num \= (x[0]^k[0]) \* (x[1]^k[1]) \* ... \* (x[n]^k[n])

其中x都是质数，k都是正整数。

利用组合数学的只是，可以得出num一共就有(k[0] + 1) \* (k[1] + 1) \* ... \* (k[n] + 1)

为了使得这个式子计算的结果为4，那么一共有两种可能：

1、k[0] \= 3，且没有其他因数。这种情况下，就有num \= x^3，也就是说num是一个完全立方数。

2、k[0] \= 1且k[1] \= 1。这种情况下，就有num \= x[0] \* x[1]，这里的x[0]和x[1]都是质数，且x[0] !\= x[1]。

根据上面的结论，我们可以先通过筛法求出100000之内的所有质数。在执行筛法的过程中，可以对于每个数num记录下其最大的非num的质因数，记为f[num]。然后对于当前的num，设tmp \= f[num]，那么：

1、若f[tmp] \= f[num]，且tmp \= f[num] \* f[num]，那么说明num \= f[num]^3，即num为一个完全立方数，此时应该将答案加上1 + f[num] + tmp + num

2、若f[tmp] \= 1，且tmp !\= f[num]，此时就满足条件2中的num \= tmp \* f[num]，且num和f[num]都是质数，二者也不相等，那么说明num也是一个符合要求的答案，同样应该将答案加上1 + f[num] + tmp + num

最后附上python代码：

```python
class Solution(object):
    def sumFourDivisors(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        max_num = max(nums)

        f = [1] * (max_num + 1)
        now = 2
        while now * now <= max_num:
            if f[now] == 1:
                tmp = now + now
                while tmp <= max_num:
                    f[tmp] = now
                    tmp += now
            now += 1

        res = 0
        for num in nums:
            if f[num] == 1:
                continue
            
            tmp = num / f[num]
            if (f[tmp] == 1 and tmp != f[num]) or (f[tmp] == f[num] and tmp / f[num] == f[num]):
                res += 1 + num + tmp + f[num]
        
        return res
```
