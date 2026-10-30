---
title: "2819. 购买巧克力后的最小相对损失"
aliases: ["yiduobo的每日leetcode 2819.购买巧克力后的最小相对损失"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/658816342"
zhihu_id: "658816342"
zhihu_title: "yiduobo的每日leetcode 2819.购买巧克力后的最小相对损失"
question_id: "2819"
question: "购买巧克力后的最小相对损失"
problem_url: "https://leetcode.cn/problems/minimum-relative-loss-after-buying-chocolates/"
created: "2023-09-28T04:56:50+08:00"
updated: "2023-09-28T04:56:50+08:00"
upvotes: 0
comments: 0
---

# 2819. 购买巧克力后的最小相对损失

> **[yiduobo的每日leetcode 2819.购买巧克力后的最小相对损失](https://zhuanlan.zhihu.com/p/658816342) · 知乎 · 2023-09-28 · 赞同 0**
> 力扣：[2819. 购买巧克力后的最小相对损失](https://leetcode.cn/problems/minimum-relative-loss-after-buying-chocolates/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2819.购买巧克力后的最小相对损失

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-relative-loss-after-buying-chocolates/)

alice和bob这两人就总喜欢整些这种损人利己的勾当，别人多出钱就是自己赢。。

言归正传。首先题目的数据规模非常大，那么先排序然后离线处理是很自然的想法。

接下来，对于某件商品的价格而言，其对bob来说的收益并不是线性的。简单的理解是，当商品价格不超过当前的k[i]时，价格越贵bob越亏，但是当商品价格超过当前的k[i]时，价格越贵bob越赚，因为超出k[i]的这部分是alice出的。

更具体的，对于一件价格为p的商品，若p \<\= k[i]，那么选择这件商品bob的相对亏损就是p，反之相对亏损应该是k[i] - (p - k[i]) \= 2 \* k[i] - p。

有了具体的数值，那么对于一组k[i]和m[i]，首先需要找出分割点bound，即按照价格排序后的商品中，price[0]到price[bound]的价格都小于等于k[i]，而price[bound + 1]以及之后的价格都大于k[i]，那么在这里可以得到，在前半部分，也就是便宜的这一部分中，应该优先选择便宜的商品，也就是下标较小的商品；反之，在后半部分，也就是贵的这一部分中，则应该优先选择贵的商品，也就是下标较大的商品。换言之，这就相当于一个二路归并问题，不过在这里如果直接使用二路归并来进行计算，复杂度肯定过高了，必须进行优化。

由于price在排序后就不会产生变化，那么选择购买的便宜商品一定是price的一个前缀，而贵的商品则一定是price的一个后缀，于是相对损失的求和实际上就可以直接通过前缀和来解决，那么现在的问题就是如何找到这个前缀的终点i以及后缀的起点j。

对于这个问题，实际上是在两个有序数组中找第m[i]小值的问题，这个问题可以参考第4题的处理方法，利用二分来求解

[yiduobo：yiduobo的每日leetcode 4. 寻找两个有序数组的中位数](https://zhuanlan.zhihu.com/p/112789053)

本题在实现上有一定的区别，首先本题找的是第m[i]小的值而不是中位数，另外本题是同一个数组，从头部和尾部想中间的分割点bound进行查找，不过思路上依然是利用当前两个部分剩余值中第m[i] / 2小的数进行比较，确定哪一侧的数将全部入选到这m[i]小的数中。除此之外，还有一个收获就是按照这个方法计算出第m小的值的位置后，顺便会将前缀终点i以及后缀起点j都计算好，接下来就只需使用前缀和计算当前k[i], m[i]对应的答案。

到了这里，就已经得到了针对单组数组的计算方法。最后还有一个问题就是对于当前的k[i], m[i]，如何高效确定bound的位置，此时之前的针对query的排序也可以利用起来了。由于query是从小到大排序好的，那么每一组询问对应的k都是单调不减的，因此其对应的bound必然也是单调不减的，于是只需在上一轮的基础上向后移动之前的bound就行了。

最后附上python代码：

```python
class Solution(object):
    def minimumRelativeLosses(self, prices, queries):
        """
        :type prices: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        prices.sort()
        s = [0]
        for p in prices:
            s.append(s[-1] + p)

        bound = 0
        res = [0] * len(queries)

        for index, q in sorted(enumerate(queries), key=lambda d:d[1][0]):
            while bound < len(prices) and prices[bound] <= q[0]:
                bound += 1

            if bound == 0:
                res[index] = q[0] * q[1] * 2 - (s[-1] - s[-q[1] - 1])
            elif bound == len(prices):
                res[index] = s[q[1]]
            else:
                i = 0
                j = len(prices) - 1
                k = q[1]
                while True:
                    if i == bound:
                        res[index] = s[bound] + q[0] * (q[1] - bound) * 2 - (s[-1] - s[-q[1] + bound - 1])
                        break
                    elif j == bound - 1:
                        res[index] = q[0] * (len(prices) - bound) * 2 - (s[-1] - s[bound]) + s[q[1] + bound - len(prices)]
                        break
                    elif k == 1:
                        if prices[i] < q[0] * 2 - prices[j]:
                            i += 1
                        else:
                            j -= 1
                        
                        res[index] = s[i] + q[0] * (q[1] - i) * 2 - (s[-1] - s[j + 1])
                        break

                    else:
                        mid = k / 2
                        if i + mid - 1 >= bound:
                            j -= mid
                        elif j - mid + 1 < bound:
                            i += mid
                        elif prices[i + mid - 1] < q[0] * 2 - prices[j - mid + 1]:
                            i += mid
                        else:
                            j -= mid
                        
                        k -= mid

        return res
```
