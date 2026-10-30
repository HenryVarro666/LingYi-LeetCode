---
title: "3536. 两个数字的最大乘积"
aliases: ["yiduobo的每日leetcode 3536.两个数字的最大乘积"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/math", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1905764359092806267"
zhihu_id: "1905764359092806267"
zhihu_title: "yiduobo的每日leetcode 3536.两个数字的最大乘积"
question_id: "3536"
question: "两个数字的最大乘积"
problem_url: "https://leetcode.cn/problems/maximum-product-of-two-digits/"
difficulty: "Easy"
created: "2025-05-16T22:00:39+08:00"
updated: "2025-05-16T22:00:39+08:00"
upvotes: 1
comments: 0
---

# 3536. 两个数字的最大乘积

> **[yiduobo的每日leetcode 3536.两个数字的最大乘积](https://zhuanlan.zhihu.com/p/1905764359092806267) · 知乎 · 2025-05-16 · 赞同 1**
> 力扣：[3536. 两个数字的最大乘积](https://leetcode.cn/problems/maximum-product-of-two-digits/) · Easy · 灵茶山艾府：[两种写法：排序 / 维护最大次大（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3536.两个数字的最大乘积

<https://leetcode.cn/problems/maximum-product-of-two-digits/description/>

题目给出一个大于等于10的正整数n，要求找出其中任意两位数字相乘可以得到的最大乘积。

为了使得乘积最大，使用的两个数位就应该是最大的两个，于是只需不断通过模10除10的方法分离n的所有数位，在这个过程中记录最大的两个，分离完成后将这两个数位相乘即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxProduct(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        first, second = None, None
        while n:
            digit = n % 10
            n //= 10

            if first is None or first < digit:
                first, second = digit, first
            elif second is None or second < digit:
                second = digit

        return first * second
```
