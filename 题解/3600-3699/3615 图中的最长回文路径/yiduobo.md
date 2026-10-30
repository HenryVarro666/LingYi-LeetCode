---
title: "3615. 图中的最长回文路径"
aliases: ["yiduobo的每日leetcode 3615.图中的最长回文路径"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/memoization", "leetcode/string", "leetcode/dynamic-programming", "题单/动态规划", "题单/字符串", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/字符串/三-Manacher-算法-回文串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1943836312571457751"
zhihu_id: "1943836312571457751"
zhihu_title: "yiduobo的每日leetcode 3615.图中的最长回文路径"
question_id: "3615"
question: "图中的最长回文路径"
problem_url: "https://leetcode.cn/problems/longest-palindromic-path-in-graph/"
difficulty: "Hard"
rating: 2463
created: "2025-08-27T01:01:49+08:00"
updated: "2025-08-27T01:01:49+08:00"
upvotes: 2
comments: 0
---

# 3615. 图中的最长回文路径

> **[yiduobo的每日leetcode 3615.图中的最长回文路径](https://zhuanlan.zhihu.com/p/1943836312571457751) · 知乎 · 2025-08-27 · 赞同 2**
> 力扣：[3615. 图中的最长回文路径](https://leetcode.cn/problems/longest-palindromic-path-in-graph/) · Hard · 灵茶山艾府：[中心扩展法 + 状压 DP + 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3615.图中的最长回文路径

<https://leetcode.cn/problems/longest-palindromic-path-in-graph/description/>

题目给出一个整数n以及一个包含n个节点的无向图，节点编号从0到n - 1，n的大小不超过14。另外给出一个二维数组edges，其中edges\[index\] \= \[u\[index\], v\[index\]\]，表示在节点u\[index\]到v\[index\]之间有一条边。

同时还给出一个长度为n的字符串label，其中label[index]表示的是与节点index关联的字符。

现在可以从任意节点开始，移动到任意相邻的节点，每个节点最多只能访问一次。要求找出其中的一条访问路径，路径中不包含重复节点，且路径上的节点关联字符构成回文串，问最长可以构成的回文串长度是多少。

首先对于n这个数据规模，第一时间想到的就是搜索回溯或者状态压缩动态规划。

传统的搜索回溯不能使用，因为是阶乘复杂度的，但是可以考虑暴力枚举节点的组合，这个的复杂度是2^n，然后判断这些节点能否构成回文串。比较直观的想法是利用割边确定哪些边必须选，然后再看情况选择其他边构成路径，通过节点的度来保证形成的路径合法，但是这样一来节点的顺序不好确定，最后有退化到常规的搜索回溯上去了，因此在这里还是要考虑使用状态压缩动态规划。

为了保持回文的性质，在这里需要记录下路径的头尾是哪两个节点，因此状态设计应该是f[state][left][right]表示选择state中的节点，且形成的路径中两个端点分别是left和right时构成的回文串长度。其中left是编号较小的节点，right是编号较大的节点，这样做的理由是可以省去一半不必要的重复状态。

对于f的初始化，可以以任意字符为回文中心展开，也就是对于任意节点v，都有f[1 \<\< v][v][v]为1，表示v这个节点可以形成长度为1的回文串；另一方面，也需要找到所有两个字符构成的回文中心，那么在这里就需要遍历所有的相邻点对left和right，若label[left]和label[right]相同，就有f[(1 \<\< left) | (1 \<\< right)][left][right]为2。需要注意在这里要保证left是较小的那个节点。

由于是在图中扩展路径，因此在初始化完成后，可以将所有为true的初始状态加入到队列中，然后通过bfs来进行状态转移。对于当前的f[state][left][right]，分别枚举left和right的相邻节点new_left和new_right，若：

1、这两个节点不同

2、都没有在state中出现过

3、label[new_left]与label[new_right]相同

4、新的状态f[state | (1 \<\< new_left) | (1 \<\< new_right)][new_left][new_right]没有被访问过

那么就可以将f[state | (1 \<\< new_left) | (1 \<\< new_right)][new_left][new_right]置为f[state][left][right] + 2，表示在两端分别添加了new_left和new_right这两个节点，然后将这个状态表示的三元组加入到bfs的队列中。当然，在这里依然需要保证new_left是较小的那个节点。

计算完成后，f中的最大值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxLen(self, n, edges, label):
        """
        :type n: int
        :type edges: List[List[int]]
        :type label: str
        :rtype: int
        """
        
        g = [set() for _ in range(n)]
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        max_state = 1 << n
        f = [[[None] * n for _ in range(n)] for _ in range(max_state)]
        
        q = []
        res = 0
        for left in range(n):
            q.append((1 << left, left, left))
            f[1 << left][left][left] = 1
            for right in range(left + 1, n):
                if label[left] == label[right] and left in g[right]:
                    q.append(((1 << left) | (1 << right), left, right))
                    f[(1 << left) | (1 << right)][left][right] = 2

        head, tail = 0, len(q)
        while head < tail:
            for state, left, right in q[head : tail]:
                res = max(res, f[state][left][right])
                for new_left in g[left]:
                    if state & (1 << new_left) == 1 << new_left:
                        continue
                    for new_right in g[right]:
                        if new_left == new_right:
                            continue
                        if state & (1 << new_right) == 1 << new_right:
                            continue
                        if label[new_left] != label[new_right]:
                            continue
                        
                        new_state = state | (1 << new_left) | (1 << new_right)
                        ma, mi = new_left, new_right
                        if ma < mi:
                            ma, mi = mi, ma
                        if f[new_state][mi][ma] is None:
                            f[new_state][mi][ma] = f[state][left][right] + 2
                            q.append((new_state, mi, ma))
        
            head, tail = tail, len(q)

        return res
```
