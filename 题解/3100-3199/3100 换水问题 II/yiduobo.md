---
title: "3100. 换水问题II"
aliases: ["yiduobo的每日leetcode 3100.换水问题II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/699858257"
zhihu_id: "699858257"
zhihu_title: "yiduobo的每日leetcode 3100.换水问题II"
question_id: "3100"
question: "换水问题 II"
problem_url: "https://leetcode.cn/problems/water-bottles-ii/"
difficulty: "Medium"
created: "2024-05-26T00:18:52+08:00"
updated: "2024-05-26T00:18:52+08:00"
upvotes: 0
comments: 0
---

# 3100. 换水问题II

> **[yiduobo的每日leetcode 3100.换水问题II](https://zhuanlan.zhihu.com/p/699858257) · 知乎 · 2024-05-26 · 赞同 0**
> 力扣：[3100. 换水问题 II](https://leetcode.cn/problems/water-bottles-ii/) · Medium · 灵茶山艾府：[两种方法：模拟 / O(1) 数学公式（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3100.换水问题II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/water-bottles-ii/)

题目的数据规模很小，可以直接模拟。

记full为手上当前没喝的，empty为手上的空瓶子数量，那么：

1、若手上还有没喝的，就全部喝掉，此时需要将full分别累加到答案和empty中，然后将full清零。

2、若此时的empty大于等于numExchange，那么就将其减去numExchange并将full加上1，表示换了一瓶，另外按照题目要求，此时还需要将numExchange额外加上1。

重复上面的过程直到full为0且empty小于numExchange为止。

最后附上python代码：

```python
class Solution(object):
    def maxBottlesDrunk(self, numBottles, numExchange):
        """
        :type numBottles: int
        :type numExchange: int
        :rtype: int
        """

        full = numBottles
        empty = 0
        res = 0
        while full > 0 or empty >= numExchange:
            if full > 0:
                empty += full
                res += full
                full = 0
            
            if empty >= numExchange:
                full += 1
                empty -= numExchange
                numExchange += 1
        
        return res
```
