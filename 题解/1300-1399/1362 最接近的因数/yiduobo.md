---
title: "1362. 最接近的因数"
aliases: ["yiduobo的每日leetcode 1362.最接近的因数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/399569583"
zhihu_id: "399569583"
zhihu_title: "yiduobo的每日leetcode 1362.最接近的因数"
question_id: "1362"
question: "最接近的因数"
problem_url: "https://leetcode.cn/problems/closest-divisors/"
created: "2021-08-13T21:16:24+08:00"
updated: "2021-08-13T21:16:24+08:00"
upvotes: 1
comments: 0
---

# 1362. 最接近的因数

> **[yiduobo的每日leetcode 1362.最接近的因数](https://zhuanlan.zhihu.com/p/399569583) · 知乎 · 2021-08-13 · 赞同 1**
> 力扣：[1362. 最接近的因数](https://leetcode.cn/problems/closest-divisors/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1362.最接近的因数

[力扣](https://leetcode-cn.com/problems/closest-divisors/)

对于num \= x \* (num / x)，为了使得x和num / x尽量接近，那么自然应该从sqrt(num)开始向下尝试，寻找第一个满足num % x \= 0的x，那么此时的x和num / x就是最接近的因数。

回到题目，这里只需要按上面的做法分别考察num + 1和num + 2的最接近因数，返回差值较小的那一组即可。

最后附上python代码：

```python
class Solution(object):
    def closestDivisors(self, num):
        """
        :type num: int
        :rtype: List[int]
        """

        x = int(sqrt(num + 1) + 0.5)
        while (num + 1) % x != 0:
            x -= 1
        
        res = [x, (num + 1) / x]
        min_diff = abs(x - (num + 1) / x)

        x = int(sqrt(num + 2) + 0.5)
        while (num + 2) % x != 0:
            x -= 1

        if abs(x - (num + 2) / x) < min_diff:
            res = [x, (num + 2) / x]
        
        return res
```
