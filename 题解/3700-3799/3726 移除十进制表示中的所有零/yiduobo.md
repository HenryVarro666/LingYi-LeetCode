---
title: "3726. 移除十进制表示中的所有零"
aliases: ["yiduobo的每日leetcode 3726.移除十进制表示中的所有零"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1965859072063538160"
zhihu_id: "1965859072063538160"
zhihu_title: "yiduobo的每日leetcode 3726.移除十进制表示中的所有零"
question_id: "3726"
question: "移除十进制表示中的所有零"
problem_url: "https://leetcode.cn/problems/remove-zeros-in-decimal-representation/"
difficulty: "Easy"
created: "2025-10-27T19:52:31+08:00"
updated: "2025-10-27T19:52:34+08:00"
upvotes: 2
comments: 0
---

# 3726. 移除十进制表示中的所有零

> **[yiduobo的每日leetcode 3726.移除十进制表示中的所有零](https://zhuanlan.zhihu.com/p/1965859072063538160) · 知乎 · 2025-10-27 · 赞同 2**
> 力扣：[3726. 移除十进制表示中的所有零](https://leetcode.cn/problems/remove-zeros-in-decimal-representation/) · Easy · 灵茶山艾府：[不用字符串的写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3726.移除十进制表示中的所有零

[3726. 移除十进制表示中的所有零 - 力扣（LeetCode）](https://leetcode.cn/problems/remove-zeros-in-decimal-representation/description/)

题目给出一个正整数n，要求返回一个整数，这个整数是n的十进制表示中所有零都被移除后得到的结果。

使用除以10模10的方案分离出n的所有数位，并丢弃掉其中值为0的数位。分离完成后，倒序遍历这些数位，将这些数位组装成答案即可。

最后附上python代码：

```python
class Solution(object):
    def removeZeros(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        digits = []
        while n:
            if n % 10 != 0:
                digits.append(n % 10)
            n //= 10
        
        res = 0
        for v in digits[::-1]:
            res = res * 10 + v
        return res
```
