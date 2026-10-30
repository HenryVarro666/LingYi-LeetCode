---
title: "837. 新21点"
aliases: ["yiduobo的每日leetcode 837.新21点"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/sliding-window", "题单/动态规划", "题单/数学算法", "题单/动态规划/十一-优化-DP", "题单/动态规划/十五-概率-DP-期望-DP", "题单/数学算法/三-概率期望"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/346547667"
zhihu_id: "346547667"
zhihu_title: "yiduobo的每日leetcode 837.新21点"
question_id: "837"
question: "新 21 点"
problem_url: "https://leetcode.cn/problems/new-21-game/"
difficulty: "Medium"
rating: 2350
created: "2021-01-25T13:04:23+08:00"
updated: "2021-01-25T13:04:23+08:00"
upvotes: 0
comments: 0
---

# 837. 新21点

> **[yiduobo的每日leetcode 837.新21点](https://zhuanlan.zhihu.com/p/346547667) · 知乎 · 2021-01-25 · 赞同 0**
> 力扣：[837. 新 21 点](https://leetcode.cn/problems/new-21-game/) · Medium · 灵茶山艾府：[滑动窗口优化 DP，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

837.新21点

[力扣](https://leetcode-cn.com/problems/new-21-game/)

经典的动态规划问题，令f[x]表示当前点数为x时最终要求的概率是多少，那么对于f[x]：

1、若x>\=K，那么此时应该判断x是否大于N，若大于，则f[x]等于0，否则等于1

2、其他情况下，都需要等概率从1到W之间抽一张，因此有

f[x] \= (f[x + 1] + f[x + 2] + ... + f[x + w]) / w

注意到上面这个式子中出现了序列连加，因此可以使用前缀和或者类似二项式定理来进行优化。我在这里采用的是后者，即

f[x] \= (f[x + 1] + f[x + 2] + ... + f[x + w]) / w

f[x + 1] \= (f[x + 2] + f[x + 3] + ... + f[x + w + 1]) / w

下式减去上式就有

f[x + 1] - f[x] \= (f[x + w + 1] - f[x + 1]) / w

化简后可得

f[x] \= f[x + 1] + (f[x +1] - f[x + w + 1]) / w

不过需要注意边界条件，对于x \= K - 1时，f[x + 1] \= f[K]不再符合上面的递推式，因此需要先对f[K - 1]进行单独处理。此时需要按照最原始的递推式

f[x] \= (f[x + 1] + f[x + 2] + ... + f[x + w]) / w

来求解f[K - 1]

最后附上python代码：

```python
class Solution(object):
    def new21Game(self, N, K, W):
        """
        :type N: int
        :type K: int
        :type W: int
        :rtype: float
        """

        f = [None] * (K + W)
        return self.dfs(0, N, K, W, f)

    def dfs(self, now, N, K, W, f):
        if f[now] is None:
            if now >= K:
                if now <= N:
                    f[now] = 1.0
                else:
                    f[now] = 0.0
            elif now == K - 1:
                tmp = 0
                for index in range(1, W + 1):
                    if now + index <= N:
                        tmp += 1
                f[now] = tmp * 1.0 / W
            else:
                f[now] = self.dfs(now + 1, N, K, W, f) + (self.dfs(now + 1, N, K, W, f) - self.dfs(now + W + 1, N, K, W, f)) / W
            
        return f[now]
```
