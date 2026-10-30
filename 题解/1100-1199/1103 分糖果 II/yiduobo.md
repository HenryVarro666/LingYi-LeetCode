---
title: "1103. 分糖果II"
aliases: ["yiduobo的每日leetcode 1103.分糖果II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/374280772"
zhihu_id: "374280772"
zhihu_title: "yiduobo的每日leetcode 1103.分糖果II"
question_id: "1103"
question: "分糖果 II"
problem_url: "https://leetcode.cn/problems/distribute-candies-to-people/"
difficulty: "Easy"
created: "2021-05-22T00:10:36+08:00"
updated: "2021-05-22T00:10:36+08:00"
upvotes: 0
comments: 0
---

# 1103. 分糖果II

> **[yiduobo的每日leetcode 1103.分糖果II](https://zhuanlan.zhihu.com/p/374280772) · 知乎 · 2021-05-22 · 赞同 0**
> 力扣：[1103. 分糖果 II](https://leetcode.cn/problems/distribute-candies-to-people/) · Easy · 灵茶山艾府：[两种方法：模拟/数学公式（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1103.分糖果II

[力扣](https://leetcode-cn.com/problems/distribute-candies-to-people/)

由于这里糖果的数量是逐一递增的，那么设最终完整地分了p次，那么一共就分出去了

s \= (1 + p) \* p / 2

颗糖果，这里的s小于等于candies，同时p要最大。

通过配方法可以很快得到

p \= int(sqrt(candies \* 2 + 0.25) - 0.5)

由于一共完整地分了p次，那么每个小朋友都分到了rnd \= p / num_people轮糖果。另外，其中的前rest \= p % num_people个小朋友还将额外分到一轮糖果。

对于第i个小朋友，第1轮分到了i颗糖果，第2轮分到了i + num_people颗糖果，那么第k轮就会分到i + (k - 1) \* num_people颗糖果，那么一共rnd轮分到糖果数就是

i + (i + num_people) + (i + 2 \* num_people) + ... + (i + (rnd - 1) \* num_people) \=

i \* rnd + ((1 + rnd - 1) \* rnd / 2) \* num_people

对于前rest个小朋友而言，第i个小朋友在上面的的基础上还将再分到i + rnd \* num_people颗糖果。

至此一共分完了p次糖果，还剩下candies - p \* (1 + p) / 2颗糖果，而这些糖果最后都将分给第rest + 1个小朋友。

最后附上python代码：

```python
class Solution(object):
    def distributeCandies(self, candies, num_people):
        """
        :type candies: int
        :type num_people: int
        :rtype: List[int]
        """

        p = int(sqrt(candies * 2 + 0.25) - 0.5)
        rnd = p / num_people
        rest = p % num_people
        res = [(index + 1) * rnd + num_people * (rnd - 1) * rnd / 2 for index in range(num_people)]
        for index in range(rest):
            res[index] += index + 1 + num_people * rnd
        res[rest] += candies - p * (1 + p) / 2
        return res
```
