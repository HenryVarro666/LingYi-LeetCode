---
title: "1648. 销售价值减少的颜色球"
aliases: ["yiduobo的每日leetcode 1648.销售价值减少的颜色球"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/440163061"
zhihu_id: "440163061"
zhihu_title: "yiduobo的每日leetcode 1648.销售价值减少的颜色球"
question_id: "1648"
question: "销售价值减少的颜色球"
problem_url: "https://leetcode.cn/problems/sell-diminishing-valued-colored-balls/"
created: "2021-12-01T23:11:30+08:00"
updated: "2021-12-01T23:11:30+08:00"
upvotes: 0
comments: 0
---

# 1648. 销售价值减少的颜色球

> **[yiduobo的每日leetcode 1648.销售价值减少的颜色球](https://zhuanlan.zhihu.com/p/440163061) · 知乎 · 2021-12-01 · 赞同 0**
> 力扣：[1648. 销售价值减少的颜色球](https://leetcode.cn/problems/sell-diminishing-valued-colored-balls/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1648.销售价值减少的颜色球

[力扣](https://leetcode-cn.com/problems/sell-diminishing-valued-colored-balls/)

从题目计算价值的方式来看，很明显每次都应该优先选择买现存数量最多的那种球。这里的球数量非常多，显然是不能一个一个来进行模拟的，那么一种很自然的想法就是将这些求按数量从大到小进行排序。对于当前数量最多的球，不妨设其有m个，且存在k种球都有m个，那么对于数量第二多的球n个而言，购买的顺序就应该是轮流买这k种球各一个，直到这k种球的数量都变为n为止。

对于每种球而言，从m个买到n个带来的价值就是m + (m - 1) + ... + (n + 1)，总和就是

(m + n + 1) \* (m - n) / 2

而这里有k种球都要这么买，因此总的价值就是

k \* (m + n + 1) \* (m - n) / 2

这一步操作一共买的球的个数为(m - n) \* k：

1、若这个数小于order，说明这些球必须全部买下来，因此可以将上面的价值累加到答案中，并更新m为n，同时寻找数组中个数等于n的数用来更新k，然后继续考察新的m、n和k

2、当这个数大于等于order时，说明在这个轮流买各一个的过程中就已经买到了足够的球，那么这里购买的轮次显然就是order / k，因此最终购买的价值就是m + (m - 1) + ... + (m - order / k + 1)，求和之后就是

k \* (m + m - order / k + 1) \* (order / k) / 2

当然，这里order不一定可以整除k，那么对于剩下的order % k这些球，则还需要进行一轮采购。此时剩下的各种球剩下的个数都是m - order / k，因此最后这些球产生的价值就是(m - order / k) \* (order % k)了

到了这一步就已经买到了足够的球，直接返回结果即可。

除此之外，注意到这里买球的形式，可以认为是找出一个最大的p，满足将所有个数大于p的球买到p个，然后从这些个数等于p个的球中补充剩下的恰好能达到order，其本质与数组中的第k大值完全一样，因此在这里使用快速选择算法可以在O(n)的时间复杂度内解决这个问题。不过具体实现的细节较多，我在这里偷懒，就还是用的上面O(nlogn)的排序做法。

最后附上python代码：

```python
class Solution(object):
    def maxProfit(self, inventory, orders):
        """
        :type inventory: List[int]
        :type orders: int
        :rtype: int
        """

        inventory.append(0)
        inventory.sort(reverse=True)
        now = inventory[0]
        mul = 1
        p = 1
        mod = 10 ** 9 + 7
        res = 0
        while p < len(inventory):
            while p < len(inventory) and now == inventory[p]:
                mul += 1
                p += 1
            if (now - inventory[p]) * mul < orders:
                res += (now + inventory[p] + 1) * (now - inventory[p]) / 2 * mul
                res %= mod
                orders -= (now - inventory[p]) * mul
                mul += 1
                now = inventory[p]
                p += 1
            else:
                offset = orders / mul
                target = now - offset + 1
                res += (now + target) * offset / 2 * mul
                res += (target - 1) * (orders % mul)
                res %= mod
                return res
```
