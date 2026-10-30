---
title: "818. 赛车"
aliases: ["yiduobo的每日leetcode 818.赛车"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343837239"
zhihu_id: "343837239"
zhihu_title: "yiduobo的每日leetcode 818.赛车"
question_id: "818"
question: "赛车"
problem_url: "https://leetcode.cn/problems/race-car/"
created: "2021-01-16T19:18:52+08:00"
updated: "2021-01-16T19:18:52+08:00"
upvotes: 1
comments: 0
---

# 818. 赛车

> **[yiduobo的每日leetcode 818.赛车](https://zhuanlan.zhihu.com/p/343837239) · 知乎 · 2021-01-16 · 赞同 1**
> 力扣：[818. 赛车](https://leetcode.cn/problems/race-car/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

818.赛车

[力扣](https://leetcode-cn.com/problems/race-car/)

首先可以明确的一点是，每次速度翻倍，那么在当前方向上累积走的距离就是2^k - 1。

接下来，令f[x]表示从0开始走到x需要的最少操作次数，那么：

1、若x本身就等于2^k - 1，那么就只要k步就能走到

2、若x不等于2^k - 1，那么就有两种走法：

2-1）可以先走到2^p - 1，然后往回走，这里的2^p - 1是最小的大于x的数。那么此时就先使用了p次前进操作和1次转向操作，然后将问题转换成了从0开始走到2^p - 1 - x。于是有

f[x] \= f[2^p - 1 - x] + p + 1

2-2）当然也可以尽可能地正向走，即选择走p - 1步。这里选择p - 1的理由是如果不采用2-1中的往回走，那么想要走到2^(p - 1) - 1，如果不是直接走p - 1步那么就至少需要走两次2^(p - 2) - 1和一次1，以及额外的转向操作，显然是不如直接走到2^(p - 1) - 1。在走到2^(p - 1) - 1之后，此时可以选择往回走。这里往回走的距离则在0到2^(p - 2) - 1之间，于是有

f\[now\] \= min(f\[now\], f\[now - (2^(p - 1) -1) + power\[index\]\] + (p - 1) + 1 + index + 1)

这里的index取值在0到p - 2之间，(p - 1) + 1表示走p - 1步之后转向，index + 1则表示往回走index步之后再转向。这里的第二次转向是必需的，因为这里第一次转向时尚未走到now，那么第二次转向之前也必须要往正向走一段，因此需要第二次转向。

最后附上python代码：

```python
class Solution(object):
    def racecar(self, target):
        """
        :type target: int
        :rtype: int
        """

        power = [0]
        while power[-1] < target:
            power.append(power[-1] + power[-1] + 1)
        
        f = [None] * (target + 1)
        f[0] = 0
        for now in range(1, target + 1):
            p = 0
            while power[p] < now:
                p += 1
            if now == power[p]:
                f[now] = p
            else:
                f[now] = f[power[p] - now] + p + 1
                for index in range(p):
                    f[now] = min(f[now], f[now - power[p - 1] + power[index]] + p + index + 1)
        
        return f[-1]
```
