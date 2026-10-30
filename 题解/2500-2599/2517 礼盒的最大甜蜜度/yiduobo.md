---
title: "2517. 礼盒的最大甜度"
aliases: ["yiduobo的每日leetcode 2517.礼盒的最大甜度"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/binary-search", "leetcode/sorting", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/634853739"
zhihu_id: "634853739"
zhihu_title: "yiduobo的每日leetcode 2517.礼盒的最大甜度"
question_id: "2517"
question: "礼盒的最大甜蜜度"
problem_url: "https://leetcode.cn/problems/maximum-tastiness-of-candy-basket/"
difficulty: "Medium"
rating: 2021
created: "2023-06-07T23:22:40+08:00"
updated: "2023-06-07T23:22:40+08:00"
upvotes: 0
comments: 0
---

# 2517. 礼盒的最大甜度

> **[yiduobo的每日leetcode 2517.礼盒的最大甜度](https://zhuanlan.zhihu.com/p/634853739) · 知乎 · 2023-06-07 · 赞同 0**
> 力扣：[2517. 礼盒的最大甜蜜度](https://leetcode.cn/problems/maximum-tastiness-of-candy-basket/) · Medium · 灵茶山艾府：[二分答案（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2517.礼盒的最大甜度

[力扣](https://leetcode.cn/problems/maximum-tastiness-of-candy-basket/)

礼盒的甜度越低，放糖果的门槛就越低，可放进去的糖果也就越多。根据这一点，就可以通过二分答案来寻找最大可行的甜度。

首先将糖果按照价格从小到大排序，然后开始二分。二分的下界自然为0，而上界则是最贵的糖果与最便宜的糖果的价格之差。对于当前二分到的甜度mid，则可以使用贪心法，一趟遍历，同时使用一个变量pre记录已选择的最后那颗糖果的下标。对于当前遍历到的下标index，若price[index]与price[pre]的价格之差大于等于mid，那么就可以选择price[index]，然后将pre更新为index。若最终可用的糖果数目大于等于k，说明mid是一种可行的甜度，此时就应该更新二分下界left为mid，否则更新二分上界right为mid - 1。

最后附上python代码：

```python
class Solution(object):
    def maximumTastiness(self, price, k):
        """
        :type price: List[int]
        :type k: int
        :rtype: int
        """

        price.sort()
        left = 0
        right = price[-1] - price[0]

        while left < right:
            mid = (left + right + 1) >> 1
            cnt = 1
            pre = 0
            now = 1
            while now < len(price):
                if price[now] - price[pre] >= mid:
                    pre = now
                    cnt += 1
                
                now += 1

            if cnt >= k:
                left = mid
            else:
                right = mid - 1

        return left
```
