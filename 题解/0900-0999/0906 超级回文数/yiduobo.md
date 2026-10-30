---
title: "906. 超级回文数"
aliases: ["yiduobo的每日leetcode 906.超级回文数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/354137209"
zhihu_id: "354137209"
zhihu_title: "yiduobo的每日leetcode 906.超级回文数"
question_id: "906"
question: "超级回文数"
problem_url: "https://leetcode.cn/problems/super-palindromes/"
created: "2021-03-02T23:00:34+08:00"
updated: "2021-03-02T23:00:34+08:00"
upvotes: 1
comments: 0
---

# 906. 超级回文数

> **[yiduobo的每日leetcode 906.超级回文数](https://zhuanlan.zhihu.com/p/354137209) · 知乎 · 2021-03-02 · 赞同 1**
> 力扣：[906. 超级回文数](https://leetcode.cn/problems/super-palindromes/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

906.超级回文数

[力扣](https://leetcode-cn.com/problems/super-palindromes/)

题目要求找出区间[l, r]之间的所有超级回文数，所谓超级回文数指的是对于一个数x，若x和x^2都是回文数，那么就说x^2是超级回文数。

注意到这里r最大为10^18，那么就意味着x最大也就10^9。由于x本身也必须是一个回文数，那么我们可以枚举x的前半部分，此时枚举的范围就进一步缩小到10^5了。

设枚举的前半部分为first，那么当first不是个位数时，first中每一位数字都不能大于2，否则x^2中将产生进位。由于进位都是向前进位，因此将破坏x^2的回文性质。

对于first，需要注意其形成的奇数位x以及偶数位x，例如对于122，其可以形成122221或者12221这两种情况。得到x之后，判断x^2是否处于l到r之间，且是否为回文数即可。

最后附上python代码：

```python
class Solution(object):
    def superpalindromesInRange(self, left, right):
        """
        :type left: str
        :type right: str
        :rtype: int
        """

        res = 0
        left = int(left)
        right = int(right)
        for first_part in range(1, 100000):
            first = str(first_part)
            l = len(first)
            flag = False
            for char in str(first):
                if char >= '3':
                    flag = True
                    break
            if l > 1 and flag:
                continue

            num = first + first[::-1]
            power = int(num) ** 2
            if left <= power and power <= right and str(power) == str(power)[::-1]:
                res += 1
            
            num = first[:l - 1] + first[::-1]
            power = int(num) ** 2
            if left <= power and power <= right and str(power) == str(power)[::-1]:
                res += 1

        return res
```
