---
title: "3959. 判定好整数"
aliases: ["yiduobo的每日leetcode 3959.判定好整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2049532821266490284"
zhihu_id: "2049532821266490284"
zhihu_title: "yiduobo的每日leetcode 3959.判定好整数"
question_id: "3959"
question: "判定好整数"
problem_url: "https://leetcode.cn/problems/check-good-integer/"
difficulty: "Easy"
created: "2026-06-14T16:47:41+08:00"
updated: "2026-06-14T16:47:42+08:00"
upvotes: 1
comments: 0
---

# 3959. 判定好整数

> **[yiduobo的每日leetcode 3959.判定好整数](https://zhuanlan.zhihu.com/p/2049532821266490284) · 知乎 · 2026-06-14 · 赞同 1**
> 力扣：[3959. 判定好整数](https://leetcode.cn/problems/check-good-integer/) · Easy · 灵茶山艾府：[不用字符串的做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3959.判定好整数

<https://leetcode.cn/problems/check-good-integer/description/>

题目给出一个正整数n。

令digitSum表示n的各位数字之和，令squareSum表示n的各位数字平方之和。

若一个整数squareSum - digitSum >\= 50，则称它为好整数。

若n是好整数，则返回true，否则返回false。

通过模10除以10的方法分离出n的每位数字，然后按照题目描述分别计算出squareSum和digitSum，最后判断前者减去后者是否大于等于50即可。

最后附上python代码：

```python
class Solution(object):
    def checkGoodInteger(self, n):
        """
        :type n: int
        :rtype: bool
        """
        
        ds = 0
        ss = 0

        while n:
            d = n % 10
            n //= 10
            ds += d
            ss += d * d
        
        return ss - ds >= 50
```
