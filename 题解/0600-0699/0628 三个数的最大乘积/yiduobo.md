---
title: "628. 三个数的最大乘积"
aliases: ["yiduobo的每日leetcode 628.三个数的最大乘积"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/270023414"
zhihu_id: "270023414"
zhihu_title: "yiduobo的每日leetcode 628.三个数的最大乘积"
question_id: "628"
question: "三个数的最大乘积"
problem_url: "https://leetcode.cn/problems/maximum-product-of-three-numbers/"
difficulty: "Easy"
created: "2020-10-29T23:28:37+08:00"
updated: "2020-10-29T23:28:37+08:00"
upvotes: 0
comments: 0
---

# 628. 三个数的最大乘积

> **[yiduobo的每日leetcode 628.三个数的最大乘积](https://zhuanlan.zhihu.com/p/270023414) · 知乎 · 2020-10-29 · 赞同 0**
> 力扣：[628. 三个数的最大乘积](https://leetcode.cn/problems/maximum-product-of-three-numbers/) · Easy · 灵茶山艾府：[证明：只需考虑两种情况（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

628.三个数的最大乘积<https://leetcode-cn.com/problems/maximum-product-of-three-numbers/>

注意到这里的数中可能出现负数，那么需要分情况进行讨论。如果直接讨论候选集中正负数的个数会比较复杂，我们可以转换思路，讨论最终答案中的正负数个数：

1、最终答案为3个正数：

此时显然应该选择最大的3个正数

2、最终答案中有一个0：

说明此时要么非0的数不足3个，要么无论怎么选择非0的数答案都是负数，于是有：

1）非0整数小于3个：此时任选3个数，其中必然有一个0，可以简单认为选择最大的3个数

2）非0整数大于等于3个，且其中没有正数：此时0是里面最大的数，于是也可以简单认为选择最大的3个数

3）非0整数恰好3个，且恰好是两个正数一个负数：此时可以选择两个正数和0，也可以认为是选择最大的3个数

3、最终答案中有2个正数，1个负数：

此时乘积为负，说明此时只有这3个数。因为若存在第3个正数，那么选择3个正数乘积为正；若存在第2个负数，那么应该选择任意正数和2个负数乘积也为正；若存在0，那么选择0加上任意两数答案为0。这几种情况下都不会使得乘积为负，说明此时就只有这3个数。于是此时的选择也可以看成选择了最大的3个数

4、最终答案中有1个正数，2个负数：

此时我们需要这2个负数的绝对值最大，因此我们应该选择最小的2个负数，以及最大的正数。此时的选择是最大的数和两个最小的数

5、最终答案为3个负数：

此时乘积为负数，说明候选集中既没有正数，也没有0，否则选择任意正数或0，乘上任意2个负数，最终答案都不会是负数。

由于最终答案为负，因此我们需要这3个负数的绝对值尽量小，那么就是从候选集中选出3个最大的负数，于是此时的选择也可以看成选择了最大的3个数

综合上面几种情况，可以发现最终答案必然是从选择3个最大的数，或者选择1个最大的数和两个最小的数之间产生，于是可以一趟扫描，选出这5个数，然后判断哪种选择方式的乘积较大即可。

最后附上python代码：

```python
class Solution(object):
    def maximumProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        max1 = max2 = max3 = min1 = min2 = None
        for num in nums:
            if max1 is None or max1 < num:
                max1, max2, max3 = num, max1, max2
            elif max2 is None or max2 < num:
                max2, max3 = num, max2
            elif max3 is None or max3 < num:
                max3 = num

            if min1 is None or min1 > num:
                min1, min2 = num, min1
            elif min2 is None or min2 > num:
                min2 = num

        return max(max1 * max2 * max3, max1 * min1 * min2)
```
