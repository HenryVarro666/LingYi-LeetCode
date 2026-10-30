---
title: "1742. 盒子中小球的最大数量"
aliases: ["yiduobo的每日leetcode 1742.盒子中小球的最大数量"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/enumeration", "leetcode/prefix-sum", "leetcode/bao-li", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/453800266"
zhihu_id: "453800266"
zhihu_title: "yiduobo的每日leetcode 1742.盒子中小球的最大数量"
question_id: "1742"
question: "盒子中小球的最大数量"
problem_url: "https://leetcode.cn/problems/maximum-number-of-balls-in-a-box/"
difficulty: "Easy"
created: "2022-01-06T00:21:18+08:00"
updated: "2022-01-06T00:21:19+08:00"
upvotes: 0
comments: 0
---

# 1742. 盒子中小球的最大数量

> **[yiduobo的每日leetcode 1742.盒子中小球的最大数量](https://zhuanlan.zhihu.com/p/453800266) · 知乎 · 2022-01-06 · 赞同 0**
> 力扣：[1742. 盒子中小球的最大数量](https://leetcode.cn/problems/maximum-number-of-balls-in-a-box/) · Easy · 灵茶山艾府：[三种方法：暴力枚举/前缀和/数位DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1742.盒子中小球的最大数量

[力扣](https://leetcode-cn.com/problems/maximum-number-of-balls-in-a-box/)

由于这里的数据规模不大，因此可以直接从low枚举到high，然后分别计算每个数各个数位上的和，然后使用哈希表来进行统计。一个简单的优化是利用x的数位和来确定x + 1的数位和。在没有出现进位的情况下，x + 1的数位和显然就等于x的数位和加1，而出现了进位时，则会有若干个9变成1的情况。此时需要统计x + 1末尾0的数量zero_cnt，这个zero_cnt对应的就是x中9变成0的数目，因此在这里需要在x的数位和加1的基础上额外减去zero_cnt \* 9。

当然，这里也存在更好的做法。之前应该遇到过一题类似的，但是记不清楚题号了。对于这类数位和有关的问题，一个通用做法是令f[i][j][flag][bound]表示长度为i，和为j，与上下界的关系为flag，且当前的上界数值或下界数值为bound时的合法数字个数。实现起来还是相对比较复杂的，但是时间复杂度可以从O(n)降到O(10 \* log(n))级别。我在这里偷懒就还是用的最上面的朴素做法。

最后附上python代码：

```python
class Solution(object):
    def countBalls(self, lowLimit, highLimit):
        """
        :type lowLimit: int
        :type highLimit: int
        :rtype: int
        """

        tmp = lowLimit
        now = 0
        while tmp:
            now += tmp % 10
            tmp /= 10
        
        cnt_dict = {now : 1}
        for num in range(lowLimit + 1, highLimit + 1):
            tmp = num
            zero = 0
            while tmp % 10 == 0:
                tmp /= 10
                zero += 1
            
            now = now - zero * 9 + 1
            cnt_dict[now] = cnt_dict.get(now, 0) + 1
        
        return max(cnt_dict.values())
```
