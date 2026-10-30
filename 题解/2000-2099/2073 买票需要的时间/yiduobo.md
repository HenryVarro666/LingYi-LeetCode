---
title: "2073. 买票需要的时间"
aliases: ["yiduobo的每日leetcode 2073.买票需要的时间"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/516496335"
zhihu_id: "516496335"
zhihu_title: "yiduobo的每日leetcode 2073.买票需要的时间"
question_id: "2073"
question: "买票需要的时间"
problem_url: "https://leetcode.cn/problems/time-needed-to-buy-tickets/"
difficulty: "Easy"
created: "2022-05-18T20:57:23+08:00"
updated: "2022-05-18T20:57:23+08:00"
upvotes: 0
comments: 0
---

# 2073. 买票需要的时间

> **[yiduobo的每日leetcode 2073.买票需要的时间](https://zhuanlan.zhihu.com/p/516496335) · 知乎 · 2022-05-18 · 赞同 0**
> 力扣：[2073. 买票需要的时间](https://leetcode.cn/problems/time-needed-to-buy-tickets/) · Easy · 灵茶山艾府：[O(n) 一次遍历，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2073.买票需要的时间

[力扣](https://leetcode.cn/problems/time-needed-to-buy-tickets/)

对于第k个人，其买到票的轮次是第tickets[k]轮，那么在其他人需求的票都足够多的情况下，一共是n个人先买tickets[k] - 1轮票，然后第0到第k个人再买一轮票后第k个人才能买到全部的票，此时需要的时间就是n \* (tickets[k] - 1) + k + 1的时间。

需要注意的是，队伍中某些人需求的票可能不足预想的轮次，因此可以节省下一些时间。按照上面的计算的方法，第0到第k - 1个人需要买足tickets[k]张票，但是这些人需求的票如果小于tickets[k]的话，实际上就多算了一些时间，需要在上面的答案中减去差值。同样的，第k + 1到第n - 1个人需要买足tickets[k] - 1张票，若这些人需求的票小于tickets[k] - 1，同样需要在答案中减去差值。

最后附上python代码：

```python
class Solution(object):
    def timeRequiredToBuy(self, tickets, k):
        """
        :type tickets: List[int]
        :type k: int
        :rtype: int
        """

        n = len(tickets)
        res = n * (tickets[k] - 1) + k + 1

        for index in range(k):
            if tickets[index] < tickets[k]:
                res -= tickets[k] - tickets[index]
        
        for index in range(k + 1, n):
            if tickets[index] < tickets[k] - 1:
                res -= tickets[k] - 1 - tickets[index]
        
        return res
```
