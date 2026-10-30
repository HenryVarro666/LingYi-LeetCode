---
title: "1833. 雪糕的最大数量"
aliases: ["yiduobo的每日leecode 1833.雪糕的最大数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/counting-sort", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/468391472"
zhihu_id: "468391472"
zhihu_title: "yiduobo的每日leecode 1833.雪糕的最大数量"
question_id: "1833"
question: "雪糕的最大数量"
problem_url: "https://leetcode.cn/problems/maximum-ice-cream-bars/"
difficulty: "Medium"
rating: 1253
created: "2022-02-16T23:43:13+08:00"
updated: "2022-02-16T23:43:13+08:00"
upvotes: 0
comments: 0
---

# 1833. 雪糕的最大数量

> **[yiduobo的每日leecode 1833.雪糕的最大数量](https://zhuanlan.zhihu.com/p/468391472) · 知乎 · 2022-02-16 · 赞同 0**
> 力扣：[1833. 雪糕的最大数量](https://leetcode.cn/problems/maximum-ice-cream-bars/) · Medium · 灵茶山艾府：[从小到大贪心（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1833.雪糕的最大数量

[力扣](https://leetcode-cn.com/problems/maximum-ice-cream-bars/)

题目只要求买到的雪糕尽量多，但是没有要求必须把钱给花完，那么在这里显然应该先买便宜的。于是可以对雪糕按价格从小到大进行排序，然后一趟遍历，对于当前雪糕，若钱还够，那么就买下来，否则说明手上剩下的钱买不到剩下的任意雪糕了，可以直接返回买到的雪糕数量。

若能够正常推出循环，说明买下了所有的雪糕，此时返回雪糕的总数n。

最后附上python代码：

```python
class Solution(object):
    def maxIceCream(self, costs, coins):
        """
        :type costs: List[int]
        :type coins: int
        :rtype: int
        """

        n = len(costs)
        costs = sorted(costs)
        for index in range(n):
            if costs[index] <= coins:
                coins -= costs[index]
            else:
                return index
                
        return n
```
