---
title: "3241. 标记所有节点需要的时间"
aliases: ["yiduobo的每日leetcode 3241.标记所有节点需要的时间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/721004825"
zhihu_id: "721004825"
zhihu_title: "yiduobo的每日leetcode 3241.标记所有节点需要的时间"
question_id: "3241"
question: "标记所有节点需要的时间"
problem_url: "https://leetcode.cn/problems/time-taken-to-mark-all-nodes/"
difficulty: "Hard"
rating: 2522
created: "2024-09-20T00:23:00+08:00"
updated: "2024-09-20T00:23:00+08:00"
upvotes: 2
comments: 1
---

# 3241. 标记所有节点需要的时间

> **[yiduobo的每日leetcode 3241.标记所有节点需要的时间](https://zhuanlan.zhihu.com/p/721004825) · 知乎 · 2024-09-20 · 赞同 2**
> 力扣：[3241. 标记所有节点需要的时间](https://leetcode.cn/problems/time-taken-to-mark-all-nodes/) · Hard · 灵茶山艾府：[【模板】第二类换根 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3241.标记所有节点需要的时间

[. - 力扣（LeetCode）](https://leetcode.cn/problems/time-taken-to-mark-all-nodes/description/)

题目给出一个节点编号在0到n - 1之间的无向树，一开始树中所有节点都是未标记的。

对于树中的某个节点i：

1、若i为奇数，且i的某个相邻节点在时刻x - 1被标记了，那么i将在时刻x被标记

2、若i为偶数，且i的某个相邻节点在时刻x - 2被标记了，那么i将在时刻x被标记

现在要求计算对于树中的每个节点而言，如果在时刻0标记了该节点，那么标记整棵树的最短时间是多少。

题目要求计算以每个节点开始的最短标记时间，直接计算是比较困难的，不妨先考虑如果在时刻0标记单个节点，标记整棵树的最短时间是多少。

方便起见，假设0是整棵树的根节点，那么树的父子形态就能唯一确定。接下来在时刻0标记的就是0号结点，令f[i]表示在时刻0标记了节点i的话，标记以i为根节点的子树中的所有节点所需的最短时间。

那么对于f[i]，就可以枚举i的所有孩子节点j，当j为奇数时，就有f[i] \= max(f[i], f[j] + 1)，反之就有f[i] \= max(f[i], f[j] + 2)。更一般的，可以写成f[i] \= max(f[i], f[j] + 2 - j % 2)。

以上算法的时间复杂度为O(n)，如果对每个节点逐个执行该算法的话，总的时间复杂度就是O(n^2)，显然是不行的，必须想办法进行优化。

注意到上面求解从0开始标记时的f数组，对于i的某个孩子j，现在已知的是从j开始标记，标记完以j为根节点的子树中所有节点需要的最短时间为f[j]，那么如果在时刻0标记的是j，除了原始的f[j]之外，还有一种可能是往上标记j的父亲节点i，然后从i开始向最远的地方进行标记，也就是f[i]。

但是这里有一点需要注意的是，如果f[i]本来就是通过f[j]得到的，那么在j变为初始节点后，f[i]就不对了，此时应该选择的是从i开始且没有经过j对应的f值。更具体的，对于节点i，先遍历i的所有孩子节点j，计算标记所需的时间，也就是f[j] + 2 - j % 2，记录其中的最大值first以及次大值second。接下来再次遍历i的所有孩子节点j，若此时的f[j] + 2 - j % 2等于first，那么就需要先将f[i]置为second，然后递归求解从j开始进行标记所需的最短时间，最后再将f[i]重新置为first。

需要特别注意的是，这里必须边做边算，不能一开始计算first和second，因为一开始计算的f值只包含向下标记的时间，但是first和second应该也包含经过父节点向上标记所需的时间。

最后附上python代码：

```python
class Solution(object):
    def timeTaken(self, edges):
        """
        :type edges: List[List[int]]
        :rtype: List[int]
        """

        n = len(edges) + 1

        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        f = [0] * n

        def dfs(now, fa):
            for nxt in g[now]:
                if nxt == fa:
                    continue
                dfs(nxt, now)
                f[now] = max(f[now], f[nxt] + 2 - nxt % 2)

        dfs(0, -1)
        
        res = [0] * n

        def calc(now, fa):
            first = second = 0
            for nxt in g[now]:
                cost = f[nxt] + 2 - nxt % 2
                if cost > first:
                    first, second = cost, first
                elif cost > second:
                    second = cost

            res[now] = first
            f[now] = first

            for nxt in g[now]:
                if nxt == fa:
                    continue
                cost = f[nxt] + 2 - nxt % 2
                if cost == first:
                    f[now] = second
                    calc(nxt, now)
                    f[now] = first
                else:
                    calc(nxt, now)

        calc(0, -1)
        return res
```
