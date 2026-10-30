---
title: "474. 一和零"
aliases: ["yiduobo的每日leetcode 474.一和零"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/三-背包"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/238203210"
zhihu_id: "238203210"
zhihu_title: "yiduobo的每日leetcode 474.一和零"
question_id: "474"
question: "一和零"
problem_url: "https://leetcode.cn/problems/ones-and-zeroes/"
difficulty: "Medium"
created: "2020-09-12T23:15:16+08:00"
updated: "2020-09-12T23:15:16+08:00"
upvotes: 0
comments: 1
---

# 474. 一和零

> **[yiduobo的每日leetcode 474.一和零](https://zhuanlan.zhihu.com/p/238203210) · 知乎 · 2020-09-12 · 赞同 0**
> 力扣：[474. 一和零](https://leetcode.cn/problems/ones-and-zeroes/) · Medium · 灵茶山艾府：[一步步思考：从记忆化搜索到递推到空间优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

474.一和零<https://leetcode-cn.com/problems/ones-and-zeroes/>

背包问题的变种。可以将问题看成，有若干个str，选择其中某个str需要花费x个0和y个1，现在给出一定量的0和1最多可以拿多少个str。

做法依然是动态规划，可以用f\[i\]\[j\]\[k\]表示对于前i个str，花费j个0和k个1最多可以拿到多少个str，状态转移方程为f\[i\]\[j\]\[k\] \= max(f\[i\]\[j\]\[k\], f\[i - 1\]\[j - zero\[i\]\]\[k - one\[i\]\] + 1)。

同样的，由于这里i这一维每次只会由i - 1更新过来，因此可以使用滚动数组进行优化，即使用f[i][j]表示使用i个0和j个1最多可以拿到多少个str，然后对于每个str从大到小循环i和j更新状态。

最后附上python代码：

```python
class Solution(object):
    def findMaxForm(self, strs, m, n):
        """
        :type strs: List[str]
        :type m: int
        :type n: int
        :rtype: int
        """

        f = [[0] * (n + 1) for _ in range(m + 1)]

        for str in strs:
            zero_cnt = one_cnt = 0
            for char in str:
                if char == '0':
                    zero_cnt += 1
                else:
                    one_cnt += 1
            for i in range(m, zero_cnt - 1, -1):
                for j in range(n, one_cnt - 1, -1):
                    f[i][j] = max(f[i][j], f[i - zero_cnt][j - one_cnt] + 1)
        
        res = 0
        for i in range(m + 1):
            for j in range(n + 1):
                res = max(f[i][j], res)
        
        return res
```
