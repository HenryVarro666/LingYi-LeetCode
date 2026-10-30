---
title: "202. 快乐数"
aliases: ["yiduobo的每日leetcode 202.快乐数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/146352374"
zhihu_id: "146352374"
zhihu_title: "yiduobo的每日leetcode 202.快乐数"
question_id: "202"
question: "快乐数"
problem_url: "https://leetcode.cn/problems/happy-number/"
created: "2020-06-06T19:09:31+08:00"
updated: "2020-06-06T19:09:31+08:00"
upvotes: 0
comments: 0
---

# 202. 快乐数

> **[yiduobo的每日leetcode 202.快乐数](https://zhuanlan.zhihu.com/p/146352374) · 知乎 · 2020-06-06 · 赞同 0**
> 力扣：[202. 快乐数](https://leetcode.cn/problems/happy-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

202.快乐数<https://leetcode-cn.com/problems/happy-number/>

根据快乐数的计算方式，一个k位的数其下一个变换后得到的数最大为k \* 9 \* 9，于是可以确定如果快乐数循环起来，那么应该是在二位数到三位数之间循环，于是可以放心地开一个set记录过去算出来的结果，然后继续迭代直到变成1或者在set里出现过。

应该能有一些数学上的证明或者构造法之类的，不过这里简单起见就直接一个一个算了。

最后附上python代码：

```python
class Solution(object):
    def isHappy(self, n):
        """
        :type n: int
        :rtype: bool
        """

        num_set = set()
        num_set.add(n)
        while n != 1:
            now = n
            n = 0
            while now:
                n += (now % 10) ** 2
                now /= 10
            if n in num_set:
                return False
            num_set.add(n)
        
        return True
```
