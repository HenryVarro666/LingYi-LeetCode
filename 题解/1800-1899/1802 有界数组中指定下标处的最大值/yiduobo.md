---
title: "1802. 有界数组中指定下标处的最大值"
aliases: ["yiduobo的每日leetcode 1802.有界数组中指定下标处的最大值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/464018604"
zhihu_id: "464018604"
zhihu_title: "yiduobo的每日leetcode 1802.有界数组中指定下标处的最大值"
question_id: "1802"
question: "有界数组中指定下标处的最大值"
problem_url: "https://leetcode.cn/problems/maximum-value-at-a-given-index-in-a-bounded-array/"
created: "2022-02-04T23:51:27+08:00"
updated: "2022-02-04T23:51:27+08:00"
upvotes: 0
comments: 0
---

# 1802. 有界数组中指定下标处的最大值

> **[yiduobo的每日leetcode 1802.有界数组中指定下标处的最大值](https://zhuanlan.zhihu.com/p/464018604) · 知乎 · 2022-02-04 · 赞同 0**
> 力扣：[1802. 有界数组中指定下标处的最大值](https://leetcode.cn/problems/maximum-value-at-a-given-index-in-a-bounded-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1802.有界数组中指定下标处的最大值

[力扣](https://leetcode-cn.com/problems/maximum-value-at-a-given-index-in-a-bounded-array/)

为了使得nums[index]最大，且相邻数的插值最多为1，那么理想情况就是

[1, 1, 1, ..., 1, 2, 3, ..., k - 1, k, k - 1, ..., 3, 2, 1, ..., 1, 1, 1]

这种形式，其中k就是对应的nums[index]。

当然，这是最节省的情况，如果有没有用完的份额则可以将两侧与2临近的1变为2，以此类推。

如果是上面这种形式，那么中间一段1到k以及k - 1到1，一共是2k - 1个数，和恰好为k^2，因此整个数组的和就是k^2 + n - (2k - 1) \= k^2 - 2k + 1 + n \= (k - 1)^2 + n \<\= maxSum，在这里就可以直接解出这个k了。

需要注意的是，这里并不一定会写成完整的1到k这种形式，因为index可能靠近两侧，位置不够了。例如样例2，就是[2, 3, 2, 1, 1, 1]这种形式，左侧的位置是不够的，这也使得计算k的值有了一些变化。

index距离左边界有0到index - 1一共index个数，距离右边界则是剩下的n - index - 1个数。由于两侧是等价的，那么不妨设这两个数中较大的为b2，较小的为b1，那么需要考察三种情况：

1、k \<\= b1：此时两侧的格子是完全足够的，因此可以直接套用上面的公式进行求解

2、b1 \< k \<\= b2：此时b1这一侧的格子是不够的，而b2这一侧的格子是足够的，那么b2这一侧的数值排列依然是1到k，其和就是(1 + k) \* k / 2。而对于b1这一侧，则是从k - 1开始向下排布的b1个数，也就是k - 1，k - 2，...，k - b1这些数，和为(2k -1 - b1) \* b1 / 2。除了这两部分，还有b2这一侧多出来的一些1，这些1的数目一共是n - k - b1个，因此此时数组的总和就是

(1 + k) \* k / 2 + (2k - 1 - b1) \* b1 / 2 + n - k - b1

化简后就是

(k^2 + (2b1 - 1)k + 2n - b1^2 - 3b1) / 2

依然是对k配方，就有

((k + (b1 - 1/2))^2) / 2 + n - b1^2 - b1 - 1 / 8 \<\= maxSum

3、b2 \< k：此时两侧的格子都是不够的。b1这一侧与上面一样，和为(2k - 1 - b1) \* b1 / 2。b2也类似，就是(2k - 1 - b2) \* b2 / 2。除此之外，还需要记得中间的k，因此此时数组的总和就是

(2k - 1 - b1) \* b1 / 2 + (2k - 1 - b2) \* b2 / 2 + k

化简后就是

（b1 + b2 + 1)k - (b1^2 + b1 + b2^2 + b2) / 2 \<\= maxSum

值得一提的是，这三种情况中k是越来越大的。为了使得答案最大，因此可以按照情况3 -> 情况2 -> 情况1的顺序来求解k。若找到了合法的k，那么这个k就是最终答案，而不需要继续向下求解了。

最后附上python代码：

```python
class Solution(object):
    def maxValue(self, n, index, maxSum):
        """
        :type n: int
        :type index: int
        :type maxSum: int
        :rtype: int
        """

        b1 = index
        b2 = n - index - 1
        if b1 > b2:
            b1, b2 = b2, b1
        
        res = int((maxSum * 2 + b1 * b1 + b2 * b2 + b1 + b2) / (2.0 * (b1 + b2 + 1)))
        if res >= b2 + 1:
            return res
        
        res = int(sqrt(2 * (maxSum - n + b1 * b1 + b1) + 0.25) + 0.5 - b1)
        if res >= b1 + 1:
            return res
        
        res = int(sqrt(maxSum - n))
        if (res + 1) * (res + 1) == maxSum - n:
            res += 1
        res += 1
        return res
```
