---
title: "LCP 18. 早餐组合"
aliases: ["yiduobo的每日leetcode LCP18.早餐组合"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/571991497"
zhihu_id: "571991497"
zhihu_title: "yiduobo的每日leetcode LCP18.早餐组合"
question_id: "LCP 18"
question: "早餐组合"
problem_url: "https://leetcode.cn/problems/2v/"
created: "2022-10-10T01:18:45+08:00"
updated: "2022-10-10T01:18:45+08:00"
upvotes: 0
comments: 0
---

# LCP 18. 早餐组合

> **[yiduobo的每日leetcode LCP18.早餐组合](https://zhuanlan.zhihu.com/p/571991497) · 知乎 · 2022-10-10 · 赞同 0**
> 力扣：[LCP 18. 早餐组合](https://leetcode.cn/problems/2v/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP18.早餐组合

[力扣](https://leetcode.cn/problems/2vYnGI/)

题目的数据规模很大，直接两两枚举肯定是不行的。注意到主食和饮料的价格都是正数，那么选择越贵的主食，就只能选择越便宜的饮料。于是可以将主食和饮料分别按从小到大和从大到小进行排序，接下来，使用一个变量p表示对于当前主食可以选择的最贵的饮料的下标，然后遍历所有的主食。

随着主食的遍历，p只会越来越大，因此可以在均摊O(1)的时间内找出每款主食对应的p。对于某一款主食而言，其可以搭配的饮料为下标大于等于p中的任意一款，因此一共有len(drinks) - p款饮料可供搭配。对于每一款主食都通过p计算可行的搭配数，并将这些数累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def breakfastNumber(self, staple, drinks, x):
        """
        :type staple: List[int]
        :type drinks: List[int]
        :type x: int
        :rtype: int
        """

        staple.sort()
        drinks.sort(reverse=True)

        res = 0
        p = 0
        mod = 10 ** 9 + 7
        for s in staple:
            if s > x:
                break
            while p < len(drinks) and drinks[p] + s > x:
                p += 1

            if p == len(drinks):
                break
            
            res += len(drinks) - p
            if res >= mod:
                res -= mod
        
        return res
```
