---
title: "3841. 查询树上回文路径"
aliases: ["yiduobo的每日leetcode 3841.查询树上回文路径"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/depth-first-search", "leetcode/binary-indexed-tree", "题单/常用数据结构", "题单/链表-二叉树与回溯", "题单/常用数据结构/八-树状数组和线段树", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2010135331828176582"
zhihu_id: "2010135331828176582"
zhihu_title: "yiduobo的每日leetcode 3841.查询树上回文路径"
question_id: "3841"
question: "查询树上回文路径"
problem_url: "https://leetcode.cn/problems/palindromic-path-queries-in-a-tree/"
difficulty: "Hard"
rating: 2384
created: "2026-02-28T03:01:13+08:00"
updated: "2026-02-28T03:01:14+08:00"
upvotes: 1
comments: 0
---

# 3841. 查询树上回文路径

> **[yiduobo的每日leetcode 3841.查询树上回文路径](https://zhuanlan.zhihu.com/p/2010135331828176582) · 知乎 · 2026-02-28 · 赞同 1**
> 力扣：[3841. 查询树上回文路径](https://leetcode.cn/problems/palindromic-path-queries-in-a-tree/) · Hard · 灵茶山艾府：[LCA + 差分树状数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3841.查询树上回文路径

<https://leetcode.cn/problems/palindromic-path-queries-in-a-tree/description/>

题目给出一个棵包含n个节点的无向树，编号为0到n - 1。树由一个长度为n - 1的二维数组edges表示，其中edges\[index\] \= \[u\[index\], v\[index\]\]，表示u\[index\]和v\[index\]之间存在一条无向边。

另外给出一个长度为n的小写英文字母组成的字符串s，其中s[index]表示分配给index的字符。

最后给出一个字符串数组queries，其中queries[index]属于以下两种形式之一：

- "update u c"，表示将节点u处的字符修改为c
- "query u v"，表示判断u到v的唯一路径上的字符形成的字符串，能否通过重新排列得到一个回文串

题目的成分还挺复杂的，接下来一步一步拆解来得到最后的做法。

---

首先，查询的是u到v的路径上的字符形成的字符串，能否通过重新排列得到回文串。

对于重新排列形成回文串的问题，可以理解成路径上的字符形成的字符串中，出现次数为奇数的字符数量不超过1个。理由是回文串中非中心的字符都是成对出现的，而中心字符最多只能有一个，因此出现次数为奇数的字符数量不能超过1个。

更进一步的，由于题目中的字符都是小写字符，因此在这里可以将路径中每种字符的奇偶性转化为一个26位的二进制数，其中第0位上为0表示'a'出现了偶数次，为1则表示'a'出现了奇数次，第1位则对应'b'出现次数的奇偶性，以此类推，直到第25位表示'z'出现次数的奇偶性。

那么对于u到v路径上字符串对应的二进制数，只有当其中所有数位中没有1，或者仅有1个1时，才能通过重新排列这个字符串得到回文串，也就是说这个二进制数只能为0，或者恰好为2的幂。另一方面，在路径上新增或者去除掉某个字符时，只需将这个字符对应的二进制值异或到字符串对应的二进制数中即可。

---

接下来，需要想办法高效计算u到v的路径对应的二进制串。

对于u到v的路径，需要先找到u和v的最近公共祖先lca，那么这条路径就可以拆分为u到lca的异或值，异或上v到lca的异或值，再异或上lca处的字符对应的二进制值。这里需要额外异或lca处的字符是因为u到lca与v到lca这两条路径计算了lca两次。

更进一步的，从u到lca的异或值，可以认为是从u到根节点的异或值，异或上lca的父节点到根节点的异或值，v到lca的异或值同理。由于最后需要将这两段异或起来，而lca的父节点到根节点的异或值被异或了两次可以消去，因此这个计算过程可以认为是u到根节点的异或值，异或上v到根节点的异或值，再异或上lca处的字符对应的二进制值。方便起见，在这里记xor[u]为u上的字符对应的二进制数，pre_xor[u]为根节点到u的路径上每个节点对应字符的二进制值的异或结果。

---

如果不考虑修改操作，就只需一趟dfs或者bfs，对于每个节点u都计算出pre_xor[u]。而对于lca，处理方法多种多样，随便取一种就行了。现在有了修改操作，则还需要进行一些额外操作。

由于最终计算是通过pre_xor实现的，而对于修改节点u的操作，这次修改将会影响到以u为根节点的子树中每个节点对应的pre_xor，因此此时的问题就转化成了如何高效的批量修改这些pre_xor。

对于这个问题，可以借助dfs序实现，理由是以u为根节点的子树中的所有节点，在dfs序中恰好是连续的一段，也就是说此时的修改变成了对于一个连续区间的修改。而对于这类区间修改，单点求值的问题，就可以通过线段树进行求解。

具体来说，在执行dfs时，若某个节点是首次访问，那么就将其加入到树的dfs序order的末尾，dfs结束后就自然得到了dfs序order。除此之外，还需要计算额外计算两个数组pos以及covered，其中pos[u]表示u在order中的位置，也就是在将u加入到order这一时刻，order的长度减1；而covered[u]则表示以u为根节点的子树中节点的数目，也就是递归计算完u的所有孩子节点后的这一时刻，order的长度减去pos[u]再加上1。

得到pos和covered之后，以u为根节点的子树中的所有节点，恰好就是order中pos[u]到pos[u] + covered[u] - 1这一段。

当节点u被修改时，需要先消除u原先节点值的影响，然后添加u新的节点值的影响，也就是说将pos[u]到pos[u] + covered[u] - 1这一段异或上u原先节点值对应的二进制数以及u新的节点值对应的二进制数。

由于这里的线段树是单点求解，因此区间的修改也不需要下防，只需在单点求解时层层异或区间的修改就行了。

---

最后，既然需要计算dfs序，那么还可以顺便通过dfs序来计算lca。具体来说，对于一组节点u和v，若u和v相同，那么lca就是u自身；若二者不同，那么不妨设pos[u] \< pos[v]，u和v的lca就是order中从pos[u] + 1到pos[v]这一段中深度最小的节点的父亲节点。在这里需要用到节点的深度以及父亲节点，因此在dfs的过程中还需要顺便计算这两个数组level和fa，其中level[u]表示u的深度，fa[u]表示u的父亲节点编号。

这同样是一个区间最值问题，不过是静态的，因此在这里可以st算法求解。

---

到了这里，就得到了完整的处理方法。

首先通过edges建树，并初始化各个辅助数组，包括order、pos、covered、xor、pre_xor、level、fa。其中xor[index]需要初始化为s[index]对应的二进制数。

接下来从0号节点开始向下进行dfs，计算这些辅助数组。

对于线段树，则可以先初始化为全0，因为线段树中记录的是修改的值，初始状态下没有任何修改。

对于st数组，令st\[index\]\[p\]表示order中从index开始，长度为2^p这一段中深度最小的节点编号。当p \= 0时，st\[index\]\[0\]就是order\[index\]，否则就需要对比level\[st\[index\]\[p - 1\]\]以及level\[st\[index + 2^p - 1\]\[p - 1\]\]，取level较小的那一个对应的st值作为st\[index\]\[p\]。

最后，遍历所有查询。

对于修改操作(u, c)，先计算c对应的二进制数v，然后通过v异或上xor[u]得到delta，接下来通过线段树修改pos[u]到pos[u] + covered[u] - 1这一段，将delta异或上去，最后将xor[u]更新为v即可。

对于查询操作(u, v)，若u和v相同，那么答案必然为true。若u和v不同，那么先计算二者的lca，然后通过线段树查询pos[u]和pos[v]的修改值，将二者异或后，再异或上pre_xor[u]、pre_xor[v]以及xor[lca]，就得到了u到v的路径对应的二进制数。若x为0，或者x & (x - 1)为0，也就是x恰好为2的幂，那么答案就为true，否则为false。

最后附上python代码：

```python
class Solution(object):
    def palindromePath(self, n, edges, s, queries):
        """
        :type n: int
        :type edges: List[List[int]]
        :type s: str
        :type queries: List[str]
        :rtype: List[bool]
        """
        
        def dfs(now, pre, fa, level, order, pos, covered, pre_xor):
            if pre == -1:
                level[now] = 0
                pre_xor[now] = xor[now]
            else:
                level[now] = level[pre] + 1
                fa[now] = pre
                pre_xor[now] = pre_xor[pre] ^ xor[now]

            order.append(now)
            pos[now] = len(order) - 1

            for nxt in g[now]:
                if nxt == pre:
                    continue
                dfs(nxt, now, fa, level, order, pos, covered, pre_xor)
            
            covered[now] = len(order) - pos[now]
        
        def update(p, left, right, start, end, delta, f):
            if left == start and right == end:
                f[p] ^= delta
                return

            mid = (left + right) // 2
            if end <= mid:
                update(p + p + 1, left, mid, start, end, delta, f)
            elif start >= mid + 1:
                update(p + p + 2, mid + 1, right, start, end, delta, f)
            else:
                update(p + p + 1, left, mid, start, mid, delta, f)
                update(p + p + 2, mid + 1, right, mid + 1, end, delta, f)

        def get(p, left, right, x):
            if left == right:
                return f[p]
            
            mid = (left + right) // 2
            if x <= mid:
                return f[p] ^ get(p + p + 1, left, mid, x)
            else:
                return f[p] ^ get(p + p + 2, mid + 1, right, x)

        def get_lca(u, v):
            if pos[u] > pos[v]:
                u, v = v, u
            
            left = pos[u] + 1
            right = pos[v]

            p = L
            mi = None
            while left <= right:
                while p > 0 and left + (1 << p) - 1 > right:
                    p -= 1
                if mi is None or level[mi] > level[st[left][p]]:
                    mi = st[left][p]
                left += (1 << p)
            
            return fa[mi]
                
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)
        
        fa = [-1] * n
        level = [0] * n
        covered = [0] * n
        pos = [0] * n
        order = []
        pre_xor = [0] * n
        xor = [1 << (ord(c) - 97) for c in s]

        dfs(0, -1, fa, level, order, pos, covered, pre_xor)
        
        f = [0] * (n * 4)

        L = 1
        while (1 << L) <= n:
            L += 1
        
        st = [[None] * L for _ in range(n)]
        for p in range(L):
            for index in range(n):
                if p == 0:
                    st[index][p] = order[index]
                elif index + (1 << p) - 1 < n:
                    if level[st[index][p - 1]] < level[st[index + (1 << (p - 1))][p - 1]]:
                        st[index][p] = st[index][p - 1]
                    else:
                        st[index][p] = st[index + (1 << (p - 1))][p - 1]

        res = []
        for q in queries:
            if q[0] == 'u':
                u, c = q.split()[1:]
                u = int(u)
                v = 1 << (ord(c) - 97)
                delta = v ^ xor[u]
                update(0, 0, n - 1, pos[u], pos[u] + covered[u] - 1, delta, f)
                xor[u] = v
            else:
                u, v = q.split()[1:]
                u = int(u)
                v = int(v)
                if u == v:
                    res.append(True)
                else:
                    lca = get_lca(u, v)
                    x = get(0, 0, n - 1, pos[u]) ^ get(0, 0, n - 1, pos[v]) ^ pre_xor[u] ^ pre_xor[v] ^ xor[lca]
                    if x == 0 or (x & (x - 1)) == 0:
                        res.append(True)
                    else:
                        res.append(False)
        
        return res
```
