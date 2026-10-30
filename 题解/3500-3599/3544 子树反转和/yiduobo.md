---
title: "3544. 子树反转和"
aliases: ["yiduobo的每日leetcode 3544.子树反转和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1907587225627136865"
zhihu_id: "1907587225627136865"
zhihu_title: "yiduobo的每日leetcode 3544.子树反转和"
question_id: "3544"
question: "子树反转和"
problem_url: "https://leetcode.cn/problems/subtree-inversion-sum/"
difficulty: "Hard"
rating: 2545
created: "2025-05-20T21:52:04+08:00"
updated: "2025-05-20T21:52:04+08:00"
upvotes: 0
comments: 0
---

# 3544. 子树反转和

> **[yiduobo的每日leetcode 3544.子树反转和](https://zhuanlan.zhihu.com/p/1907587225627136865) · 知乎 · 2025-05-20 · 赞同 0**
> 力扣：[3544. 子树反转和](https://leetcode.cn/problems/subtree-inversion-sum/) · Hard · 灵茶山艾府：[树形 DP：从 O(nk) 到 O(n)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3544.子树反转和

[3544. 子树反转和 - 力扣（LeetCode）](https://leetcode.cn/problems/subtree-inversion-sum/)

题目给出一颗以节点0为根节点，包含n个节点的无向树，其中节点的编号为0到n - 1，n不超过50000。这棵树由长度为n - 1的二维数组edges表示，其中edges\[index\] \= \[u\[index\], v\[index\]\]，表示u\[index\]和v\[index\]之间存在一条边。

另外给出一个整数k以及一个长度为n的整数数组nums，其中nums[index]表示节点index的值，k的大小在1到50之间。

现在可以对树中的部分节点执行反转操作，当反转某个节点时，以该节点为根节点的子树中所有节点的值都乘以-1，另外对于某个节点，只有当其距离与其距离最近，且已经被反转过的某个祖先节点的距离大于等于k，才能翻转这个节点。更通俗的说法就是，如果翻转了当前节点，那么从该节点往下的k - 1层节点都不能反转，但是对于更下层的则可以执行翻转。

问如何执行反转操作，才能使得树中节点值之和最大。

朴素的动态规划算法是比较容易想到的，令f[now][dis][rev]表示以now为根节点，距离最近的执行过反转的祖先节点的距离为dis，且当前子树的反转状态为rev时的最大子树和。其中rev等于0表示子树没有被翻转过，等于1则表示被反转过，那么对于f[now][dis][rev]：

1、首先考虑不翻转now的情况：

这种情况下，先根据rev等于0还是1，先将nums[index]或者-nums[index]作为f[now][dis][rev]的初始值。

接下来则需要遍历now的所有孩子节点nxt，先递归计算f[nxt][dis + 1][rev]，然后将其累加到f[now][dis][rev]中。需要注意这里记录大于k的dis是没有意义的，因此在这里可以改为递归计算f[nxt][min(dis + 1, k)][rev]。

2、然后考虑翻转now的情况：

这种情况的前提是当前的dis必须等于k，否则因为与上一个反转的祖先节点距离不够，不能反转该节点。若可以反转该节点，那么：

先将nxt_rev置为rev^1，然后根据nxt_rev等于0还是1，将nums[index]或者-nums[index]作为f[now][dis][rev]的初始值。

接下来依然是遍历now的所有孩子节点nxt，先递归计算f[nxt][1][nxt_rev]，这里的1是因为当前节点被反转了，其孩子节点与该节点的距离为1，然后将其累加到f[now][dis][rev]中。

根据以上的描述，最终答案就是f[0][k][0]。这个算法的时间复杂度为O(nk)，但是由于rev这一维的存在，最终的时间复杂度还是比较微妙的，需要一些常数优化或者整体算法的优化才行。

---

注意到以上的算法中，由于dis的限制，在k较大的情况下大多数时候都不能执行翻转操作，而不执行翻转操作时子树和实际上可以在预处理的时候计算出来，从而跳过某些中间节点，这样一来就无需再记录dis。

以样例1为例，如果不选择翻转节点0，那么还是照常递归计算节点1和节点2；如果翻转节点0，由于k \= 2，那么下一层的所有节点都不能反转，而节点0，以及下一层这些节点的节点值之和，就可以通过以节点0为根节点的子树中所有节点值之和，减去以0往下两层的所有节点为根节点的子树中所有节点之和计算得到。

更进一步的，对于某个节点now，如果不选择翻转now，那么还是照常递归计算now的所有孩子节点；如果翻转节点now，那么从now的下一层开始往下的k - 1层节点都不能反转，而now与这些节点的节点值之和，则可以通过以now为根节点的子树中所有节点值之和，减去以now往下k层的所有节点为根节点的子树中所有节点之和计算得到。接下来的往下第k层的所有节点，则是照常递归计算就行了。

在这里记k_level_childs[now]为now往下k层的所有节点，那么对于f[now][rev]：

1、如果不翻转now：

此时依然是通过rev等于0还是1先使用nums[now]或者-nums[now]来初始化f[now][rev]，然后遍历now的所以孩子节点nxt，递归计算f[nxt][rev]，将其累加到f[now][rev]即可。

2、如果翻转now：

此时使用两个变量x和v分别表示now以及往下k - 1层的节点值之和，以及k层节点往下的子树中节点值之和，那么就可以先用s[now]来初始化x，v的初始值则为0。这里的s[now]指的是原始树中，以now为根节点的子树中所有节点值之和，可以在动态规划之前先通过一趟dfs计算得到。

接下来，遍历now的所有k层子孙节点k_nxt，首先将s[k_nxt]从x中减去，然后递归计算f[k_nxt][rev^1]，并将其累加到v中。

最后，若rev为0，那么在翻转后x就应该取反，然后使用x + v更新f[now][rev]即可。

这样一来，就优化掉了dis这一维，时间复杂度就优化到了O(n)，不过又引入了一个新的问题，就是如何计算k_level_childs。k_level_childs是一对多的数组，直接计算比较麻烦，不妨反过来思考，对于每个节点，先计算该节点往上k层的节点k_level_anc是什么，然后根据k_level_anc再计算k_level_childs。

对于k_level_anc的计算，则可以通过记录深度的dfs来完成。对于某个深度为depth的节点，其往上k层的祖先节点就是最近一次遍历到的深度为depth - k的节点，于是可以使用一个哈希表last记录每一层最后遍历到的节点，那么对于当前遍历到的节点now，若其深度为depth，其对应的k_level_anc[now]就是last[depth - k]，当然这里的前提条件是depth大于等于k。接下来，将last[depth]更新为now，然后继续dfs即可。

得到k_level_anc后，只需遍历所有节点，对于当前遍历到的index，若k_level_anc\[index\]存在，将index加入到k_level_childs\[k_level_anc\[index\]\]即可。

在具体实现上，由于计算s数组也需要预先进行一趟dfs，刚好可以将k_level_anc的计算也放进去一次性都算好。

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
        
        n = len(edges) + 1
        g = [[] for _ in range(n)]
        fa = [None] * n
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        k_level_anc = [None] * n
        last = {}
        s = [0] * n

        def dfs(now, pre, depth):
            v = nums[now]
            if depth >= k:
                k_level_anc[now] = last[depth - k]
            last[depth] = now
            fa[now] = pre

            for nxt in g[now]:
                if nxt != pre:
                    dfs(nxt, now, depth + 1)
                    v += s[nxt]
            s[now] = v
        
        dfs(0, None, 0)
        
        k_level_childs = [[] for _ in range(n)]
        for index in range(n):
            if k_level_anc[index] is not None:
                k_level_childs[k_level_anc[index]].append(index)
        

        f = [[None] * 2 for _ in range(n)]
        def calc(now, rev, f):
            if f[now][rev] is None:
                f[now][rev] = nums[now]
                if rev == 1:
                    f[now][rev] = -nums[now]
                
                for nxt in g[now]:
                    if nxt != fa[now]:
                        f[now][rev] += calc(nxt, rev, f)
                

                x = s[now]
                v = 0
                for k_nxt in k_level_childs[now]:
                    x -= s[k_nxt]
                    v += calc(k_nxt, rev ^ 1, f)
                
                if rev == 0:
                    x = -x
                
                f[now][rev] = max(f[now][rev], x + v)
            
            return f[now][rev]
        
        return calc(0, 0, f)
```
