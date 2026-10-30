---
title: "2977. 转换字符串的最小成本II"
aliases: ["yiduobo的每日leetcode 2977.转换字符串的最小成本II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/trie", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/shortest-path", "题单/常用数据结构", "题单/动态规划", "题单/图论算法", "题单/常用数据结构/六-字典树-trie", "题单/动态规划/五-划分型-DP", "题单/动态规划/十一-优化-DP", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/692230360"
zhihu_id: "692230360"
zhihu_title: "yiduobo的每日leetcode 2977.转换字符串的最小成本II"
question_id: "2977"
question: "转换字符串的最小成本 II"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-convert-string-ii/"
difficulty: "Hard"
rating: 2696
created: "2024-04-13T03:13:36+08:00"
updated: "2024-04-13T03:13:36+08:00"
upvotes: 1
comments: 0
---

# 2977. 转换字符串的最小成本II

> **[yiduobo的每日leetcode 2977.转换字符串的最小成本II](https://zhuanlan.zhihu.com/p/692230360) · 知乎 · 2024-04-13 · 赞同 1**
> 力扣：[2977. 转换字符串的最小成本 II](https://leetcode.cn/problems/minimum-cost-to-convert-string-ii/) · Hard · 灵茶山艾府：[字典树+Floyd+记忆化搜索/递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2977.转换字符串的最小成本

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-cost-to-convert-string-ii/)

与上一题类似，如果将本题中的子串视为图中的节点，依然可以使用floyd算法计算将一个子串变换成另一个子串的最小代价。

另一方面，由于题目要求变换过的子串只能视为一个整体来看待，因此在这里就需要使用动态规划来计算转换的代价。令f[i]表示前i个字符匹配上的最小代价，那么对于f[i]，就可以枚举最后这个子串的起点j，那么就有f[i] \= min(f[i], f[j - 1] + cost(trans(j, i)))，其中cost部分表示将source的j到i这一段变换成target的j到i这一段所需的最小代价。

由于涉及到了字符串的检索，在这里还需要建立一颗逆向的trie树来保存可变换的词。除了trie树，也可以手动设计一个类似rk算法的窗口哈希函数来计算这个子串的哈希值。这两种做法可以边往前枚举状态边检索字符串，因此最终的时间复杂度为O(n^2)。

但是如果直接使用哈希表的话，由于计算字符串哈希的复杂度与字符串的长度有关，那么在最坏情况下复杂度可以来到O(n^3)。我在这里偷懒，还是使用的哈希表，不过修改了一下枚举的内容。我在这里枚举的是所有可变换子串的长度，然后检测source和target末尾对应长度的子串是否出现在哈希表中。由于可变换子串的长度取值范围小于等于100，因此在最坏情况下复杂度相比之前降低了一个量级，可以勉强通过本题了。

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, source, target, original, changed, cost):
        """
        :type source: str
        :type target: str
        :type original: List[str]
        :type changed: List[str]
        :type cost: List[int]
        :rtype: int
        """

        mapping = {}
        length_set = set()
        tot = 0
        for s in original:
            if s not in mapping:
                mapping[s] = tot
                tot += 1
            length_set.add(len(s))

        for s in changed:
            if s not in mapping:
                mapping[s] = tot
                tot += 1
            length_set.add(len(s))
        
        dis = [[-1] * tot for _ in range(tot)]
        m = len(original)
        for index in range(m):
            x = mapping[original[index]]
            y = mapping[changed[index]]
            if dis[x][y] == -1 or dis[x][y] > cost[index]:
                dis[x][y] = cost[index]
        
        for k in range(tot):
            for i in range(tot):
                for j in range(tot):
                    if dis[i][k] != -1 and dis[k][j] != -1 and (dis[i][j] == -1 or dis[i][j] > dis[i][k] + dis[k][j]):
                        dis[i][j] = dis[i][k] + dis[k][j]
        
        f = [0]
        n = len(source)
        for index in range(n):
            if source[index] == target[index]:
                f.append(f[-1])
            else:
                f.append(-1)
            
            for length in length_set:
                if length > index + 1:
                    continue
                
                x = mapping.get(source[index - length + 1 : index + 1], -1)
                if x == -1:
                    continue
                y = mapping.get(target[index - length + 1 : index + 1], -1)
                if y == -1:
                    continue

                if dis[x][y] != -1 and f[index - length + 1] != -1 and (f[-1] == -1 or f[-1] > f[index - length + 1] + dis[x][y]):
                    f[-1] = f[index - length + 1] + dis[x][y]

        return f[-1]
```
