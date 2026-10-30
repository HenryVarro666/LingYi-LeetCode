---
title: "2008. 出租车的最大盈利"
aliases: ["yiduobo的每日leetcode 2008.出租车的最大盈利"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/503776720"
zhihu_id: "503776720"
zhihu_title: "yiduobo的每日leetcode 2008.出租车的最大盈利"
question_id: "2008"
question: "出租车的最大盈利"
problem_url: "https://leetcode.cn/problems/maximum-earnings-from-taxi/"
difficulty: "Medium"
rating: 1872
created: "2022-04-23T21:52:56+08:00"
updated: "2022-04-23T21:52:56+08:00"
upvotes: 1
comments: 0
---

# 2008. 出租车的最大盈利

> **[yiduobo的每日leetcode 2008.出租车的最大盈利](https://zhuanlan.zhihu.com/p/503776720) · 知乎 · 2022-04-23 · 赞同 1**
> 力扣：[2008. 出租车的最大盈利](https://leetcode.cn/problems/maximum-earnings-from-taxi/) · Medium · 灵茶山艾府：[教你一步步思考动态规划：从记忆化搜索到递推（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2008.出租车的最大盈利

[力扣](https://leetcode-cn.com/problems/maximum-earnings-from-taxi/)

题目实际上是给出了若干区间，每个区间都有一个权重，要求从中选出若干不相交的区间，使得这些区间权重之和最大。

对于这类区间选择问题，常见的做法是将区间按照起点或者终点排序，然后采用贪心或者动态规划来进行求解。

对于本题，可以按照区间的结尾从小到大进行排序，然后令f[i]表示前i个区间，以第i个区间结尾时的最大收益。那么对于f[i]，设第i个区间的左右边界以及权重分别为(l, r, v)。由于已经将区间按结尾排好序了，那么就必然存在一个j，满足前j个区间的右边界都小于等于l，那么就有

f[i] \= max(f[i], f[j] + v)

表示在f[j]的基础上加入了第i个区间。

这个过程是O(m^2)的，其中m表示的是区间的数目。

注意到这里转移的过程实际上是求一个区间最值，而且还是最特殊的前缀区间最值，那么完全可以使用树状数组或者线段树来进行优化，最终可以得到一种时间复杂度为O(mlogm)的算法。

除此之外，注意到题目中n的范围比较小，那么也可以使用另一种状态表示，令f[i]表示到位置i为止所能取得的最大收益。那么对于f[i]，如果最后这一段什么都没干，就有f[i] \= f[i - 1]。除此之外，也可以选择任意右边界为r \= i的区间，那么就有f[i] \= f[l] + v。

这个做法看上去是O(mn)的，但是随着i的向后移动，选择的最后这个区间下标也是单调递增的，因此在这里同样可以将区间按右边界进行排序，利用单调性将转移的复杂度优化到均摊O(1)。这样一来，最终的时间复杂度就是O(mlogm + n)，与上面的复杂度差不多。

我在这里选择的是做法2，实现起来相对方便点。

最后附上python代码：

```python
class Solution(object):
    def maxTaxiEarnings(self, n, rides):
        """
        :type n: int
        :type rides: List[List[int]]
        :rtype: int
        """

        rides = sorted(rides, key=lambda d:d[1])
        f = [0] * (n + 1)

        p = 0
        for index in range(1, n + 1):
            f[index] = f[index - 1]
            while p < len(rides) and rides[p][1] == index:
                f[index] = max(f[index], f[rides[p][0]] + rides[p][1] - rides[p][0] + rides[p][2])
                p += 1
        
        return f[-1]
```
