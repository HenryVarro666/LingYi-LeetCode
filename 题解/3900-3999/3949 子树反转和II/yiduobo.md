---
title: "3949. 子树反转和II"
aliases: ["yiduobo的每日leetcode 3949.子树反转和II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2047096033096758627"
zhihu_id: "2047096033096758627"
zhihu_title: "yiduobo的每日leetcode 3949.子树反转和II"
question_id: "3949"
question: "子树反转和II"
problem_url: "https://leetcode.cn/problems/subtree-inversion-sum-ii/"
created: "2026-06-08T00:09:24+08:00"
updated: "2026-06-08T00:09:24+08:00"
upvotes: 1
comments: 0
---

# 3949. 子树反转和II

> **[yiduobo的每日leetcode 3949.子树反转和II](https://zhuanlan.zhihu.com/p/2047096033096758627) · 知乎 · 2026-06-08 · 赞同 1**
> 力扣：[3949. 子树反转和II](https://leetcode.cn/problems/subtree-inversion-sum-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3949.子树反转和II

<https://leetcode.cn/problems/subtree-inversion-sum-ii/description/>

题目给出一颗以节点0为根节点包含n个节点的无向树，节点编号从0到n - 1。另外给出一个长度为n - 1的二维整数数组edges，其中edges\[index\] \= \[u\[index\], v\[index\]\]，表示u\[index\]和v\[index\]之间有一条边。

同时给出一个整数k以及长度为n的整数数组nums，其中nums[index]表示节点index的值。

现在可以对树中的部分节点执行反转操作：

- 反转一个节点时，以该节点为根的子树中的所有节点值都乘以-1
- 任意两个被反转的节点a和b之间的距离至少为k

问执行操作后树中节点值之和最大可能是多少。

对于这类在树中的选或者不选的问题，一种常见的思路是以子树为单位来执行动态规划。另外本题涉及到节点间距离的限制，那么在这里就可以使用f[now][d]表示，以now为根节点的子树中，与now距离最短的反转的节点，距离根节点的距离大于等于d时，树中节点值之和的最大值是多少。特别地，当d为now时，说明翻转了now，另外距离now大于d的情况统一归到f[now][d]当中。

这里可以简单说明一下，因为子树内部的反转距离限制一般是在递归计算时就解决掉了，因此主要需要考虑的还是兄弟子树间节点的距离。而对于以now为根节点的子树，其中的节点要到达其他子树的节点，必然会经过now，因此在这里可以通过维护最近的那个反转节点到d的距离，然后通过这些距离的组合找出合法且最大的反转方案。

除了f之外，在这里还需要另外使用一个g[now][d]，不过这里记录的是最小值。理由也很简单，因为目标是让节点值之和最大，而题目中的反转是反转整个子树，因此当now反转时，应该让now的孩子节点对应的子树取到最小值，这样才能让f[now]取到最大。

另外值得一提的是，基于f和g的定义，f[now]和g[now]显然都是单调的。

接下来考虑f[now]和g[now]的具体计算方法。

首先，自然还是先遍历now的所有孩子节点nxt，然后递归计算f[nxt]和g[nxt]。

接下来，根据d与k的关系，可以分出几种不同的情况：

1、当d为0时：

这种情况表示反转了now，因此对于now的任意孩子nxt，其中反转的节点与nxt的至少为k - 1，在这种情况下，任意两个nxt之间的反转节点距离必然大于k，因此无需考虑额外考虑不同nxt内的反转节点间的距离，于是有

f\[now\]\[0\] \= -(g\[nxt\[0\]\]\[k - 1\] + g\[nxt\[1\]\]\[k - 1\] + ... + g\[nxt\[-1\]\]\[k - 1\]) - nums\[now\]

g\[now\]\[0\] \= -(f\[nxt\[0\]\]\[k - 1\] + f\[nxt\[1\]\]\[k - 1\] + ... + f\[nxt\[-1\]\]\[k - 1\]) - nums\[now\]

需要注意，因为以now为根节点的子树中所有节点都反转了，因此在这里应该让f和g交叉更新

2、当d + d >\= k时：

这种情况下，任意两个nxt中的反转节点与now的距离之和，也就是d + d >\= k，因此同样无需考虑不同nxt内的反转节点间的距离。另一方面，对于任意一个nxt，其中与now距离为大于等于d的节点，相当于与nxt距离大于等于d - 1的节点，于是有

f\[now\]\[d\] \= f\[nxt\[0\]\]\[d - 1\] + f\[nxt\[1\]\]\[d - 1\] + ... + f\[nxt\[-1\]\]\[d - 1\] + nums\[now\]

g\[now\]\[d\] \= g\[nxt\[0\]\]\[d - 1\] + g\[nxt\]\[1\]\]\[d - 1\] + ... + g\[nxt\]\[-1\]\]\[d - 1\] + nums\[now\]

这里没有反转，因此f和g都由自己更新

3、当d不为0，且d + d \< k时：

对于这种情况，就需要考虑不同nxt之内反转节点的距离了。

更具体的，以f\[now\]\[d\]的更新举例：假设目前选中了某个f\[nxt\[p\]\]\[d - 1\]，那么对于其他的nxt\[q\]而言，其中可选的就只能是f\[nxt\[q\]\]\[k - d - 1\]，这样做的理由是f是单调的，因此在这里应该尽量让d更小，对应的f\[nxt\]\[q\]\]\[d\]才能最大。而受到f\[nxt\[p\]\]\[d - 1\]的限制，nxt\[q\]对应的d最多只能取到k - d - 1，其中反转节点的距离之和才不会超过d。

另一方面，对于不同的q1和q2，在取到f\[nxt\[q1\]\]\[k - d - 1\]以及f\[nxt\[q2\]\]\[k - d - 1\]\]时，其中反转节点的距离之和为k - d + k - d，而这种情况下d + d \< k，因此这个距离之和必然大于k，也就是说在这里无需考虑不同的nxt\[q\]之间的反转节点的距离。

综合起来，在这里就只需要找出一个最优的p，使得f\[nxt\[p\]\]\[d - 1\] + f\[nxt\[q0\]\]\[k - d - 1\] + f\[nxt\[q1\]\]\[k - d - 1\] + ... 最大，其中后面与q有关的项覆盖了now除了nxt\[p\]之外的所有孩子。

为了方便计算，在这里可以先加上一项f\[nxt\[p\]\]\[k - d - 1\]，再减去f\[nxt\[p\]\]\[k - d - 1\]。这样一来，关于k - d - 1的正项之和，即

f\[nxt\[0\]\]\[k - d - 1\] + f\[nxt\[1\]\]\[k - d - 1\] + ... f\[nxt\[-1\]\]\[k - d - 1\]

这个值与p的取值无关，剩下的则是f\[nxt\[p\]\]\[d - 1\] - f\[nxt\[p\]\]\[k - d - 1\]，因此在这里只需找出最大的f\[nxt\[p\]\]\[d - 1\] - f\[nxt\[p\]\]\[k - d - 1\]就行了。

对于以上三种情况，可以发现多次进行了全部nxt对应的f以及g的求和，因此在这里可以使用两个数组sf以及sg，其中sf[d]表示f[nxt][d]之和，sg[d]表示g[nxt][d]之和。

另外，还可以使用两个数组ma_f以及mi_g，其中ma_f\[d\]表示最大的f\[nxt\[p\]\]\[d - 1\] - f\[nxt\[p\]\]\[k - d - 1\]，而mi_g\[d\]则表示最小的g\[nxt\[p\]\]\[d - 1\] - g\[nxt\[p\]\]\[k - d - 1\]。需要注意，只有当d > 0且d + d \< k时，这两个数组才有对应的值。

到了这里，就得到了完整的处理方法：

1、首先，遍历now的所有孩子nxt，递归计算f[nxt]以及g[nxt]并进行预处理。

对于当前的nxt，从0到k遍历d，将f[nxt][d]以及g[nxt][d]累加到sf[d]以及sg[d]当中。

同时，若d > 0且d + d \< k，还需要使用f[nxt][d - 1] - f[nxt][k - d - 1]更新ma_f[d]，使用g[nxt][d - 1] - g[nxt][k - d - 1]更新mi_g[d]。

2、接下来处理f[now][0]以及g[now][0]：

f[now][0] \= -sg[k - 1] - nums[now]

g[now][0] \= -sf[k - 1] - nums[now]

3、然后从1到k遍历d，计算f[now][d]以及g[now][d]。

对于当前的d，若d + d >\= k，那么

f[now][d] \= sf[d - 1] + nums[now]

g[now][d] \= sg[d - 1] + nums[now]

否则

f[now][d] \= sf[k - d - 1] + ma_f[d] + nums[now]

g[now][d] \= sg[k - d - 1] + mi_g[d] + nums[now]

4、最后，基于f和g中，距离大于等于d时最优这一定义，还需要从k - 1到0逆序遍历，对于当前遍历到的d：

f[now][d] \= max(f[now][d], f[now][d + 1])

g[now][d] \= min(g[now][d], g[now][d + 1])

全部计算完成后，f[0][0]即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def subtreeInversionSum(self, edges, nums, k):
        """
        :type edges: List[List[int]]
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        n = len(nums)

        f = [[None] * (k + 1) for _ in range(n)]
        g = [[None] * (k + 1) for _ in range(n)]

        t = [[] for _ in range(n)]
        for x, y in edges:
            t[x].append(y)
            t[y].append(x)
        
        def dfs(now, pre, f, g):
            sf = [0] * (k + 1)
            ma_f = [None] * (k + 1)
            sg = [0] * (k + 1)
            mi_g = [None] * (k + 1)

            for nxt in t[now]:
                if nxt == pre:
                    continue
                
                dfs(nxt, now, f, g)
                
                for d in range(k + 1):
                    sf[d] += f[nxt][d]
                    sg[d] += g[nxt][d]
                    if d != 0 and d + d < k:
                        if ma_f[d] is None or f[nxt][d - 1] - f[nxt][k - d - 1] > ma_f[d]:
                            ma_f[d] = f[nxt][d - 1] - f[nxt][k - d - 1]
                        if mi_g[d] is None or g[nxt][d - 1] - g[nxt][k - d - 1] < mi_g[d]:
                            mi_g[d] = g[nxt][d - 1] - g[nxt][k - d - 1]

            for d in range(1, k + 1):
                if d + d >= k:
                    f[now][d] = sf[d - 1] + nums[now]
                    g[now][d] = sg[d - 1] + nums[now]
                else:
                    if ma_f[d] is not None:
                        f[now][d] = sf[k - d - 1] + ma_f[d] + nums[now]
                    if mi_g[d] is not None:
                        g[now][d] = sg[k - d - 1] + mi_g[d] + nums[now]

            f[now][0] = -sg[k - 1] - nums[now]
            g[now][0] = -sf[k - 1] - nums[now]

            for d in range(k - 1, -1, -1):
                if f[now][d] is None or f[now][d] < f[now][d + 1]:
                    f[now][d] = f[now][d + 1]
                if g[now][d] is None or g[now][d] > g[now][d + 1]:
                    g[now][d] = g[now][d + 1]

        dfs(0, -1, f, g)
        return f[0][0]
```
