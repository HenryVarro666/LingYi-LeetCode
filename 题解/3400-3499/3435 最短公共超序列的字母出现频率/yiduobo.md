---
title: "3435. 最短公共超序列的字母出现频率"
aliases: ["yiduobo的每日leetcode 3435.最短公共超序列的字母出现频率"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/bit-manipulation", "leetcode/depth-first-search", "leetcode/graph", "leetcode/enumeration", "题单/图论算法", "题单/图论算法/九-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1889053097470440778"
zhihu_id: "1889053097470440778"
zhihu_title: "yiduobo的每日leetcode 3435.最短公共超序列的字母出现频率"
question_id: "3435"
question: "最短公共超序列的字母出现频率"
problem_url: "https://leetcode.cn/problems/frequencies-of-shortest-supersequences/"
difficulty: "Hard"
rating: 3028
created: "2025-03-28T22:02:20+08:00"
updated: "2025-03-28T23:37:50+08:00"
upvotes: 1
comments: 0
---

# 3435. 最短公共超序列的字母出现频率

> **[yiduobo的每日leetcode 3435.最短公共超序列的字母出现频率](https://zhuanlan.zhihu.com/p/1889053097470440778) · 知乎 · 2025-03-28 · 赞同 1**
> 力扣：[3435. 最短公共超序列的字母出现频率](https://leetcode.cn/problems/frequencies-of-shortest-supersequences/) · Hard · 灵茶山艾府：[贪心构造 + 枚举子集 + 有向图判环 + 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3435.最短公共超序列的字母出现频率

[3435. 最短公共超序列的字母出现频率 - 力扣（LeetCode）](https://leetcode.cn/problems/frequencies-of-shortest-supersequences/description/)

题目给出一个字符串数组words，words的长度在1到256之间，同时其中所有的字符串都是由不超过16个互不相同的小写英文字母组成的，长度为2的字符串。words中的字符串互不相同。

现在要求找出words所有最短公共超序列，且确保它们互相之间无法通过排列得到。最短公共超序列指的是一个字符串，words中所有字符串都是它的子序列，其它的长度最短。

返回一个二维整数数组freqs，表示所有的最短公共超序列，其中freqs[i]是一个长度为26的数组，它依次表示一个最短公共超序列的所有小写英文字母的出现频率。

首先可以将words中出现的所有字符都收集起来，这些字符将构成最短的超序列。可以明确的是，对于这些字符，在最短超序列中最少出现一次，多只也会出现两次。最少出现一次很好理解，因为需要覆盖住words中的所有字符串，而最多出现两次则可以通过words中字符串的长度分析得到。

若某个字符x在最短超序列中出现了不止两次，那么对于某个中间的x，其可能构成xx、\_x、x\_这三种字符串。对于xx，可以用第一个和最后一个x构成；对于\_x，可以用最后一个x替换当前的x；对于x\_，则可以用第一个x替换当前的x。也就是说，当前这个中间的x是没有存在的必要的。

有了上面的结论，接下来的问题就是判断最短超序列中每种字符到底出现了一次还是两次。由于题目保证words中的字符串是通过不超过16个互不相同的小写字符构成的，因此在这里可以暴力枚举每种字符出现了一次还是两次，一共只有2^16种可能的情况，在时间复杂度方面是完全没有问题的。

对于当前枚举的状态state，可以先将其中出现次数为两次的字符填充到最短超序列的两端，那么words中与这些字符相关的字符串必然可以满足，就不需要考虑了。接下来只需要考察出现次数为一次的这些字符能否构成words中剩下的字符串。可以发现，如果将每个字符视为图中的点，每个words[i]中字符串的前后顺序视为图中的边，那么问题就变成了检测图中是否存在环，而对于检测有向图中是否有环这个问题，只需做一次拓扑排序就可以了。

另外在具体实现时，不需要每次都建图，而是只需要先对于words建图一次，然后对于每种state，在执行拓扑排序时，除了常规的入度为0的节点加入到初始队列之外，额外将state中出现两次的字符对应的节点加入到初始队列就行了。

最后附上python代码：

```python
class Solution(object):
    def supersequences(self, words):
        """
        :type words: List[str]
        :rtype: List[List[int]]
        """
        
        char2index = {}
        index2char = {}
        n = 0
        for w in words:
            if w[0] not in char2index:
                char2index[w[0]] = n
                index2char[n] = w[0]
                n += 1
            if w[1] not in char2index:
                char2index[w[1]] = n
                index2char[n] = w[1]
                n += 1

        g = [set() for x in range(n)]
        ind = [0] * n
        for w in words:
            x = char2index[w[0]]
            y = char2index[w[1]]
            g[x].add(y)
            ind[y] += 1

        best = None
        res_state = set()
        for state in range(1 << n):
            cnt = [1] * n
            tot = n
            for index in range(n):
                if (state & (1 << index)) == (1 << index):
                    cnt[index] += 1
                    tot += 1

            if best is not None and tot > best:
                continue

            part_ind = ind[:]
            q = []
            head = 0
            tail = 0
            for index in range(n):
                if cnt[index] == 2 or part_ind[index] == 0:
                    q.append(index)
                    tail += 1

            while head < tail:
                x = q[head]
                head += 1
                for y in g[x]:
                    if cnt[y] == 2:
                        continue
                    part_ind[y] -= 1
                    if part_ind[y] == 0:
                        q.append(y)
                        tail += 1

            if len(q) == n:
                if best is None or tot < best:
                    best = tot
                    res_state = set([state])
                else:
                    res_state.add(state)
        
        res = []
        for state in res_state:
            cnt = [0] * 26
            for index in range(n):
                if (state & (1 << index)) == (1 << index):
                    cnt[ord(index2char[index]) - 97] = 2
                else:
                    cnt[ord(index2char[index]) - 97] = 1
            res.append(cnt[:])
        
        return res
```
