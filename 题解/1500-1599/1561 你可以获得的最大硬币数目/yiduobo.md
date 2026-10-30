---
title: "1561. 你可以获得的最大硬币数目"
aliases: ["yiduobo的每日leetcode 1561.你可以获得的最大硬币数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/426984339"
zhihu_id: "426984339"
zhihu_title: "yiduobo的每日leetcode 1561.你可以获得的最大硬币数目"
question_id: "1561"
question: "你可以获得的最大硬币数目"
problem_url: "https://leetcode.cn/problems/maximum-number-of-coins-you-can-get/"
difficulty: "Medium"
rating: 1406
created: "2021-10-30T22:18:03+08:00"
updated: "2021-10-30T22:18:03+08:00"
upvotes: 1
comments: 0
---

# 1561. 你可以获得的最大硬币数目

> **[yiduobo的每日leetcode 1561.你可以获得的最大硬币数目](https://zhuanlan.zhihu.com/p/426984339) · 知乎 · 2021-10-30 · 赞同 1**
> 力扣：[1561. 你可以获得的最大硬币数目](https://leetcode.cn/problems/maximum-number-of-coins-you-can-get/) · Medium · 灵茶山艾府：[贪心，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1561.你可以获得的最大硬币数目

[力扣](https://leetcode-cn.com/problems/maximum-number-of-coins-you-can-get/)

首先可以排除掉干扰项bob。由于bob每次拿的都是最少的，因此每次都可以安排当前剩下硬币中最少的给bob，那么问题就变成了两个人分n \* 2/3个硬币。由于alice每次都是拿最多的，因此每一轮我们就应该拿次多的。很直观的理解是如果我们不拿次多的，那么次多的必然在之后的某一次被alice拿走，我们拿到的硬币肯定是更少的。

于是可以对硬币进行排序，按行从大到小，跳着选择n个数作为最终答案。

注意到这里堆中硬币数的规模是小于堆数规模的，因此我采用的是桶排序。

最后附上python代码：

```python
class Solution(object):
    def maxCoins(self, piles):
        """
        :type piles: List[int]
        :rtype: int
        """

        cnt_list = [0] * 10001
        for pile in piles:
            cnt_list[pile] += 1

        n = len(piles) / 3
        delta = 0
        res = 0
        for now in range(10000, 0, -1):
            cnt_list[now] += delta
            tmp = cnt_list[now] / 2
            if n <= tmp:
                return res + now * n
            else:
                n -= tmp
                res += now * tmp
                delta = cnt_list[now] % 2
```
