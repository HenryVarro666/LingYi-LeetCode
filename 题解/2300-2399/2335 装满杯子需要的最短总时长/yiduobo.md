---
title: "2335. 装满杯子需要的最短总时长"
aliases: ["yiduobo的每日leetcode 2235.装满杯子需要的最短总时长"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/559255190"
zhihu_id: "559255190"
zhihu_title: "yiduobo的每日leetcode 2235.装满杯子需要的最短总时长"
question_id: "2335"
question: "装满杯子需要的最短总时长"
problem_url: "https://leetcode.cn/problems/minimum-amount-of-time-to-fill-cups/"
difficulty: "Easy"
rating: 1360
title_number_fixed: ["2235→2335"]
created: "2022-08-30T00:50:16+08:00"
updated: "2022-08-30T00:50:16+08:00"
upvotes: 0
comments: 0
---

# 2335. 装满杯子需要的最短总时长

> **[yiduobo的每日leetcode 2235.装满杯子需要的最短总时长](https://zhuanlan.zhihu.com/p/559255190) · 知乎 · 2022-08-30 · 赞同 0**
> 力扣：[2335. 装满杯子需要的最短总时长](https://leetcode.cn/problems/minimum-amount-of-time-to-fill-cups/) · Easy · 灵茶山艾府：[结论题（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)
> 原文标题里的题号写作 2235，这里改成 2335：文章里的力扣链接和题名都对应这道题

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2235.装满杯子需要的最短总时长

[力扣](https://leetcode.cn/problems/minimum-amount-of-time-to-fill-cups/)

本题与之前做过的1753题思路完全一样，就是最终求解的东西略有不同。具体的可以参考

[yiduobo：yiduobo的每日leetcode 1753.移除石子的最大得分](https://zhuanlan.zhihu.com/p/458702976)

对于本题，需要总时长最短，因此理想的情况就是两杯一起接的次数尽可能多。相对地，1753题则是要求同时移除两块石头的次数尽可能多，所以说这两题的思路完全一样。

最后附上python代码：

```python
class Solution(object):
    def fillCups(self, amount):
        """
        :type amount: List[int]
        :rtype: int
        """

        s = sum(amount)
        ma = max(amount)

        if ma > s - ma:
            return ma
        else:
            return (s + 1) / 2
```
