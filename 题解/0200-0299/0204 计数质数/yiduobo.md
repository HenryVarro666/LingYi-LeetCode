---
title: "204. 计数质数"
aliases: ["yiduobo的每日leetcode 204.计数质数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/146539941"
zhihu_id: "146539941"
zhihu_title: "yiduobo的每日leetcode 204.计数质数"
question_id: "204"
question: "计数质数"
problem_url: "https://leetcode.cn/problems/count-primes/"
created: "2020-06-07T23:12:53+08:00"
updated: "2020-06-07T23:12:53+08:00"
upvotes: 0
comments: 0
---

# 204. 计数质数

> **[yiduobo的每日leetcode 204.计数质数](https://zhuanlan.zhihu.com/p/146539941) · 知乎 · 2020-06-07 · 赞同 0**
> 力扣：[204. 计数质数](https://leetcode.cn/problems/count-primes/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

204.计数质数<https://leetcode-cn.com/problems/count-primes/>

问题需要找出1到n之间的所有质数，求解这个问题数学上有好几种筛法，在实际运用中我见过的基本上是埃式筛法。

具体做法为令变量x从2开始循环到根号n：

1、若x为质数，那么将x \* 2，x \* 3，...，x \* k全部标记为合数。

2、若x为合数，则不进行任何操作。

最后当遍历完成后，2到n之间未被标记为合数的数即为质数。

时间复杂度为n / 2 + n / 3 + n / 5 + ...，印象中是渐进于nlogn的，需要用到素数分布定理然后用定积分来算，具体的计算方法我不太清楚。

最后附上python代码：

```python
class Solution(object):
    def countPrimes(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n < 2:
            return 0

        max_l = int(n ** 0.5)
        f = [1] * (n + 1)

        now = 2
        cnt = 0
        while now <= max_l:
            if f[now] == 1:
                tmp = now * now
                while tmp <= n:
                    f[tmp] = 0
                    tmp += now
            now += 1

        return sum(f[2 : n])
```
