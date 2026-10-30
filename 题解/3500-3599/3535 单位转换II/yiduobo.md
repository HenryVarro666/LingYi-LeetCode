---
title: "3535. 单位转换II"
aliases: ["yiduobo的每日leetcode 3535.单位转换II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1905760687638177664"
zhihu_id: "1905760687638177664"
zhihu_title: "yiduobo的每日leetcode 3535.单位转换II"
question_id: "3535"
question: "单位转换II"
problem_url: "https://leetcode.cn/problems/unit-conversion-ii/"
created: "2025-05-16T22:00:33+08:00"
updated: "2025-05-16T22:00:33+08:00"
upvotes: 1
comments: 0
---

# 3535. 单位转换II

> **[yiduobo的每日leetcode 3535.单位转换II](https://zhuanlan.zhihu.com/p/1905760687638177664) · 知乎 · 2025-05-16 · 赞同 1**
> 力扣：[3535. 单位转换II](https://leetcode.cn/problems/unit-conversion-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3535.单位转换II

[3535. 单位转换 II - 力扣（LeetCode）](https://leetcode.cn/problems/unit-conversion-ii/)

题目给出一个整数n，表示有n种单位，编号为0到n - 1。另外给出一个二维整数数组conversions，其长度为n - 1，其中conversions\[index\] \= \[source\[index\], target\[index\], factor\[index\]\]，表示一个source类型的单位等于factor\[index\]个target类型的单位。

另外给出一个长度为q的二维数组queries，其中queries\[index\] \= \[A\[index\], B\[index\]\]，表示要求计算一个A类型单位可以转换为多少个B类型单位。若转换结果写作分数为p / q，且p和q互质，那么要求返回p \* inv\[q\] % mod的结果，其中mod \= 10^9 + 7，而inv\[q\]表示q在模mod下的乘法逆元。

题目保证单位0可以通过正向或者反向的组合唯一地转换为任何其他单位。

之前3528题的加强版，本题中可以进行反向转换，并且需要计算的是任意两点之间的转换路径汇率，不过做法还是差不多，依然是建图后从0号节点开始做bfs，计算其到其他节点的汇率。不过需要注意的是这里的建图需要建双向边，对于一组conversions\[index\] \= \[source\[index\], target\[index\], factor\[index\]\]，除了建立source\[index\]到target\[index\]的权重为factor\[index\]的边之外，还需要建立target\[index\]到source\[index\]的权重为inv\[factor\[index\]\]的边，这里的inv指的是模mod的乘法逆元。

bfs完成后，不妨记为0号节点到节点x的汇率为dis\[x\]，那么对于一组询问中的\[a, b\]，最终的转换结果就是dis\[b\] \* inv\[dis\[a\]\] % mod。

另外对于乘法逆元的计算，在本题中使用费马小定理来求是比较方便的。对于质数p，正整数a满足a^(p - 1) % p \= 1，写成同余的形式就是a^(p - 1) ≡ 1 (mod p)，然后左边拆一个a出来，就是a \* a^(p - 2) ≡ 1 (mod p)。而现在要计算的a乘法逆元满足a \* inv[a] ≡ 1 (mod p)，那么就有inv[a] ≡ a^(p - 2) (mod p)。对于本题，将p \= 10^9 + 7带入进去计算快速幂就行了。

最后附上python代码：

```python
class Solution(object):
    def queryConversions(self, conversions, queries):
        """
        :type conversions: List[List[int]]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        mod = 10 ** 9 + 7
        
        def quick_pow(base, p):
            if p == 0:
                return 1
            if p == 1:
                return base
            
            res = quick_pow(base, p // 2)
            res = res * res % mod
            if p & 1:
                res = res * base % mod
            return res
        
        n = len(conversions) + 1
        g = [[] for _ in range(n)]
        for x, y, w in conversions:
            g[x].append((y, w))
            g[y].append((x, quick_pow(w, mod - 2)))
        
        q = deque()
        q.append(0)
        dis = [None] * n
        dis[0] = 1
        while q:
            now = q.popleft()
            for nxt, w in g[now]:
                if dis[nxt] is None:
                    dis[nxt] = dis[now] * w % mod
                    q.append(nxt)
        
        res = []
        for x, y in queries:
            res.append(quick_pow(dis[x], mod - 2) * dis[y] % mod)
        return res
```
