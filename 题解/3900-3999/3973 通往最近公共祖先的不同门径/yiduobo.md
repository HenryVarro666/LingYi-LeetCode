---
title: "3973. 通往最近公共祖先的不同门径"
aliases: ["yiduobo的每日leetcode 3973.通往最近公共祖先的不同门径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2054002975769678958"
zhihu_id: "2054002975769678958"
zhihu_title: "yiduobo的每日leetcode 3973.通往最近公共祖先的不同门径"
question_id: "3973"
question: "通往最近公共祖先的不同门径"
problem_url: "https://leetcode.cn/problems/distinct-gate-paths-to-lca/"
created: "2026-06-27T01:27:57+08:00"
updated: "2026-06-27T01:27:57+08:00"
upvotes: 1
comments: 0
---

# 3973. 通往最近公共祖先的不同门径

> **[yiduobo的每日leetcode 3973.通往最近公共祖先的不同门径](https://zhuanlan.zhihu.com/p/2054002975769678958) · 知乎 · 2026-06-27 · 赞同 1**
> 力扣：[3973. 通往最近公共祖先的不同门径](https://leetcode.cn/problems/distinct-gate-paths-to-lca/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3973.通往最近公共祖先的不同门径

<https://leetcode.cn/problems/distinct-gate-paths-to-lca/description/>

题目给出一颗以节点0为根节点的无向树，共有n个节点，编号为0到n - 1。树有一个数组parent给出，其中parent[index]表示index的父节点。

每个节点都有三种类型的门，由二维数组gates给出，其中gates\[index\] \= \[red\[index\], blue\[index\], white\[index\]\]，分别表示index上红门、蓝门、白门的数量，其中：

- 红门只能使用红卡通过
- 蓝门只能使用蓝卡通过
- 白门可以使用任意颜色的卡通过，但是通过后需要翻转卡牌的颜色

alice和bob分别从给定节点出发，初始持有一张红卡或者蓝卡（1表示红卡，0表示蓝卡）。两人需要独立地沿着树向上移动，直到到达他们的最近公共祖先。

每次移动，都需要满足当前节点上至少有一个可以当前持有的卡通过的门，同一个节点上多个同色的门将被认为是不同的移动方案。

给出一个二维数组queries，其中queries\[index\] \= \[aNode\[index\], aCard\[index\], bNode\[index\], bCard\[index\]\]，分别表示alice的起始节点和卡片颜色，以及bob的其实节点和卡片颜色。问alice和bob到达最近公共祖先的不同合法移动方案数，结果对10^9 + 7取模。

所有查询计算完成后，取这些结果的按位异或作为最终答案。

首先，对于lca类的问题，常见的做法是利用dfs序，将lca转化为rmq问题，或者使用树上倍增，记录从每个节点开始向上走2^k步到达的节点。

另外，本题还需要计算合法的路径总数。对于这个问题，节点-颜色的pair是非常直观的状态表示，也就是说使用动态规划可以比较方便地求解。

结合以上两点，在这里选用树上倍增是比较合适的做法，因为anc[u][p]表示u往上走2^p到达的节点，这本身也是一种动态规划的状态表示，而对于路径方案的计算，则可以如法炮制，令f[u][p][state]表示u往上走2^p步，且其实的卡牌颜色和到达终点时的卡牌颜色的组合为state时的合法方案数。其中state是一个两位二进制数，高位表示起始的卡牌颜色，如题目描述，0表示蓝色，1表示红色。低位则表示到达终点后的卡牌颜色，同样是0表示蓝色，1表示红色。

---

接下来，对于anc[u][p]以及f[u][p][state]：

1、首先当p \= 0时，目标节点就是u的父节点parent[u]：

anc[u][p] \= parent[u]

当parent[u]不等于-1，即u不是根节点时，可以计算对应的f[u][0][state]。先分离state，得到起点和终点的卡牌颜色start和end。

若start等于end，那么只能通过u上特定颜色的门，具体对应的就是f[u][0][state] \= gates[u][1 - start]。需要特别注意，虽然题目中的0表示蓝色，1表示红色，但是gates[u]中下标0表示红色门数量，1表示蓝色门数量，所以这里是gates[u][1 - start]。

若start不等于end，那么只能通过u上的白色门，具体对应的就是f[u][0][state] \= gates[u][-1]。

2、当p > 0时，则需要先从u走2^(p - 1)步走到anc[u][p - 1]，然后再往上走2^(p - 1)到达目的地：

首先，这里显然需要满足v \= anc[u][p - 1]存在，同时anc[v][p - 1]也需要存在，否则anc[u][p]和f[u][p][state]都没有意义。

接下来，先更新anc[u][p]为anc[v][p - 1]，然后对于f[u][p][state]，同样是先分离start和end，接下来，需要计算在v这一处持有蓝色卡牌或者红色卡牌的合法路径数量，即从u -> v -> anc[v][p - 1]的路径上，卡牌颜色为start->blue->end以及start->red->end的路径数量。

于是可以得到转移方程

f[u][p][state] \= (f[u][p - 1][start \<\< 1] \* f[v][p - 1][end] % mod + f[u][p - 1][(start \<\< 1) | 1] \* f[v][p - 1][2 | end] % mod) % mod

对于前面的f[u][p - 1][start \<\< 1] \* f[v][p - 1][end]，其中

f[u][p - 1][start \<\< 1]表示的是u->v，卡牌颜色start->blue的路径数量，这个state为start \<\< 1，是start作为高位，低位为蓝色，即0作为低位的state。

f[v][p - 1][end]表示的则是v -> anc[v][p - 1]，卡牌颜色blue->end的路径数量，这个state为end，是高位为蓝色，即0作为高位，而end作为低位的state。

对于后面的f[u][p - 1][(start \<\< 1) | 1] \* f[v][p - 1][2 | end]类似，不同之处是到达v时持有红色卡牌。

---

得到anc和f之后，还需要额外计算树中每个节点的深度。

接下来对于一组查询[u, color_u, v, color_v]，可以先根据colur_u和color_v得到初始状态下的路径数量。

具体来说，令u_red、u_blue表示最终持有红色卡牌以及蓝色卡牌的合法路径数量，v_red、v_blue同理。那么就有u_red \= color_u，u_blue \= 1 - colur_u，即colur_u为0时表示蓝色卡，因此红色路径数量为0，蓝色路径数量为1，反之则红色路径数量为1，蓝色路径数量为0。

接下来，开始从u和v开始向上，一边计算lca一边计算路径数量。

首先，若u或v与另一方面不在同一深度时，应该先选择较深的节点开始往上走，直到两个节点的深度相同。每次行走的步数2^p不能太大，不能反而走得比另一方更浅。

确定了p之后，就可以更新u或v(记为x)对应的red和blue为

new_red \= red \* f[x][p][3] + blue \* f[x][p][1]

new_blue \= red \* f[x][p][2] + blue \* f[x][p][0]

含义也好理解，其中new_red是一开始持有红卡或蓝卡，从x走到anc[x][p]后持有红卡的路径数量，而new_blue则是一开始持有红卡或蓝卡，最后持有蓝卡的路径数量。

接下来，当u和v位于同一深度时，则两个节点同时往上走，直到走到二者相遇。需要注意这里2^p同样不能太大，当p > 0时不能一次性走到二者相同的节点，因为可能走过了头。

而对于red和blue的计算，则与上面完全相同。

得到最终u_red、u_blue以及v_red、v_blue之后，路径总数就是(u_red + u_blue) \* (v_red + v_blue)。需要需要u和v是独立路径，因此最后是使用乘法原理。

最后附上python代码：

```python
class Solution(object):
    def distinctPaths(self, n, parent, gates, queries):
        """
        :type n: int
        :type parent: List[int]
        :type gates: List[List[int]]
        :type queries: List[List[int]]
        :rtype: int
        """
        
        g = [[] for _ in range(n)]
        for u, p in enumerate(parent):
            if p != -1:
                g[p].append(u)
        
        q = [0]
        level = [0] * n
        head, tail = 0, 1
        while head < tail:
            for u in q[head : tail]:
                for v in g[u]:
                    level[v] = level[u] + 1
                    q.append(v)
            head, tail = tail, len(q)

        ma_p = 0
        x = 1
        while x <= level[q[-1]]:
            x += x
            ma_p += 1

        anc = [[-1] * ma_p for _ in range(n)]
        f = [[[0] * 4 for _ in range(ma_p)] for _ in range(n)]
        
        mod = 10 ** 9 + 7
        for p in range(ma_p):
            for u in range(n):
                if p == 0:
                    anc[u][p] = parent[u]
                    update = True
                    if parent[u] != -1:
                        for state in range(4):
                            start = (state >> 1) & 1
                            end = state & 1
                            if start == end:
                                f[u][0][state] = gates[u][1 - start]
                            else:
                                f[u][0][state] = gates[u][-1]
                else:
                    v = anc[u][p - 1]
                    if v != -1 and anc[v][p - 1] != -1:
                        anc[u][p] = anc[v][p - 1]
                        for state in range(4):
                            start = (state >> 1) & 1
                            end = state & 1
                            f[u][p][state] = (f[u][p - 1][start << 1] * f[v][p - 1][end] % mod + f[u][p - 1][(start << 1) | 1] * f[v][p - 1][2 | end] % mod) % mod

            p += 1

        res = 0
        mod = 10 ** 9 + 7
        for u, color_u, v, color_v in queries:
            u_red = color_u
            u_blue = 1 - color_u

            v_red = color_v
            v_blue = 1 - color_v
            
            p = ma_p - 1
            while level[u] > level[v]:
                while p > 0 and (anc[u][p] == -1 or level[anc[u][p]] < level[v]):
                    p -= 1

                nxt_u = anc[u][p]
                u_red, u_blue = (u_red * f[u][p][3] % mod + u_blue * f[u][p][1] % mod) % mod, (u_red * f[u][p][2] % mod + u_blue * f[u][p][0] % mod) % mod
                u = nxt_u
            
            p = ma_p - 1
            while level[v] > level[u]:
                while p > 0 and (anc[v][p] == -1 or level[anc[v][p]] < level[u]):
                    p -= 1
                nxt_v = anc[v][p]
                v_red, v_blue = (v_red * f[v][p][3] % mod + v_blue * f[v][p][1] % mod) % mod, (v_red * f[v][p][2] % mod + v_blue * f[v][p][0] % mod) % mod
                v = nxt_v

            p = ma_p - 1
            while u != v:
                while p > 0 and anc[u][p] == anc[v][p]:
                    p -= 1
                nxt_u = anc[u][p]
                u_red, u_blue = (u_red * f[u][p][3] % mod + u_blue * f[u][p][1] % mod) % mod, (u_red * f[u][p][2] % mod + u_blue * f[u][p][0] % mod) % mod
                u = nxt_u
                nxt_v = anc[v][p]
                v_red, v_blue = (v_red * f[v][p][3] % mod + v_blue * f[v][p][1] % mod) % mod, (v_red * f[v][p][2] % mod + v_blue * f[v][p][0] % mod) % mod
                v = nxt_v

            res ^= (u_red + u_blue) * (v_red + v_blue) % mod

        return res
```
