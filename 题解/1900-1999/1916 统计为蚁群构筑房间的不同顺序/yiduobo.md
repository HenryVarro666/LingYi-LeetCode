---
title: "1916. 统计为蚁群构筑房间的不同顺序"
aliases: ["yiduobo的每日leetcode 1916.统计为蚁群构筑房间的不同顺序"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/math", "leetcode/combinatorics", "题单/动态规划", "题单/数学算法", "题单/动态规划/十二-树形-DP", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/484287809"
zhihu_id: "484287809"
zhihu_title: "yiduobo的每日leetcode 1916.统计为蚁群构筑房间的不同顺序"
question_id: "1916"
question: "统计为蚁群构筑房间的不同顺序"
problem_url: "https://leetcode.cn/problems/count-ways-to-build-rooms-in-an-ant-colony/"
difficulty: "Hard"
rating: 2486
created: "2022-03-20T19:49:03+08:00"
updated: "2022-03-20T19:49:03+08:00"
upvotes: 0
comments: 0
---

# 1916. 统计为蚁群构筑房间的不同顺序

> **[yiduobo的每日leetcode 1916.统计为蚁群构筑房间的不同顺序](https://zhuanlan.zhihu.com/p/484287809) · 知乎 · 2022-03-20 · 赞同 0**
> 力扣：[1916. 统计为蚁群构筑房间的不同顺序](https://leetcode.cn/problems/count-ways-to-build-rooms-in-an-ant-colony/) · Hard · 灵茶山艾府：[简单做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1916.统计为蚁群构筑房间的不同顺序

[力扣](https://leetcode-cn.com/problems/count-ways-to-build-rooms-in-an-ant-colony/)

经典的组合数学问题。令f[now]表示以now为根节点的子树有多少种构造方案，cnt[now]表示以now为根节点的子树中有多少个节点。那么对于now而言，一共有cnt[now]个节点。出去now自身需要优先构造之外，剩下cnt[now] - 1个节点理论上有(cnt[now] - 1)！种构造方案。

对于这(cnt[now] - 1)！种方案，都可以视为一个排列。不妨设k是now的一个孩子，那么k这颗子树中的节点一共为cnt[k]个，也就意味着将在所有排列中占据cnt[k]个位置。不考虑形态的话，这cnt[k]个位置一共可以提供cnt[k]！种构造方案，但是由于构造有先后顺序，因此实际上合法的构造只有f[k]种，于是此时就应该除以cnt[k]！，再乘以f[k]。

根据这个结论，就有了一种做法。从0开始向下dfs，对于当前节点now：

1、首先递归求解now的所有孩子节点，并记录对应的f和cnt

2、接下来可以通过所有孩子节点的cnt计算出以now为根节点的子树中所有节点的数目，记为tot_cnt

3、最后先初始化f[now] \= (tot_cnt - 1)！，然后遍历所有的孩子k，更新f[now]为f[now] \* f[k] / (cnt[k]！)

这里阶乘计算太大，不可能先算完了再取模，而是需要边算边取模，因此还需要优先预处理出阶乘对于mod的乘法逆元。由于mod是质数，因此在这里可以套用费马小定理，配合快速幂来求解，这里就不展开了。

另外，由于f和cnt只会给父亲节点使用，因此我在这里直接使用的变量迭代而没有使用数组。

最后附上python代码，其中fac[i]表示i！对mod取模的结果，inv_fac[i]表示i！对mod的乘法逆元：

```python
class Solution(object):
    def waysToBuildRooms(self, prevRoom):
        """
        :type prevRoom: List[int]
        :rtype: int
        """

        n = len(prevRoom)
        mod = 10 ** 9 + 7

        fac = [1]
        inv_fac = [1]
        for num in range(1, n + 1):
            fac.append(fac[-1] * num % mod)
            inv_fac.append(self.quickPow(fac[-1], mod - 2, mod))
        
        sons = {index : set() for index in range(n)}
        for index, fa in enumerate(prevRoom):
            if index > 0:
                sons[fa].add(index)
        
        return self.dfs(0, sons, fac, inv_fac, mod)[0]
    
    def quickPow(self, base, p, mod):
        if p == 1:
            return base
        
        res = self.quickPow(base, p / 2, mod)
        res = res * res % mod
        if p % 2 == 1:
            res = res * base % mod
        
        return res

    def dfs(self, now, sons, fac, inv_fac, mod):
        res = 1
        tot_cnt = 1
        for son in sons[now]:
            ways, cnt = self.dfs(son, sons, fac, inv_fac, mod)
            res = res * ways % mod
            res = res * inv_fac[cnt] % mod
            tot_cnt += cnt
        
        res = res * fac[tot_cnt - 1] % mod

        return res, tot_cnt
```
