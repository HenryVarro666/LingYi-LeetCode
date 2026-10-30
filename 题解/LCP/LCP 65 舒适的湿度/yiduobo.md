---
title: "LCP 65. 舒适的湿度"
aliases: ["yiduobo的每日leetcode LCP65.舒适的湿度"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "leetcode/dp", "leetcode/dp-2", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/579888197"
zhihu_id: "579888197"
zhihu_title: "yiduobo的每日leetcode LCP65.舒适的湿度"
question_id: "LCP 65"
question: "舒适的湿度"
problem_url: "https://leetcode.cn/problems/3aqs1c/"
difficulty: "Hard"
created: "2022-11-03T01:03:34+08:00"
updated: "2022-11-03T01:03:34+08:00"
upvotes: 0
comments: 0
---

# LCP 65. 舒适的湿度

> **[yiduobo的每日leetcode LCP65.舒适的湿度](https://zhuanlan.zhihu.com/p/579888197) · 知乎 · 2022-11-03 · 赞同 0**
> 力扣：[LCP 65. 舒适的湿度](https://leetcode.cn/problems/3aqs1c/) · Hard · 灵茶山艾府：[数形结合 + 巧妙地定义状态（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP65.舒适的湿度

[力扣](https://leetcode.cn/problems/3aqs1c/description/)

题目给出一个数组，其中的数都是正数。接下来要求将其中某些数的符号变为负号，问数组中各个子数组之和绝对值中最大值的最小值是多少。

一个直观的想法是这个最小值越大，数组就越好构造，那么在这里可以二分答案，然后将问题转化成判断当前能否构造出一个数组使得各子数组之和绝对值中的最大值小于这个二分的mid。

接下来需要决定二分的边界。二分的下界显然是1，而对于二分的上界，则可以认为是max(operate) \* 2，因为在进行构造时，有一种构造方法是若当前构造数组的前缀和为正，那么就将下一个数作为负数，反之就将下一个数作为正数，这样一来就可以保证前缀和的绝对值不会超过max(operate)，从而保证最终答案不会超过max(operate) \* 2。

确定了二分的边界后，接下来的问题就是如何判断对于当前的二分值mid可以构造出合法的答案。

对于子数组和绝对值的最大值问题，常见的求解方法有两种两种。

第一种是一趟遍历，按照最大子段和以及类似的最小子段和的方式求解，那么最大的绝对值就是最大子段和以及负的最小子段和中较大的那一个。

另一种则是一趟遍历，计算前缀和，最后答案就是最大的前缀和减去最小的前缀和。

对于本题，使用第二种方法是比较合适的，因为在这里已经给出了前缀和的上下界mid，而问题则转化成了能否构造一个数组，使得其最大的前缀和减去最小的前缀和小于等于mid。

虽然在这里给出了取值的范围，但是具体值没有定下来，处理起来依然不太方便。不过在这里由于已经定死了前缀和的下界-mid，那么在这里完全可以从0到-mid枚举这个下界。设当前枚举到的下界为x，那么如果在数组最前面加入一项-x，需要求解的问题就变成了能否构造出一个数组，使得数组所有前缀和都在0到mid之间。

这个问题就好办多了，可以使用动态规划，令f[i][j]表示前i个数能否构成这些数之和为j的数组，那么对于f[i][j]，可以枚举f[i - 1]中所有满足f[i - 1][k]为true的k，接下来：

1、若k + op\[i\] \<\= mid，那么就有f\[i\]\[k + op\[i\]\] \= true

2、若k - op\[i\] >\= 0，那么就有f\[i\]\[k - op\[i\]\] \= true

全部处理完成后，只需判断f[n - 1]中是否存在满足f[n - 1][j]为true的j就行了。

当然，在这里一个一个枚举x来计算的复杂度依然很高，在这里完全可以一次性先将f[0][0]到f[0][mid]都赋为true，表示在数组最开始加入0到mid这些情况，然后再进行动态规划。

这样一来，就可以在O(n \* max(op))的时间内完成一次判定了，因此最终的时间复杂度为O(n \* max(op) \* log(max(op)))

最后附上python代码：

```python
class Solution(object):
    def unSuitability(self, operate):
        """
        :type operate: List[int]
        :rtype: int
        """

        n = len(operate)

        ma = max(operate)

        def check(v):
            g = [True] * (v + 1)
            for op in operate:
                f = [False] * (v + 1)
                for num in range(mid + 1):
                    if g[num]:
                        if num + op <= mid:
                            f[num + op] = True
                        if num >= op:
                            f[num - op] = True
                
                g = f[:]
            
            for num in range(mid + 1):
                if f[num]:
                    return True
            
            return False

        left = 1
        right = ma + ma
        while left < right:
            mid = (left + right) >> 1
            if check(mid):
                right = mid
            else:
                left = mid + 1
        
        return left
```
