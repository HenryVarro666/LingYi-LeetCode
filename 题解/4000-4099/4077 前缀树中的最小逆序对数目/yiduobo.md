---
title: "4077. 前缀树中的最小逆序对数目"
aliases: ["yiduobo的每日leetcode 4077.前缀树中的最小逆序对数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2093857360062238999"
zhihu_id: "2093857360062238999"
zhihu_title: "yiduobo的每日leetcode 4077.前缀树中的最小逆序对数目"
question_id: "4077"
question: "前缀树中的最小逆序对数目"
problem_url: "https://leetcode.cn/problems/minimize-inversions-in-a-prefix-tree/"
created: "2026-10-15T00:44:52+08:00"
updated: "2026-10-15T00:44:52+08:00"
upvotes: 0
comments: 0
---

# 4077. 前缀树中的最小逆序对数目

> **[yiduobo的每日leetcode 4077.前缀树中的最小逆序对数目](https://zhuanlan.zhihu.com/p/2093857360062238999) · 知乎 · 2026-10-15 · 赞同 0**
> 力扣：[4077. 前缀树中的最小逆序对数目](https://leetcode.cn/problems/minimize-inversions-in-a-prefix-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4077.前缀树中的最小逆序对数目

<https://leetcode.cn/problems/minimize-inversions-in-a-prefix-tree/description/>

题目给出一个包含n个互不相同字符串的数组words，其长度不超过10000，其中字符串的长度不超过20，且仅有a到j这10种字符组成。

另外给出一个整数数字target，其中恰好包含0到n - 1。对于一个下标index，若target[p]恰好等于index，那么words[index]这个字符串的编号就是p。

接下来，使用words中的字符串构造一颗trie树，然后在其中进行先序遍历。对于trie树中的某个节点，其可能具有多个孩子节点，在这里可以自由选择先遍历哪个孩子。在先序遍历的过程中，当首次访问到words中某个字符串的结束节点时，将这个字符串对应的编号记录下来，最终将得到一个长度为n的编号数组。

问在最优的访问顺序下，这个编号数组中的逆序对最少是多少。

由于题目中是通过先序遍历获取编号数组的，那么就意味着不同子树包含的字符串的编号必然是互相隔离开的。这样一来，就可以逐个节点递归计算，对于当前节点，只需要考虑如何排布当前节点的孩子遍历的顺序，让子树间产生的逆序对最少。

又由于本题中字符串仅有a到j组成，那么就意味着一个节点最多只有10个孩子节点，因此在这里可以使用状态压缩动态规划来进行计算。

不妨设当前节点一共有m个孩子，那么可以先将所有子树按照0到m - 1编号，令f[state]表示遍历完state中的子树形成的逆序对数量。

那么对于f\[state\]，可以先将其中包含的子树编号分离出来，得到编号数组last_candidate。若last_candidate中仅包含一颗子树，那么f\[state\]为0，否则就需要从中枚举最后遍历的子树编号last，此时就有f\[state\] \= min(f\[state ^ (1 \<\< last)\] + cost)。其中前一项表示遍历完state中除编号last子树之外的子树形成的最少逆序对数量，后者则表示将last接在这些子树后面形成的逆序对数量。如果记rev\[x\]\[y\]为将x放在y之前遍历时，子树x与子树y中逆序对的数量(方便起见，规定rev\[x\]\[x\]为0)，那么在这里的cost就是rev\[last_candidate\[0\]\]\[last\] + rev\[last_candidate\[1\]\]\[last\] + ... + rev\[last_candidate\[-1\]\]\[last\]。

到了这里，问题就变成了对于这些子树，如何高效计算两两之间的rev。

对于这个问题，可以参考归并排序的做法，在保证子树中字符串编号有序的前提下，直接两两暴力二路归并来进行计算。具体来说，就是对于两颗子树a和b，不妨设二者包含的字符串的编号数组分别为o[a]和o[b]，且这两个数组有序，那么就可以使用类似二路归并的做法，使用两个变量p和q开始向后扫。若o[a][p] \< o[b][q]，那么就说o[b][0]到o[b][q - 1]这q个编号是小于o[a][p]的，因此先遍历a将带来q组逆序对，此时应该将rev[a][b]加上q，然后将p向后移动；反之，若o[a][p] > o[b][q]，则应该将rev[b][a]加上p，然后将q向后移动。

这样做虽然看上去的复杂度较高，但是由于这些数组包含的编号总数有限，因此对于单层节点而言，暴力计算的时间复杂度实际上是O(10n)。理由是对于最坏情况，一共10颗子树，不妨设这些子树对应的编号数组的长度分别为|A|、|B|、...、|J|，那么两两计算的复杂度就是

(|A| + |B|) + (|A| + |C|) + ... + (|A| + |J|) + (|B| + |C|) + ... + (|B| + |J|) + ... + (|I| + |J|)

可以发现，其中每种长度都恰好出现了10次，而|A| + |B| + |C| + ... + |J|就是当前子树中全部字符串的数量，那么对于trie树中单层的所有节点，包含的全部字符串不超过n个，因此对于单层节点而言，两两暴力计算的时间复杂度就是O(10n)。又由于字符串的长度不超过20，因此花在计算rev的时间复杂度为O(10nL)，其中L为字符串的长度。

需要注意，由于当前节点中所有字符串的编号需要按顺序排列好供父节点使用，因此在两两计算的同时，也需要额外做一次全体的归并排序，形成有序的编号数组。

最后，还有一点就是除了考虑排布各个子树计算逆序对之外，还有一种情况就是某个字符串恰好以当前节点结束，那么对于子树中的其他字符串，无论怎样排序，其先序遍历都必然在这个恰好结束的字符串的后面，因此还需要额外计算这里形成的逆序对。

最后附上python代码：

```python
class Solution(object):
    def minInversions(self, words, target):
        """
        :type words: List[str]
        :type target: List[int]
        :rtype: int
        """

        root = [{}, []]
        order = [0] * len(target)
        for index, t in enumerate(target):
            order[t] = index

        for index, (w, t) in enumerate(zip(words, target)):
            now = root
            for c in w:
                if c not in now[0]:
                    now[0][c] = [{}, []]
                now = now[0][c]
            
            now[1].append(order[index])

        global res
        res = 0

        def dfs(now):
            if not now[0]:
                return

            for c in now[0]:
                dfs(now[0][c])
            
            chars = list(now[0].keys())
            m = len(chars)
            rev = [[0] * m for _ in range(m)]
            final = now[1][:]

            global res

            for a in range(m):
                tmp = []
                p, q = 0, 0
                o1, o2 = final, now[0][chars[a]][1]
                while p < len(o1) and q < len(o2):
                    if o1[p] < o2[q]:
                        tmp.append(o1[p])
                        p += 1
                    else:
                        tmp.append(o2[q])
                        q += 1
                
                tmp.extend(o1[p:])
                tmp.extend(o2[q:])
                final = tmp[:]

                if now[1]:
                    o1 = now[1]
                    p, q = 0, 0
                    while p < len(o1) or q < len(o2):
                        if q == len(o2) or (p < len(o1) and o1[p] < o2[q]):
                            res += q
                            p += 1
                        else:
                            q += 1

                for b in range(a + 1, m):
                    p, q = 0, 0
                    o1 = now[0][chars[a]][1]
                    o2 = now[0][chars[b]][1]
                    while p < len(o1) or q < len(o2):
                        if p == len(o1) or (q < len(o2) and o2[q] < o1[p]):
                            rev[b][a] += p
                            q += 1
                        else:
                            rev[a][b] += q
                            p += 1
            
            now[1] = final[:]

            max_state = 1 << m
            f = [None] * max_state

            for index in range(m):
                f[1 << index] = 0
            
            for state in range(1, max_state):
                if f[state] is not None:
                    continue
                
                last_candidate = []
                for index in range(m):
                    if state & (1 << index) == (1 << index):
                        last_candidate.append(index)
                
                for last in last_candidate:
                    cost = 0
                    for other in last_candidate:
                        cost += rev[other][last]
                    if f[state] is None or f[state] > f[state ^ (1 << last)] + cost:
                        f[state] = f[state ^ (1 << last)] + cost

            res += f[-1]

        dfs(root)
        return res
```
