---
title: "991. 坏了的计算器"
aliases: ["yiduobo的每日leetcode 991.坏了的计算器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/364620798"
zhihu_id: "364620798"
zhihu_title: "yiduobo的每日leetcode 991.坏了的计算器"
question_id: "991"
question: "坏了的计算器"
problem_url: "https://leetcode.cn/problems/broken-calculator/"
created: "2021-04-13T22:52:27+08:00"
updated: "2021-04-13T22:52:27+08:00"
upvotes: 0
comments: 0
---

# 991. 坏了的计算器

> **[yiduobo的每日leetcode 991.坏了的计算器](https://zhuanlan.zhihu.com/p/364620798) · 知乎 · 2021-04-13 · 赞同 0**
> 力扣：[991. 坏了的计算器](https://leetcode.cn/problems/broken-calculator/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

991.坏了的计算器

[力扣](https://leetcode-cn.com/problems/broken-calculator/)

由于X是大于0的，那么对于题目中给出的两种操作，乘以2只会让X变大，减1则会让X变小。若某一时刻出现了X大于Y的情况，此时就应该不断执行减1直到X等于Y。接下来讨论X小于Y的情况。

由于X小于Y，那么至少需要执行一次乘以2，那么很明显在乘以2之后不应该出现两次连续的减1操作，理由很简单，对于X \* 2 -1 - 1这个操作序列而言，(X - 1) \* 2显然是更好的选择。

有了这两个结论，我们就可以从Y开始倒推：

1、当X大于等于Y时，还需要执行(X - Y)次减1操作，因此将答案加上(X - Y)然后返回即可

2、当X小于Y，且Y为偶数时。此时操作序列的最后一步必然不会是减1，因为Y是偶数，而X在执行最后一次乘以2操作之后也会是偶数，期间如果有减1操作那么必然是偶数次的减1操作，与上面的结论相矛盾。因此当Y为偶数时，操作序列的最后一步必然是乘以2，那么此时将答案加1，然后问题就变成了从X变换到Y/2需要多少步。

3、当X小于Y，且Y为奇数时。此时操作序列的最后一步显然是减1，因此此时将答案加1，然后问题就变成了从X变换到Y + 1需要多少步。

最后附上python代码：

```python
class Solution(object):
    def brokenCalc(self, X, Y):
        """
        :type X: int
        :type Y: int
        :rtype: int
        """

        res = 0
        while Y != X:
            if X >= Y:
                res += X - Y
                break
            if Y & 1:
                Y += 1
            else:
                Y /= 2
            res += 1
        
        return res
```
