---
title: "2861. 最大合金数"
aliases: ["yiduobo的每日leetcode 2861.最大合金数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/661480945"
zhihu_id: "661480945"
zhihu_title: "yiduobo的每日leetcode 2861.最大合金数"
question_id: "2861"
question: "最大合金数"
problem_url: "https://leetcode.cn/problems/maximum-number-of-alloys/"
difficulty: "Medium"
rating: 1981
created: "2023-10-16T00:56:14+08:00"
updated: "2023-10-16T00:56:14+08:00"
upvotes: 1
comments: 0
---

# 2861. 最大合金数

> **[yiduobo的每日leetcode 2861.最大合金数](https://zhuanlan.zhihu.com/p/661480945) · 知乎 · 2023-10-16 · 赞同 1**
> 力扣：[2861. 最大合金数](https://leetcode.cn/problems/maximum-number-of-alloys/) · Medium · 灵茶山艾府：[二分答案，附题单（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2861.最大合金数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-number-of-alloys/)

题目要求所有合金都由一台机器完成，那么在这里就没有调度这一说了，只需遍历每台机器，计算当前机器可以生产的最大合金数，取其中的最大值作为最终答案即可。

对于单台机器而言，生产越多就越困难，因此在这里可以二分最后可以生产的最大合金数，二分的下界自然是0，而上界则需要取budget与stocks中最大值这二者之和，因为单个零件的单价最便宜也是1块钱，所以budget最多能买的零件数量就是budget，极限情况下就可以得到budget + max(stocks)个特定零件。

确定了二分上下界之后开始进行二分。对于当前二分到的mid，首先通过composition计算当前机器生产mid个合金需要的零件数量数组need，然后通过need和stock计算出需要额外购买的零件数量数组buy，最后通过buy和cost计算出所需的金额tot_cost。若tot_cost不超过budget，那么就更新二分的下界为mid，否则更新二分的上界为mid - 1。

二分完成后，当前的二分下界就是当前机器可以生产的合金数量，使用这个值更新答案然后继续考虑下一台机器。

最后附上python代码：

```python
class Solution(object):
    def maxNumberOfAlloys(self, n, k, budget, composition, stock, cost):
        """
        :type n: int
        :type k: int
        :type budget: int
        :type composition: List[List[int]]
        :type stock: List[int]
        :type cost: List[int]
        :rtype: int
        """

        res = 0
        for index in range(k):
            left = 0
            right = budget + max(stock)
            while left < right:
                mid = (left + right + 1) / 2
                need = [x * mid for x in composition[index]]
                buy = [max(0, x - y) for x, y in zip(need, stock)]
                tot_cost = sum([x * y for x, y in zip(buy, cost)])
                if tot_cost <= budget:
                    left = mid
                else:
                    right = mid - 1
            
            res = max(res, left)
        
        return res
```
