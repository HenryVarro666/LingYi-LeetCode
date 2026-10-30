---
title: "2561. 重排水果"
aliases: ["yiduobo的每日leetcode 2561.重排水果"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/quickselect", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/640524894"
zhihu_id: "640524894"
zhihu_title: "yiduobo的每日leetcode 2561.重排水果"
question_id: "2561"
question: "重排水果"
problem_url: "https://leetcode.cn/problems/rearranging-fruits/"
difficulty: "Hard"
rating: 2222
created: "2023-06-30T02:01:25+08:00"
updated: "2023-06-30T02:01:25+08:00"
upvotes: 0
comments: 0
---

# 2561. 重排水果

> **[yiduobo的每日leetcode 2561.重排水果](https://zhuanlan.zhihu.com/p/640524894) · 知乎 · 2023-06-30 · 赞同 0**
> 力扣：[2561. 重排水果](https://leetcode.cn/problems/rearranging-fruits/) · Hard · 灵茶山艾府：[贪心及其证明（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2561.重排水果

[力扣](https://leetcode.cn/problems/rearranging-fruits/)

首先，若某种水果在两个果篮中的数量相同，那么就不需要交换这两种水果。反之，若其在某个果篮中的数量比另一个多出k个，那么就需要将其中的一半交换到另一个果篮中，也就是说这里的k必须为偶数，否则无解。

而对于具体的交换操作，第一种处理方法是两种需要交换的水果直接交换。对于这种交换方法，应该按水果成本排序后，让成本较小的水果与成本较大的水果配对交换。另一种处理方法则是使用一个成本最小的水果作为中间水果，先与一种水果交换，再与另一种水果交换。

根据上面这两个结论，就可以先分别遍历两个数组，使用一个哈希表统计每种水果在这两个果篮中的数量之差。接下来遍历这些水果，若某种水果的数量差为奇数，那么直接返回-1，反之将数量差一半的这种水果加入到待交换数组swap_list中。

得到swap_list后，将其从小到大进行排序，然后遍历swap_list的前半部分。对于当前遍历到的数swap_list[index]，将其与所有水果成本的最小值mi的两倍进行比较，将较小值累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, basket1, basket2):
        """
        :type basket1: List[int]
        :type basket2: List[int]
        :rtype: int
        """

        cnt = {}
        for v in basket1:
            cnt[v] = cnt.get(v, 0) + 1
        for v in basket2:
            cnt[v] = cnt.get(v, 0) - 1
        
        swap_list = []
        for v, freq in cnt.items():
            if freq % 2 != 0:
                return -1
            for _ in range(abs(freq) / 2):
                swap_list.append(v)
        
        mi = min(cnt.keys())
        swap_list.sort()
        res = 0
        for index in range(len(swap_list) / 2):
            res += min(mi * 2, swap_list[index])
        
        return res
```
