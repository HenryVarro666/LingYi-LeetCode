---
title: "1529. 灯泡开关IV"
aliases: ["yiduobo的每日leetcode 1529.灯泡开关IV"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/422966742"
zhihu_id: "422966742"
zhihu_title: "yiduobo的每日leetcode 1529.灯泡开关IV"
question_id: "1529"
question: "灯泡开关IV"
problem_url: "https://leetcode.cn/problems/bulb-switcher-iv/"
created: "2021-10-18T23:32:34+08:00"
updated: "2021-10-18T23:32:34+08:00"
upvotes: 0
comments: 0
---

# 1529. 灯泡开关IV

> **[yiduobo的每日leetcode 1529.灯泡开关IV](https://zhuanlan.zhihu.com/p/422966742) · 知乎 · 2021-10-18 · 赞同 0**
> 力扣：[1529. 灯泡开关IV](https://leetcode.cn/problems/bulb-switcher-iv/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1529.灯泡开关IV

[力扣](https://leetcode-cn.com/problems/bulb-switcher-iv/)

由于题目要求只能翻转从某个位置开始到末尾的这些灯泡，那么对于两个位置p和q，若p \< q，对p进行的翻转也将影响到q，而对q进行的翻转则不会影响到p，也就是说应该优先处理掉靠前的灯泡。

根据上面的结论，可以从左向右一趟扫描，对于当前位置index，设当前已经翻转了k次。由于翻转的操作都发生在index之前，也就意味着index这个位置也翻转了k次。当然，由于这里的翻转是在0和1之间变化，这里并不需要关心k具体是多少，而只需要关心k的奇偶性。

若当前的target[index]的奇偶性与k的奇偶性相同，那么当前位置就无需翻转，否则需要对当前位置进行一次翻转，此时应当更新答案，同时更新k的奇偶性。

最后附上python代码：

```python
class Solution(object):
    def minFlips(self, target):
        """
        :type target: str
        :rtype: int
        """

        now = 0
        res = 0
        for char in target:
            if now == int(char):
                continue
            else:
                res += 1
                now = 1 - now
        
        return res
```
