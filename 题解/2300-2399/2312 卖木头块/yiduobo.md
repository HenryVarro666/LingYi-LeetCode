---
title: "2312. 卖木头块"
aliases: ["yiduobo的每日leetcode 2312.卖木头块"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/556061033"
zhihu_id: "556061033"
zhihu_title: "yiduobo的每日leetcode 2312.卖木头块"
question_id: "2312"
question: "卖木头块"
problem_url: "https://leetcode.cn/problems/selling-pieces-of-wood/"
difficulty: "Hard"
rating: 2363
created: "2022-08-21T00:14:29+08:00"
updated: "2022-08-21T00:14:29+08:00"
upvotes: 1
comments: 0
---

# 2312. 卖木头块

> **[yiduobo的每日leetcode 2312.卖木头块](https://zhuanlan.zhihu.com/p/556061033) · 知乎 · 2022-08-21 · 赞同 1**
> 力扣：[2312. 卖木头块](https://leetcode.cn/problems/selling-pieces-of-wood/) · Hard · 灵茶山艾府：[动态规划：枚举切割位置+循环优化（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2312.卖木头块

[力扣](https://leetcode.cn/problems/selling-pieces-of-wood/)

由于题目中m和n的规模都不大，因此可以使用经典的二维动态规划来处理。

令f[i][j]表示高为i，宽为j的木头最多可以卖多少钱，那么对于f[i][j]：

1、若(i, j)恰好是prices中的某种尺寸，那么就可以将这块木头整个卖掉，此时就有f[i][j] \= max(f[i][j], p[(i, j)])。这里的p[(i, j)]表示(i, j)这个尺寸的木头的价格

2、可以尝试水平切割，枚举上半部分的高度index，这里的index满足1 \<\= index \< i，那么切分后两块木头就分别是(index, j)以及(i - index, j)，于是有f[i][j] \= max(f[i][j], f[index][j] + f[i - index][j])

3、也可以尝试竖直切割，枚举左半部分的宽度index，这里的index满足1 \<\= index \< j，那么切分后两块木头就分别是(i, index)以及(i, j - index)，于是有f[i][j] \= max(f[i][j], f[i][index] + f[i][j - index])

全部计算完成后，f[m][n]就是最终答案。

具体实现上，由于f[i][j]可能一来所有i或j更小的状态，因此在这里使用记忆化搜索而非常规的递推式动态规划会更方便一些。

最后附上python代码：

```python
class Solution(object):
    def sellingWood(self, m, n, prices):
        """
        :type m: int
        :type n: int
        :type prices: List[List[int]]
        :rtype: int
        """

        f = [[-1] * (n + 1) for _ in range(m + 1)]
        price_dict = {}

        for h, w, price in prices:
            price_dict[(h, w)] = price

        def dfs(h, w, f):
            if f[h][w] == -1:
                if (h, w) in price_dict:
                    f[h][w] = price_dict[(h, w)]
                else:
                    f[h][w] = 0

                for index in range(1, h):
                    f[h][w] = max(f[h][w], dfs(index, w, f) + dfs(h - index, w, f))
                
                for index in range(1, w):
                    f[h][w] = max(f[h][w], dfs(h, index, f) + dfs(h, w - index, f))
            
            return f[h][w]
            
        return dfs(m, n, f)
```
