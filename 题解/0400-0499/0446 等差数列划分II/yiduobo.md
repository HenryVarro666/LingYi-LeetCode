---
title: "446. 等差数列划分II"
aliases: ["yiduobo的每日leetcode 446.等差数列划分II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/206755603"
zhihu_id: "206755603"
zhihu_title: "yiduobo的每日leetcode 446.等差数列划分II"
question_id: "446"
question: "等差数列划分II"
problem_url: "https://leetcode.cn/problems/arithmetic-slices-ii-subsequence/"
created: "2020-08-30T19:52:45+08:00"
updated: "2020-08-30T19:52:45+08:00"
upvotes: 0
comments: 0
---

# 446. 等差数列划分II

> **[yiduobo的每日leetcode 446.等差数列划分II](https://zhuanlan.zhihu.com/p/206755603) · 知乎 · 2020-08-30 · 赞同 0**
> 力扣：[446. 等差数列划分II](https://leetcode.cn/problems/arithmetic-slices-ii-subsequence/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

446.等差数列划分II <https://leetcode-cn.com/problems/arithmetic-slices-ii-subsequence/>

上一个等差数列划分的加强版。由于这里要求的是子序列而不是子串，因此之前的做法不再合适。我在这里使用的是动态规划的做法，设f[i][diff]表示以第i个数结尾，公差为diff的数列个数。由于这里的diff跨度很大，因此这里的f[i]需要以dict的形式储存。

对于f[i][diff]，若存在j，满足j \< i且A[i] - A[j] \= diff，那么在以j为结尾，公差为diff的数列后面加上一项A[i]同样是满足条件的，此时形成的等差数列必然是大于等于三项的，于是这里就应该将f[j][diff]加入到答案中。而对于f[i][diff]，除了从f[j][diff]继承过来的数列之外，仅包含A[j]、A[i]这两项的数列也应该计入f[i][diff]，于是有f[i][diff] +\= f[j][diff] + 1。

最后附上python代码：

```python
class Solution(object):
    def numberOfArithmeticSlices(self, A):
        """
        :type A: List[int]
        :rtype: int
        """

        f = []
        ans = 0
        for i in range(len(A)):
            f.append({})
            for j in range(i):
                diff = A[j] - A[i]
                cnt = f[j].get(diff, 0)
                f[i][diff] = f[i].get(diff, 0) + cnt + 1
                ans += cnt
        return ans
```
