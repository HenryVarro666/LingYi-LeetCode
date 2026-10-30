---
title: "526. 优美的排列"
aliases: ["yiduobo的每日leetcode 526.优美的排列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261163678"
zhihu_id: "261163678"
zhihu_title: "yiduobo的每日leetcode 526.优美的排列"
question_id: "526"
question: "优美的排列"
problem_url: "https://leetcode.cn/problems/beautiful-arrangement/"
difficulty: "Medium"
created: "2020-10-03T20:29:09+08:00"
updated: "2020-10-03T20:29:09+08:00"
upvotes: 0
comments: 0
---

# 526. 优美的排列

> **[yiduobo的每日leetcode 526.优美的排列](https://zhuanlan.zhihu.com/p/261163678) · 知乎 · 2020-10-03 · 赞同 0**
> 力扣：[526. 优美的排列](https://leetcode.cn/problems/beautiful-arrangement/) · Medium · 灵茶山艾府：[教你一步步思考状压 DP：从记忆化搜索到递推，附题单（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

526.优美的排列<https://leetcode-cn.com/problems/beautiful-arrangement/>

看到排列和n小于等于15，立马就想到了状态压缩动态规划。使用1 \<\< (num - 1)来表示数字num，那么对于一个状态status，可以枚举1到N，通过status & (1 \<\< (nums - 1))来确定num是否已经被使用过。

简单起见，我们尝试从排列的最后一位开始往前选择数字。令f[now]表示剩下的数为now时可行的排列数，那么我们可以枚举1到N，通过上面的做法检测当前还有哪些数没有被使用，同时统计出没使用过数的个数k。接下来，就是需要从这些数中选择一个num放在排列的第k位上，这里的num需要满足k % num \= 0或者num % k \= 0。于是对于f[now]而言，就有

f[now] \= sum(f[num])，其中num为now中还存在的数且满足k % num \= 0或num % k \= 0

f[1 \<\< N - 1]即为答案。

最后附上python代码，方便起见，我在这里用的记忆化搜索：

```python
class Solution(object):
    def countArrangement(self, N):
        """
        :type N: int
        :rtype: int
        """

        f = [None] * (1 << N)
        return self.dfs((1 << N) - 1, N, f)

    def dfs(self, now, N, f):
        if f[now] is not None:
            return f[now]
        if now == 0:
            f[now] = 1
            return 1

        rest_num = set()
        for num in range(N):
            if now & (1 << num):
                rest_num.add(num + 1)
        
        f[now] = 0
        for num in rest_num:
            if len(rest_num) % num == 0 or num % len(rest_num) == 0:
                f[now] += self.dfs(now - (1 << num - 1), N, f)
        
        return f[now]
```
