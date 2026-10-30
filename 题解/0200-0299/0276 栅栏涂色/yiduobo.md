---
title: "276. 栅栏涂色"
aliases: ["yiduobo的每日leetcode 276.栅栏涂色"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/594294623"
zhihu_id: "594294623"
zhihu_title: "yiduobo的每日leetcode 276.栅栏涂色"
question_id: "276"
question: "栅栏涂色"
problem_url: "https://leetcode.cn/problems/paint-fence/"
created: "2022-12-26T01:04:23+08:00"
updated: "2022-12-26T01:04:23+08:00"
upvotes: 0
comments: 0
---

# 276. 栅栏涂色

> **[yiduobo的每日leetcode 276.栅栏涂色](https://zhuanlan.zhihu.com/p/594294623) · 知乎 · 2022-12-26 · 赞同 0**
> 力扣：[276. 栅栏涂色](https://leetcode.cn/problems/paint-fence/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

276.栅栏涂色

[力扣](https://leetcode.cn/problems/paint-fence/)

经典的动态规划问题。令f[i]表示前i个栅栏，最后两个栅栏颜色相同时的涂色方案数，而g[i]则表示前i个栅栏，最后两个栅栏颜色不同时的涂色方案数，那么：

f[i] \= g[i - 1]

g[i] \= (f[i - 1] + g[i - 1]) \* (k - 1)

其中，f[i]的转移方程表示最后一个栅栏涂上了与倒数第二根相同的颜色，而g[i]的转移方程则表示最后一个栅栏涂上了与倒数第二根不同的颜色。

全部计算完成后，f[-1] + g[-1]就是最终答案。

另外，注意到f和g的每一轮只与上一轮有关，因此可以利用滚动省去i这一维。

最后附上python代码：

```python
class Solution(object):
    def numWays(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """

        f, g = 0, k
        for index in range(1, n):
            f, g = g, (f + g) * (k - 1) 
        
        return f + g
```
