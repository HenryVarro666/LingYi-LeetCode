---
title: "2137. 通过倒水操作让所有的水桶所含水量相等"
aliases: ["yiduobo的每日leetcode 2137.通过倒水操作让所有的水桶所含水量相等"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/626504094"
zhihu_id: "626504094"
zhihu_title: "yiduobo的每日leetcode 2137.通过倒水操作让所有的水桶所含水量相等"
question_id: "2137"
question: "通过倒水操作让所有的水桶所含水量相等"
problem_url: "https://leetcode.cn/problems/pour-water-between-buckets-to-make-water-levels-equal/"
created: "2023-05-03T21:17:50+08:00"
updated: "2023-05-03T21:17:50+08:00"
upvotes: 0
comments: 0
---

# 2137. 通过倒水操作让所有的水桶所含水量相等

> **[yiduobo的每日leetcode 2137.通过倒水操作让所有的水桶所含水量相等](https://zhuanlan.zhihu.com/p/626504094) · 知乎 · 2023-05-03 · 赞同 0**
> 力扣：[2137. 通过倒水操作让所有的水桶所含水量相等](https://leetcode.cn/problems/pour-water-between-buckets-to-make-water-levels-equal/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2137.通过倒水操作让所有的水桶所含水量相等

[力扣](https://leetcode.cn/problems/pour-water-between-buckets-to-make-water-levels-equal/)

二分法的题目，每次二分最终各水桶的水量。对于当前二分到的水量mid，只需一趟遍历，使用一个变量cnt记录多出的水量。若当前桶中的水量大于mid，那么就将多出的水量累加到cnt当中，否则就需要从cnt中抽取部分水量到当前桶中。需要注意使用cnt补充桶内水量时需要计算loss。若最终的cnt大于等于0，那么就调整下边界，否则就调整上边界。

重复此过程直到上下边界之差在10^(-5)之内，此时的二分边界即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def equalizeWater(self, buckets, loss):
        """
        :type buckets: List[int]
        :type loss: int
        :rtype: float
        """

        left = 0.0
        right = max(buckets) * 1.0
        eps = 10 ** -5

        while left < right - eps:
            mid = (left + right) / 2.0
            cnt = 0.0
            for v in buckets:
                if v > mid:
                    cnt += v - mid
                else:
                    cnt -= (mid - v) * 100 / (100 - loss)

            if cnt >= 0:
                left = mid
            else:
                right = mid
        
        return left
```
