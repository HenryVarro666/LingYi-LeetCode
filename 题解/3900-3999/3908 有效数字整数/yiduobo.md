---
title: "3908. 有效数字"
aliases: ["yiduobo的每日leetcode 3908.有效数字"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2031846714022311348"
zhihu_id: "2031846714022311348"
zhihu_title: "yiduobo的每日leetcode 3908.有效数字"
question_id: "3908"
question: "有效数字整数"
problem_url: "https://leetcode.cn/problems/valid-digit-number/"
difficulty: "Easy"
created: "2026-04-26T21:29:23+08:00"
updated: "2026-04-26T21:29:23+08:00"
upvotes: 0
comments: 0
---

# 3908. 有效数字

> **[yiduobo的每日leetcode 3908.有效数字](https://zhuanlan.zhihu.com/p/2031846714022311348) · 知乎 · 2026-04-26 · 赞同 0**
> 力扣：[3908. 有效数字整数](https://leetcode.cn/problems/valid-digit-number/) · Easy · 灵茶山艾府：[不用字符串的做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3908.有效数字

<https://leetcode.cn/problems/valid-digit-number/description/>

题目给出一个整数n以及一个数字x。

若一个数字中包含至少一个x，且这个数字不以x开头，那么就称其是有效的。

问n是否是有效的数字。

通过模10除以10的方法分离n中的所有数位，直到其小于10为止。若分离过程中出现了x，且最后剩下的元素不等于x，那么就说明n是有效的。

最后附上python代码：

```python
class Solution(object):
    def validDigit(self, n, x):
        """
        :type n: int
        :type x: int
        :rtype: bool
        """
        
        flag = False
        while n >= 10:
            if n % 10 == x:
                flag = True
            n //= 10
        
        return flag and n != x
```
