---
title: "319. 灯泡开关"
aliases: ["yiduobo的每日leetcode 319.灯泡开关"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/159452266"
zhihu_id: "159452266"
zhihu_title: "yiduobo的每日leetcode 319.灯泡开关"
question_id: "319"
question: "灯泡开关"
problem_url: "https://leetcode.cn/problems/bulb-switcher/"
created: "2020-07-14T20:36:47+08:00"
updated: "2020-07-14T20:36:47+08:00"
upvotes: 0
comments: 0
---

# 319. 灯泡开关

> **[yiduobo的每日leetcode 319.灯泡开关](https://zhuanlan.zhihu.com/p/159452266) · 知乎 · 2020-07-14 · 赞同 0**
> 力扣：[319. 灯泡开关](https://leetcode.cn/problems/bulb-switcher/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

319.灯泡开关<https://leetcode-cn.com/problems/bulb-switcher/>

经典的数学题。

考察第k个灯泡，那么如果在1到k之间有奇数个数是k的约数，那么k最后就是亮着的，否则k就是灭的。而对于一个数而言，只有当这个数是完全平方数时，才会具有奇数个约数。

于是到了这里，题目就变成了求解1到n之间有多少个完全平方数，直接返回sqrt(n)即可。

最后附上python代码：

```python
class Solution(object):
    def bulbSwitch(self, n):
        """
        :type n: int
        :rtype: int
        """

        return int(sqrt(n))
```
