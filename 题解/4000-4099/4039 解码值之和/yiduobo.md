---
title: "4039. 解码值之和"
aliases: ["yiduobo的每日leetcode 4039.解码值之和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/number-theory"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2078980205436212177"
zhihu_id: "2078980205436212177"
zhihu_title: "yiduobo的每日leetcode 4039.解码值之和"
question_id: "4039"
question: "解码值之和"
problem_url: "https://leetcode.cn/problems/sum-of-decoded-numbers/"
difficulty: "Medium"
created: "2026-09-03T23:04:15+08:00"
updated: "2026-09-03T23:04:15+08:00"
upvotes: 1
comments: 0
---

# 4039. 解码值之和

> **[yiduobo的每日leetcode 4039.解码值之和](https://zhuanlan.zhihu.com/p/2078980205436212177) · 知乎 · 2026-09-03 · 赞同 1**
> 力扣：[4039. 解码值之和](https://leetcode.cn/problems/sum-of-decoded-numbers/) · Medium · 灵茶山艾府：[不用字符串的做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4039.解码值之和

<https://leetcode.cn/problems/sum-of-decoded-numbers/description/>

题目给出一个整数数组nums。

每个nums[index]都是一个编码后的整数，表示两个正整数x[index]与y[index]。要解码nums[index]，定义：

- width[index] \= nums[index] % 10
- d[index] \= nums[index] // 10，这里的除法是整除
- x[index]为d[index]的十进制表示中，前width[index]位数组组成的整数
- y[index]为d[index]的十进制表示中，剩余所有数字组成的整数

保证d[index]的十进制表示包含的数字位数大于width[index]，也就是说，x[index]与y[index]都至少包含一位数组，而nums[index]的解码值就是x[index]^y[index]。

要求返回nums中所有元素的解码值之和，结果对10^9 + 7取模。

直接遍历nums，对于其中每个元素，按照题目描述模拟计算解码值并累加到答案中即可。

具体来说，对于当前的元素v，先模10取出w，然后除以10。接下来，通过模10除以10的方法分离出数位数组d，然后将d反转，通过前w位构造出x，剩余的数位构造出y，最后利用快速幂计算x^y并累加到答案中。

最后附上python代码：

```python
class Solution(object):
    def sumDecoded(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        def quick_power(base, p, mod):
            if p == 0:
                return 1
            if p == 1:
                return base % mod
            
            x = quick_power(base, p // 2, mod)
            x = x * x % mod
            if p & 1:
                x = x * base % mod
            return x

        res = 0
        mod = 10 ** 9 + 7
        for v in nums:
            w = v % 10
            v //= 10

            d = []
            while v:
                d.append(v % 10)
                v //= 10

            d.reverse()
            x = 0
            for index in range(w):
                x = x * 10 + d[index]
            
            y = 0
            for index in range(w, len(d)):
                y = y * 10 + d[index]
            
            res += quick_power(x, y, mod)
            if res >= mod:
                res -= mod
        
        return res
```
