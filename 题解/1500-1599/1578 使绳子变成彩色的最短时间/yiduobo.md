---
title: "1578. 避免重复字母的最小删除成本"
aliases: ["yiduobo的每日leetcode 1578.避免重复字母的最小删除成本"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/滑动窗口与双指针", "题单/贪心算法", "题单/滑动窗口与双指针/六-分组循环", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/430011848"
zhihu_id: "430011848"
zhihu_title: "yiduobo的每日leetcode 1578.避免重复字母的最小删除成本"
question_id: "1578"
question: "使绳子变成彩色的最短时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-make-rope-colorful/"
difficulty: "Medium"
rating: 1574
created: "2021-11-05T22:55:18+08:00"
updated: "2021-11-05T22:55:18+08:00"
upvotes: 0
comments: 0
---

# 1578. 避免重复字母的最小删除成本

> **[yiduobo的每日leetcode 1578.避免重复字母的最小删除成本](https://zhuanlan.zhihu.com/p/430011848) · 知乎 · 2021-11-05 · 赞同 0**
> 力扣：[1578. 使绳子变成彩色的最短时间](https://leetcode.cn/problems/minimum-time-to-make-rope-colorful/) · Medium · 灵茶山艾府：[贪心，每段保留最大的（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1578.避免重复字母的最小删除成本

[力扣](https://leetcode-cn.com/problems/minimum-deletion-cost-to-avoid-repeating-letters/)

为了使得最终字符串中任意两个相邻字符都不一样，那么就是要将字符串中连续出现的字符都删到只剩下一个。为了使得成本最小，那么剩下的自然就是成本最大的那一个，换言之就是一旦遇到两个相同的相邻字符，那么必然是删去其中成本较小的那一个。

接下来就只需要一趟扫描，根据上面的原则执行删除就好了。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, s, cost):
        """
        :type s: str
        :type cost: List[int]
        :rtype: int
        """

        last = None
        last_cost = None
        n = len(cost)
        res = 0
        for index in range(n):
            if s[index] == last:
                if cost[index] < last_cost:
                    res += cost[index]
                else:
                    res += last_cost
                    last_cost = cost[index]
            else:
                last = s[index]
                last_cost = cost[index]
        
        return res
```
