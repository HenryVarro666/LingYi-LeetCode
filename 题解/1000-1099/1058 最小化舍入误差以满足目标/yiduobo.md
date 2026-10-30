---
title: "1058. 最小化舍入误差以满足目标"
aliases: ["yiduobo的每日leetcode 1058.最小化舍入误差以满足目标"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/607305159"
zhihu_id: "607305159"
zhihu_title: "yiduobo的每日leetcode 1058.最小化舍入误差以满足目标"
question_id: "1058"
question: "最小化舍入误差以满足目标"
problem_url: "https://leetcode.cn/problems/minimize-rounding-error-to-meet-target/"
created: "2023-02-17T23:19:31+08:00"
updated: "2023-02-17T23:19:31+08:00"
upvotes: 0
comments: 0
---

# 1058. 最小化舍入误差以满足目标

> **[yiduobo的每日leetcode 1058.最小化舍入误差以满足目标](https://zhuanlan.zhihu.com/p/607305159) · 知乎 · 2023-02-17 · 赞同 0**
> 力扣：[1058. 最小化舍入误差以满足目标](https://leetcode.cn/problems/minimize-rounding-error-to-meet-target/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1058.最小化舍入误差以满足目标

[力扣](https://leetcode.cn/problems/minimize-rounding-error-to-meet-target/)

首先，对于小数位上都为0的数x，都有floor(x) \= ceil(x)，也就意味着对于这类数并没有操作空间，因此可以在一开始就将这些数给移除出去，同时让target减去这些x。

接下来，对于剩下的数p，都有floor(p) \= ceil(p) - 1，因此此时可以得到的最小值就是

mi \= floor(p1) + floor(p2) + ... + floor(pn)

最大值则是

ma \= ceil(p1) + ceil(p2) + ... + ceil(pn) \= mi + n

那么在这里就需要满足

mi \<\= target \<\= ma \= mi + n

若不满足这个条件，直接返回-1。

若满足这个条件，则说明可以将mi中的若干项从floor变为ceil，而需要变换的项数就是k \= target - mi。

为了使得变换的代价最小，在这里就是要将从floor(p)变为ceil(p)所需代价最小的k项进行变换，于是可以先一趟遍历，将所有p变为floor(p)所需的代价累加起来得到最初的代价res，同时使用一个数组cost将floor(p)变为ceil(p)的代价也记录下来。遍历完成后，将cost从小到大进行排序，然后取top k累加到res当中即可。

最后附上python代码：

```python
class Solution(object):
    def minimizeError(self, prices, target):
        """
        :type prices: List[str]
        :type target: int
        :rtype: str
        """

        res = 0
        cost = []
        for p in prices:
            p = float(p)
            if math.floor(p) != math.ceil(p):
                res += p - math.floor(p)
                cost.append(math.ceil(p) - p - (p - math.floor(p)))
            
            target -= int(math.floor(p))
        
        if target < 0:
            return "-1"
        
        if target > len(cost):
            return "-1"

        cost.sort()
        res += sum(cost[:target])
        return "%.3f" % res
```
