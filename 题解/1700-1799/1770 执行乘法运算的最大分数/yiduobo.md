---
title: "1770. 执行乘法运算的最大分数"
aliases: ["yiduobo的每日leetcode 1770.执行乘法运算的最大分数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/460972599"
zhihu_id: "460972599"
zhihu_title: "yiduobo的每日leetcode 1770.执行乘法运算的最大分数"
question_id: "1770"
question: "执行乘法运算的最大分数"
problem_url: "https://leetcode.cn/problems/maximum-score-from-performing-multiplication-operations/"
created: "2022-01-23T16:10:11+08:00"
updated: "2022-01-23T16:10:11+08:00"
upvotes: 0
comments: 0
---

# 1770. 执行乘法运算的最大分数

> **[yiduobo的每日leetcode 1770.执行乘法运算的最大分数](https://zhuanlan.zhihu.com/p/460972599) · 知乎 · 2022-01-23 · 赞同 0**
> 力扣：[1770. 执行乘法运算的最大分数](https://leetcode.cn/problems/maximum-score-from-performing-multiplication-operations/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1770.执行乘法运算的最大分数

[力扣](https://leetcode-cn.com/problems/maximum-score-from-performing-multiplication-operations/)

对于这类从两侧向中间处理的区间类问题，经典的做法就是f[l][r]表示l到r如何如何的动态规划。不过本题有一点需要注意的是，这里的区间长度n非常大，直接使用f[l][r]表示的话空间复杂度承受不住，必须另想办法。

注意到操作次数m的规模是比较小的，又因为每次操作只能是头或者尾，因此可以转而用m相关的状态表示来替代f[l][r]。状态表示中的一维肯定是操作的次数，此时就还需要一维来表示当前操作次数下用掉了多少个nums头部的数字，这样一来，就可以通过操作的次数以及头部用掉的数字计算出尾部用掉的数字，从而在头尾中选择下一个数字来进行状态转移。

具体来说，令f[i][j]表示前i + 1步，用掉了数组头部j个数字时的最大分数，那么对于f[i][j]：

1、首先边界情况。当i \= 0时，一共执行了1次操作，所以一共使用了1个数。

1-1）若此时的j \= 0，那么说明没有使用数组头部的数，而是使用了一个数组尾部的数，因此就有f[0][0] \= nums[-1] \* mul[0]。

1-2）若此时的j \= 1，那么说明只使用了数组头部的数，因此就有f[0][1] \= nums[0] \* mul[0]。

2、接下来对于i > 0的情况，一共执行了i + 1次操作，所以一共使用了i + 1个数。

2-1）若此时的j \= 0，那么说明依然没有用到数组头部的数，而这一步用到的是数组从后往前数的第i + 1个数，即nums[n - i - 1]，于是就有f[i][0] \= f[i - 1][0] + nums[n - i - 1] \* mul[i]。

2-2）若此时的j \= i + 1，那么说明用到的全部都是数组头部的数，而这一步用到的是数组从前往后数的第i + 1个数，即nums[i]，于是就有f[i][i + 1] \= f[i - 1][i] + nums[i] \* mul[i]。

2-3）若此时的j满足0 \< j \< i + 1，那么这一步使用的数就有两种选择方法，即选择头部的数或者选择尾部的数。

如果选择头部的数，那么当前状态f[i][j]的上一个状态就是f[i - 1][j - 1]，而这一步选择的数是从前往后数的第j个数，即nums[j - 1]，于是就有f[i][j] \= f[i - 1][j - 1] + nums[j - 1] \* mul[i]。

如果选择尾部的数，那么当前状态f[i][j]的上一个状态就是f[i - 1][j]。到这一步位置一共使用了i + 1个数，其中j个数是从头部选择的，因此需要从尾部选择i + 1 - j个数，因此这一步选择的数是从后往前数的第i - j + 1个数，即nums[n - (i - j + 1)] \= nums[n - (i - j) - 1]，于是就有f[i][j] \= f[i - 1][j] + nums[n - (i - j) - 1] \* mul[i]。

综合起来，就有

f[i][j] \= max(f[i - 1][j - 1] + nums[j - 1] \* mul[i], f[i - 1][j] + nums[n - (i - j) - 1] \* mul[i])

动态规划完成后，最终答案就是max(f[-1])。

最后附上python代码：

```python
class Solution(object):
    def maximumScore(self, nums, multipliers):
        """
        :type nums: List[int]
        :type multipliers: List[int]
        :rtype: int
        """

        n = len(nums)
        m = len(multipliers)

        f = [[0] * (m + 1) for _ in range(m)]
        f[0][0] = nums[n - 1] * multipliers[0]
        f[0][1] = nums[0] * multipliers[0]
        for i in range(1, m):
            f[i][0] = f[i - 1][0] + nums[n - i - 1] * multipliers[i]
            for j in range(1, i + 1):
                f[i][j] = max(f[i - 1][j] + nums[n - (i - j) - 1] * multipliers[i], f[i - 1][j - 1] + nums[j - 1] * multipliers[i])
            f[i][i + 1] = f[i - 1][i] + nums[i] * multipliers[i]
        
        return max(f[-1])
```
