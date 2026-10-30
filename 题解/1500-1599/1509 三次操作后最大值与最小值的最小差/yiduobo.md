---
title: "1509. 三次操作后最大值与最小值的最小差"
aliases: ["yiduobo的每日leetcode 1509.三次操作后最大值与最小值的最小差"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/419901497"
zhihu_id: "419901497"
zhihu_title: "yiduobo的每日leetcode 1509.三次操作后最大值与最小值的最小差"
question_id: "1509"
question: "三次操作后最大值与最小值的最小差"
problem_url: "https://leetcode.cn/problems/minimum-difference-between-largest-and-smallest-value-in-three-moves/"
created: "2021-10-10T20:01:39+08:00"
updated: "2021-10-10T20:01:40+08:00"
upvotes: 0
comments: 0
---

# 1509. 三次操作后最大值与最小值的最小差

> **[yiduobo的每日leetcode 1509.三次操作后最大值与最小值的最小差](https://zhuanlan.zhihu.com/p/419901497) · 知乎 · 2021-10-10 · 赞同 0**
> 力扣：[1509. 三次操作后最大值与最小值的最小差](https://leetcode.cn/problems/minimum-difference-between-largest-and-smallest-value-in-three-moves/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1509.三次操作后最大值与最小值的最小差

[力扣](https://leetcode-cn.com/problems/minimum-difference-between-largest-and-smallest-value-in-three-moves/)

首先考虑边界情况。当数组长度小于等于4时，显然可以将所有数都调整成同样大小，那么此时的答案必然为0。

接下来考虑数组长度n > 4的情况。为了使得最大值和最小值的差尽量小，那么就应该将最小值调大，或者将最大值调小。在将最小值或者最大值操作之后，此时新的最小值或者最大值就是原始数组中的次小值或者次大值，依次类推。

那么最终可以归纳成一下几种情况：

1、将第1、2、3小的值调大之后，此时数组中的最大值不变，最小值变为了原始数组中第4小的值

2、将第1、2小的值调大，最大值调小之后，此时数组中的最大值变为原始数组中的次大值，最小值变为了原始数组中第3小的值

3、将最小值调大，第1、2大的值调小之后，此时数组中的最大值变为了原始数组中第3大的值，最小值变为了原始数组中的次小值

4、将第1、2、3大的值调小之后，此时数组中的最小值不变，最大值变为了原始数组中第4打的值

也就是说，可以先找出数组中最大的四个数ma1，ma2，ma3，ma4以及数组中最小的四个数mi1，mi2，mi3，mi4，那么每种情况最终的结果就是

1、ma1 - mi4

2、ma2 - mi3

3、ma3 - mi2

4、ma4 - mi1

取其中最小值作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def minDifference(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        if len(nums) <= 4:
            return 0

        ma1 = ma2 = ma3 = ma4 = None
        mi1 = mi2 = mi3 = mi4 = None
        
        for num in nums:
            if ma1 is None or num > ma1:
                ma1, ma2, ma3, ma4 = num, ma1, ma2, ma3
            elif ma2 is None or num > ma2:
                ma2, ma3, ma4 = num, ma2, ma3
            elif ma3 is None or num > ma3:
                ma3, ma4 = num, ma3
            elif ma4 is None or num > ma4:
                ma4 = num
            
            if mi1 is None or num < mi1:
                mi1, mi2, mi3, mi4 = num, mi1, mi2, mi3
            elif mi2 is None or num < mi2:
                mi2, mi3, mi4 = num, mi2, mi3
            elif mi3 is None or num < mi3:
                mi3, mi4 = num, mi3
            elif mi4 is None or num < mi4:
                mi4 = num
        
        return min(ma1 - mi4, ma2 - mi3, ma3 - mi2, ma4 - mi1)
```
