---
title: "1558. 得到目标数组的最少函数调用次数"
aliases: ["yiduobo的每日leetcode 1558.得到目标数组的最少函数调用次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/426966174"
zhihu_id: "426966174"
zhihu_title: "yiduobo的每日leetcode 1558.得到目标数组的最少函数调用次数"
question_id: "1558"
question: "得到目标数组的最少函数调用次数"
problem_url: "https://leetcode.cn/problems/minimum-numbers-of-function-calls-to-make-target-array/"
created: "2021-10-28T23:36:49+08:00"
updated: "2021-10-28T23:36:49+08:00"
upvotes: 0
comments: 0
---

# 1558. 得到目标数组的最少函数调用次数

> **[yiduobo的每日leetcode 1558.得到目标数组的最少函数调用次数](https://zhuanlan.zhihu.com/p/426966174) · 知乎 · 2021-10-28 · 赞同 0**
> 力扣：[1558. 得到目标数组的最少函数调用次数](https://leetcode.cn/problems/minimum-numbers-of-function-calls-to-make-target-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1558.得到目标数组的最少函数调用次数

[力扣](https://leetcode-cn.com/problems/minimum-numbers-of-function-calls-to-make-target-array/)

首先分析这个函数的作用。这个函数支持两种操作，分别为将数组中某个位置的值加上1，以及将数组中所有的数都乘以2。

如果从二进制数的角度来看的话，由于乘以2这种操作本身是不会产出1的，因此对于一个数而言，若其二进制表示中有k个1，那么至少需要k次操作来添加这些1。

另外，对于乘以2这种操作，由于0乘以2依然为0，也就是说可以让二进制表示下数位较多的数先行启动，而数位较少的数则先保持0的状态，跟着执行乘以2的操作，等到适当的时候再执行加1，然后此时的乘2才会发挥作用。换言之，只需要找到所有数中二进制位最多的那个数，设其位数为k，那么总共就只需要执行k - 1次乘以2操作了。

综合起来，可以遍历每个数，统计这些数二进制表示下的位数以及1的个数，将1的个数累加到答案中，并更新最大位数k。遍历完成后，最终答案就是所有1的个数加上k - 1。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        max_l = 0
        for num in nums:
            l = 0
            while num:
                res += num % 2
                num /= 2
                l += 1
            
            max_l = max(max_l, l - 1)

        return res + max_l
```
