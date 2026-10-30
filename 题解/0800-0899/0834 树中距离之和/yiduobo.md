---
title: "834. 树中距离之和"
aliases: ["yiduobo的每日leetcode 834.树中距离之和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/346315645"
zhihu_id: "346315645"
zhihu_title: "yiduobo的每日leetcode 834.树中距离之和"
question_id: "834"
question: "树中距离之和"
problem_url: "https://leetcode.cn/problems/sum-of-distances-in-tree/"
difficulty: "Hard"
rating: 2197
created: "2021-01-24T22:39:45+08:00"
updated: "2021-01-24T22:39:45+08:00"
upvotes: 2
comments: 0
---

# 834. 树中距离之和

> **[yiduobo的每日leetcode 834.树中距离之和](https://zhuanlan.zhihu.com/p/346315645) · 知乎 · 2021-01-24 · 赞同 2**
> 力扣：[834. 树中距离之和](https://leetcode.cn/problems/sum-of-distances-in-tree/) · Hard · 灵茶山艾府：[【图解】一张图秒懂换根 DP！（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

834.树中距离之和

[力扣](https://leetcode-cn.com/problems/sum-of-distances-in-tree/)

很有意思的题目，平方的做法是很容易想到的，枚举每个节点，将树的结构调整成以该节点为根的树，然后进行一趟dfs即可求出该节点到其他节点的距离之和。

dfs求解的具体过程为，对于当前节点now，设其有若干个孩子节点，分别为son0，son1，...，sonK，那么我们可以先递归求解以son0，son1，...，sonK这些节点为根节点的子树中，各个节点到其根节点son的距离之和dis0，dis1，...，disK。

递归求解完成之后，对于now而言，其到son0为根节点的子树中所有节点的距离应该等于son0到对应节点的距离加1。不妨设以son0为根节点的子树中一共有p0个其他节点，那么从now到son0中所有节点的距离之和就应该是dis0 + p0 + 1，其中的加1表示的是从now到son0的距离。同理，对于任意的sonM而言，now到以sonM为根节点的子树中所有节点的距离之和就是disM + pM + 1。

根据上面的结论，我们就可以得到now到以now为根节点的子树中所有节点的距离之和等于

dis0 + p0 + 1 + dis1 + p1 + 1 + ... + disK + pK + 1

另一方面，pNow则等于

p0 + 1 + p1 + 1 + ... + pK + 1

于是最后就有

disNow \= dis0 + dis1 + ... + disK + pNow

例如样例中的节点2，可知dis2 \= 3，p2 \= 3，那么对于节点0而言，其到以节点2为根节点的子树的所有节点的距离之和应该为

0到2：1

0到3：2

0到4：2

0到5：2

合计为7

而如果使用上面的方法，则为

dis2：3

p2：3

加上表示节点2的1

合计同样为7

到了这里，我们就有了一种O(N^2)的做法。不过仔细想一下，树中的距离被多次重复求解了，特别是父子节点之间的距离信息没有得到有效的利用。基于这个思路，我们首先对于根节点进行一趟dfs，求解出dis和p，然后考察根节点的孩子节点。

同样是考察节点2，此时我们已经有了节点0到其他所有节点的距离之和f0，那么对于节点2而言，可以做如下变化：

2到0：即为0到2的距离

2到1：可以看做0到1的距离**加上**0到2的距离

2到3：可以看做0到3的距离**减去**0到2的距离

2到4：可以看做0到4的距离**减去**0到2的距离

2到5：可以看做0到5的距离**减去**0到2的距离

可以发现，上面的值可以分为两类，分别是0到X的距离以及0到2的距离。对于前者而言，各项之和就是之前已经求解完毕的0到其他所有节点的距离之和，而仔细观察后者可以发现，其中做减法的都是以2为根节点的子树中的其他节点，而对于其他节点则应该做加法。

假设这里所有节点都是做加法的话，那么最终就应该是N - 2，这里的减2表示的是2以及2的父亲节点0这两个节点。但是实际上，有p2次加法应该修改为减法，因此最终需要减去两倍的p2，那么后面的部分应该写成N - 2 - 2 \* p2

那么此时就可以得到f2 \= f0 + N - 2 - 2 \* p2

更一般地，如果我们严格按照dfs来进行求解，那么对于任意节点，我们都可以得到

fX \= fY + N - 2 - 2 \* pX，其中y为x的父亲节点

到了这里，就有了一种O(n)的做法：

1、从根节点开始进行dfs，dfs过程中需要记录子树节点数量以及到子树根节点的距离之和，同时还需要记录dfs序

2、按dfs序遍历每个节点，通过当前节点父亲的结果来计算当前节点的结果

最后附上python代码：

```python
class Solution(object):
    def sumOfDistancesInTree(self, N, edges):
        """
        :type N: int
        :type edges: List[List[int]]
        :rtype: List[int]
        """

        tree = {x : set() for x in range(N)}
        for x, y in edges:
            tree[x].add(y)
            tree[y].add(x)
        used = [False] * N
        sons = [0] * N
        fa = [0] * N
        used[0] = True
        order = []
        res = [0] * N
        res[0] = self.dfs(0, 0, order, used, sons, fa, tree)
        for now in order:
            res[now] = res[fa[now]] + N - 2 - sons[now] * 2
        return res

    def dfs(self, now, dis, order, used, sons, fa, tree):
        tmp = 0
        for next in tree[now]:
            if not used[next]:
                used[next] = True
                order.append(next)
                fa[next] = now
                tmp += self.dfs(next, dis + 1, order, used, sons, fa, tree)
                sons[now] += sons[next] + 1
        
        return sons[now] + tmp
```
