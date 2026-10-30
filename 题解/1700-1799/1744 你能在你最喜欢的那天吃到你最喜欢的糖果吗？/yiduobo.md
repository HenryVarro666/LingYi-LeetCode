---
title: "1744. 你能在你最喜欢的那天吃到你最喜欢的糖果吗？"
aliases: ["yiduobo的每日leetcode 1744.你能在你最喜欢的那天吃到你最喜欢的糖果吗？"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/454223562"
zhihu_id: "454223562"
zhihu_title: "yiduobo的每日leetcode 1744.你能在你最喜欢的那天吃到你最喜欢的糖果吗？"
question_id: "1744"
question: "你能在你最喜欢的那天吃到你最喜欢的糖果吗？"
problem_url: "https://leetcode.cn/problems/can-you-eat-your-favorite-candy-on-your-favorite-day/"
created: "2022-01-07T00:18:57+08:00"
updated: "2022-01-07T00:18:58+08:00"
upvotes: 0
comments: 0
---

# 1744. 你能在你最喜欢的那天吃到你最喜欢的糖果吗？

> **[yiduobo的每日leetcode 1744.你能在你最喜欢的那天吃到你最喜欢的糖果吗？](https://zhuanlan.zhihu.com/p/454223562) · 知乎 · 2022-01-07 · 赞同 0**
> 力扣：[1744. 你能在你最喜欢的那天吃到你最喜欢的糖果吗？](https://leetcode.cn/problems/can-you-eat-your-favorite-candy-on-your-favorite-day/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1744.你能在你最喜欢的那天吃到你最喜欢的糖果吗？

[力扣](https://leetcode-cn.com/problems/can-you-eat-your-favorite-candy-on-your-favorite-day/)

这题目名字还真是够长的。。

言归正传。由于这里每一组询问之间都是相互独立的，那么可以分开来处理。不妨设现在考虑的是第i组询问。在这里很容易根据吃糖的上限和下限计算出第n天最多或者最少需要吃掉多少颗糖果。具体来说，每天最多吃dailyCap[i]颗糖果，因此第n天最多吃到第dailyCap[i] \* n颗糖果。相对的，每天至少吃一颗糖果，因此第n天至少需要吃掉n颗糖果。也就是说，只要第n到第n \* dailyCap[i]这些糖果当中有任何一颗想吃的糖果，那么就可以保证在第n天吃到想吃的糖果。

而对于想吃的糖果而言，其在所有糖果中第一次出现的位置first\[type\[i\]\]就等于

candiesCount[0] + candiesCount[1] + ... + candiesCount[favorateType[i] - 1] + 1

而最后一次出现的位置last\[type\[i\]\]则等于

candiesCount\[0\] + candiesCount\[1\] + ... + candiesCount\[favorateType\[i\]\]

可以发现上面是一个前缀和的式子，即first\[type\[i\]\] \= s\[type\[i\]\] + 1，last\[type\[i\]\] \= s\[type\[i\]\]，其中s表示candiesCount的前缀和。

到了这里，问题就变成了判断两个区间\[n, n \* dailyCap\[i\]\]与\[first\[type\[i\]\], last\[type\[i\]\]之间是否相交。不相交有两种情况，第一种是first\[type\[i\]\] > n \* dailyCap\[i\]，第二种则是last\[type\[i\]\] \< n。若满足其中之一，那么就吃不到最喜欢的糖果，否则就可以吃到。

根据上面的结论，就可以在预处理出first和last之后对每个询问逐个进行判断了。

最后附上python代码：

```python
class Solution(object):
    def canEat(self, candiesCount, queries):
        """
        :type candiesCount: List[int]
        :type queries: List[List[int]]
        :rtype: List[bool]
        """

        n = len(candiesCount)
        first = []
        last = []
        s = 0
        for candies in candiesCount:
            first.append(s + 1)
            s += candies
            last.append(s)
        
        res = []
        for t, d, c in queries:
            if first[t] > (d + 1) * c or last[t] < d + 1:
                res.append(False)
            else:
                res.append(True)
        
        return res
```
