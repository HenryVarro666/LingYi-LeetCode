---
title: "LCP 33. 蓄水"
aliases: ["yiduobo的每日leetcode LCP33.蓄水"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/574592314"
zhihu_id: "574592314"
zhihu_title: "yiduobo的每日leetcode LCP33.蓄水"
question_id: "LCP 33"
question: "蓄水"
problem_url: "https://leetcode.cn/problems/o8/"
created: "2022-10-18T02:00:42+08:00"
updated: "2022-10-18T02:00:42+08:00"
upvotes: 0
comments: 0
---

# LCP 33. 蓄水

> **[yiduobo的每日leetcode LCP33.蓄水](https://zhuanlan.zhihu.com/p/574592314) · 知乎 · 2022-10-18 · 赞同 0**
> 力扣：[LCP 33. 蓄水](https://leetcode.cn/problems/o8/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP33.蓄水

[力扣](https://leetcode.cn/problems/o8SXZn/)

本题应该有数学方法可以解，但是似乎比较复杂。注意到题目中水桶的数目和最大的蓄水要求规模都不大，那么可以暴力枚举求解。

首先考虑边界情况。当所有水桶的蓄水要求都是0时，则不需要进行任何操作，直接返回0。

接下来是一般情况。若当前的蓄水轮次为t，那么就可以枚举所有的水桶，通过对应的蓄水要求和t计算出当前水桶的最小容积，然后根据这个最小容积计算当前水桶需要扩容的次数。所有水桶扩容次数之和在加上蓄水次数就是当前蓄水轮次t所需的操作总次数。

于是可以枚举所有的t，计算对应的操作总次数，其中的最小值就是最终答案了。

最后附上python代码：

```python
class Solution(object):
    def storeWater(self, bucket, vat):
        """
        :type bucket: List[int]
        :type vat: List[int]
        :rtype: int
        """

        if sum(vat) == 0:
            return 0
        
        res = None
        for t in range(1, max(vat) + 1):
            now = 0
            for index, v in enumerate(vat):                
                min_buck = (v - 1) / t + 1
                if min_buck > bucket[index]:
                    now += min_buck - bucket[index]
            if res is None or res > t + now:
                res = t + now
        
        return res
```
