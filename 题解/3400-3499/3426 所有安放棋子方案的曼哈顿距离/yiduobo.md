---
title: "3426. 所有安放棋子方案的曼哈顿距离"
aliases: ["yiduobo的每日leetcode 3426.所有安放棋子方案的曼哈顿距离"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/combinatorics", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1889459307713655616"
zhihu_id: "1889459307713655616"
zhihu_title: "yiduobo的每日leetcode 3426.所有安放棋子方案的曼哈顿距离"
question_id: "3426"
question: "所有安放棋子方案的曼哈顿距离"
problem_url: "https://leetcode.cn/problems/manhattan-distances-of-all-arrangements-of-pieces/"
difficulty: "Hard"
rating: 2443
created: "2025-03-30T00:08:26+08:00"
updated: "2025-03-30T00:08:26+08:00"
upvotes: 0
comments: 0
---

# 3426. 所有安放棋子方案的曼哈顿距离

> **[yiduobo的每日leetcode 3426.所有安放棋子方案的曼哈顿距离](https://zhuanlan.zhihu.com/p/1889459307713655616) · 知乎 · 2025-03-30 · 赞同 0**
> 力扣：[3426. 所有安放棋子方案的曼哈顿距离](https://leetcode.cn/problems/manhattan-distances-of-all-arrangements-of-pieces/) · Hard · 灵茶山艾府：[贡献法，预处理后 O(1)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3426.所有安放棋子方案的曼哈顿距离

[3426. 所有安放棋子方案的曼哈顿距离 - 力扣（LeetCode）](https://leetcode.cn/problems/manhattan-distances-of-all-arrangements-of-pieces/description/)

题目给出三个整数m、n、k，表示给出一个大小为m \* n的矩形格子，其中包含k个相同的棋子。n、m、n \* m、k的规模都可达10^5。

现在要求返回所有防止棋子的合法方案中，每对棋子之间的曼哈顿距离之和。合法方案指的是所有k个棋子都放在格子中，且每个格子中至多只有一枚棋子。

最终答案很大，需要对10^9 + 7取模。

题目的数据规模很大，只能考虑用组合数学进行求解。注意到题目需要计算的是每对棋子间的曼哈顿距离之和，那么可以考虑使用贡献法。最直观的思路就是直接枚举一对棋子的下标(x1, y1)、(x2, y2)，那么这一对棋子的距离就是dis \= abs(x1 - x2) + abs(y1 - y2)，而对于这一对棋子，另外k - 2枚棋子在棋盘上放置的方案数为C(m \* n - 2, k - 2)，也就是说这一对棋子的总贡献为dis \* C(m \* n - 2, k - 2)。

由于取模的存在，那么对于组合数的计算，还需要计算逆元，不过这个组合数是个定值，可以先预处理好。关于乘法逆元的计算可以参考之前的3405题：

[yiduobo：yiduobo的每日leetcode 3405.统计恰好有K个相等相邻元素的数组数目](https://zhuanlan.zhihu.com/p/31401526455)

那么最终的时间复杂度就是枚举棋子对的复杂度O((mn)^2)，还需要进行优化。

一种自然的想法就是枚举所有的曼哈顿距离，计算出与当前枚举到的曼哈顿距离相等的点对数量，不过曼哈顿距离相等的点对是个菱形，在边界的计算上感觉会很困难。

另一种思路则是固定住点对中的一个点，然后计算另一个点到这个固定点的曼哈顿距离之和。不过这种方法依然需要计算菱形边上节点的数量，在边界的计算上还是很困难。

由于题目需要计算的是曼哈顿距离，那么不妨将其拆分成水平上的距离和竖直上的距离，这样一来第二种方法似乎就可行了。对于固定的点(i, j)，首先考虑其他点到(i, j)的水平距离之和：

1、对于处于第0列到第j - 1列的所有节点：

对于位于(x, y)的节点，其与(i, j)的水平距离为j - y。

y的取值范围在0到j - 1，而对于每个y，都有m个可行的x，因此这些节点到(i, j)的水平距离之和为

j \* m + (j - 1) \* m + ... + m \= m \* ((1 + j) \* j // 2)

2、对于处于第j列的，除(i, j)之外的所有节点：

这些节点与(i, j)的水平距离为0，无需计算

3、对于处于第j + 1列到n - 1列的所有节点：

对于位于(x, y)的节点，其与(i, j)的水平距离为y - j。

y的取值范围在j + 1到n - 1，同样的对于每个y，都有m个可行的x，因此这些节点到(i, j)的水平距离之和为

m + 2 \* m + ... + (n - 1 - j) \* m \= m \* ((n - j) \* (n - j - 1) // 2)

综合起来，就可以计算出对于一对棋子，其中一个棋子固定在了(i, j)，那么这一对棋子对最终答案在水平距离上的贡献就是m \* ((1 + j) \* j // 2 + (n - j) \* (n - j - 1) // 2)。

与水平距离对称，竖直距离上的贡献则为n \* ((1 + i) \* i // 2 + (m - i) \* (m - i - 1) // 2)。

将这二者之和累加，然后乘以C(m \* n - 2, k - 2)就是这一对棋子对最终答案的贡献。

接下来只需枚举每个固定的(i, j)，将所有贡献累加起来，然后除以2即为最终答案。这里除以2的理由是对于每一对棋子，在枚举固定的(i, j)时两个棋子都作为固定的棋子被枚举了一次，相当于所有的距离都被计算了两次，所以最终答案需要除以2。另外需要注意这里是在取模的语境下，所以处理2应该乘以2的逆元后取模。

最后附上python代码：

```python
class Solution(object):
    def distanceSum(self, m, n, k):
        """
        :type m: int
        :type n: int
        :type k: int
        :rtype: int
        """
        
        c = 1
        mod = 10 ** 9 + 7
        for v in range(1, m * n - 1):
            c = c * v % mod
        
        inv = [None, 1]
        for v in range(2, max(3, k - 1, m * n - k + 1)):
            inv.append((mod - mod // v) * inv[mod % v] % mod)

        for v in range(1, k - 1):
            c = c * inv[v] % mod
        
        for v in range(1, m * n - k + 1):
            c = c * inv[v] % mod

        print c

        res = 0
        for i in range(m):
            for j in range(n):
                diff_x = n * ((1 + i) * i // 2 + (m - i) * (m - i - 1) // 2) % mod
                diff_y = m * ((1 + j) * j // 2 + (n - j) * (n - j - 1) // 2) % mod
                res = (res + (diff_x + diff_y) * c) % mod
        
        return res * inv[2] % mod
```
