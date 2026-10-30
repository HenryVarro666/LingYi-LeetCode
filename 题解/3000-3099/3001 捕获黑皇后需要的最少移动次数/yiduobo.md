---
title: "3001. 捕获黑皇后需要的最少移动次数"
aliases: ["yiduobo的每日leetcode 3001.捕获黑皇后需要的最少移动次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/693088697"
zhihu_id: "693088697"
zhihu_title: "yiduobo的每日leetcode 3001.捕获黑皇后需要的最少移动次数"
question_id: "3001"
question: "捕获黑皇后需要的最少移动次数"
problem_url: "https://leetcode.cn/problems/minimum-moves-to-capture-the-queen/"
difficulty: "Medium"
rating: 1797
created: "2024-04-18T00:39:54+08:00"
updated: "2024-04-18T00:39:54+08:00"
upvotes: 1
comments: 0
---

# 3001. 捕获黑皇后需要的最少移动次数

> **[yiduobo的每日leetcode 3001.捕获黑皇后需要的最少移动次数](https://zhuanlan.zhihu.com/p/693088697) · 知乎 · 2024-04-18 · 赞同 1**
> 力扣：[3001. 捕获黑皇后需要的最少移动次数](https://leetcode.cn/problems/minimum-moves-to-capture-the-queen/) · Medium · 灵茶山艾府：[分类讨论+简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3001.捕获黑皇后需要的最少移动次数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-moves-to-capture-the-queen/)

首先，如果车或者象可以一步到位，即车与皇后在同一行或同一列，且没有被象挡住，或者象与皇后在同一左对角线或者同一右对角线，且没有被车挡住，那么答案就是一。

接下来，如果不满足上面的条件，那么车是一定可以通过一次水平的移动加上一次竖直的移动到达皇后的位置的，在这里可以先水平后竖直，或者先竖直后水平。由于这两条路径没有交叉，也就意味着象最多挡住其中的一条路径，因此在这种情况下车花费两次操作是一定可以到达皇后的位置的，答案就是二。

最后附上python代码：

```python
class Solution(object):
    def minMovesToCaptureTheQueen(self, a, b, c, d, e, f):
        """
        :type a: int
        :type b: int
        :type c: int
        :type d: int
        :type e: int
        :type f: int
        :rtype: int
        """

        if a == e and (c != a or d < min(b, f) or d > max(b, f)):
            return 1
        
        if b == f and (d != b or c < min(a, e) or c > max(a, e)):
            return 1
        
        if e - f == c - d and (a - b != c - d or a < min(c, e) or a > max(c, e)):
            return 1
        
        if e + f == c + d and (a + b != c + d or a < min(c, e) or a > max(c, e)):
            return 1
        
        return 2
```
