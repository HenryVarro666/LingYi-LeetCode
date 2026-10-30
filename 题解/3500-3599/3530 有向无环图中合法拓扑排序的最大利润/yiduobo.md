---
title: "3530. 有向无环图中合法拓扑排序的最大利润"
aliases: ["yiduobo的每日leetcode 3530.有向无环图中合法拓扑排序的最大利润"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/sorting", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1904707469013386841"
zhihu_id: "1904707469013386841"
zhihu_title: "yiduobo的每日leetcode 3530.有向无环图中合法拓扑排序的最大利润"
question_id: "3530"
question: "有向无环图中合法拓扑排序的最大利润"
problem_url: "https://leetcode.cn/problems/maximum-profit-from-valid-topological-order-in-dag/"
difficulty: "Hard"
rating: 2353
created: "2025-05-13T23:00:54+08:00"
updated: "2025-05-13T23:00:54+08:00"
upvotes: 1
comments: 0
---

# 3530. 有向无环图中合法拓扑排序的最大利润

> **[yiduobo的每日leetcode 3530.有向无环图中合法拓扑排序的最大利润](https://zhuanlan.zhihu.com/p/1904707469013386841) · 知乎 · 2025-05-13 · 赞同 1**
> 力扣：[3530. 有向无环图中合法拓扑排序的最大利润](https://leetcode.cn/problems/maximum-profit-from-valid-topological-order-in-dag/) · Hard · 灵茶山艾府：[排列型状压 DP：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3530.有向无环图中合法拓扑排序的最大利润

[3530. 有向无环图中合法拓扑排序的最大利润 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-profit-from-valid-topological-order-in-dag/description/)

题目给出一个由n个节点构成的有向无环图，节点编号为0到n - 1，其中n的大小不超过22。另外给出一个二维数组edges，其中edges\[index\] \= \[u\[index\], v\[index\]\]，表示有一条从u\[index\]指向v\[index\]的有向边。图中的每个节点都有一个对应的得分，由数组score给出，其中score\[index\]表示节点index的得分。

现在要求给出一个有效的拓扑排序来处理图中的节点，将这些节点乘以其在拓扑序中的下标（下标从1开始计算），然后求和，就是这个拓扑序的利润。问所有合法拓扑序中的最大利润为多少。

对于这类多路的调度问题，没有什么特别好的处理方法，不过本题的数据规模不算太大，可以使用状态压缩动态规划来处理。

令f[now]表示已经处理了状态为now的节点时，处理剩余节点可以得到的最大利润，那么对于f[now]，可以先分离出now的二进制表示中1的数量cnt，也就是已经处理了cnt个任务。接下来遍历所有的任务，对于第index个任务，若now & (1 \<\< index)为0，说明index这个任务还未执行，接下来需要判断index这个任务是否可以执行。

对于这个判断，则可以在一开始先对每个节点进行预处理，使用一个数组depend记录每个节点所有直接前置节点状态表示。对于一条从x指向y的边，需要将(1 \<\< x)加入到depend[y]中。

有了depend，就可以通过now & depend[index]是否等于depend[index]来判断index是否可以执行，若可以，那么就有f[now] \= max(f[now], f[now | (1 \<\< index)] + score[index] \* (cnt + 1))，其中score[index] \* (cnt + 1)为本轮选择执行index这个任务的得分。

以上算法的时间复杂度为O(2^n \* n)，对于n \= 22这个规模还是比较微妙的，可以适当加一些优化。我在这里选择加了一个贪心优化：如果某一轮可以选择执行剩下的任意任务，也就是剩下的任务都没有前置的依赖，那么就应该按照得分从小到大的顺序执行，这样就可以分数大的任务留到后面乘以更大的系数。

最后附上python代码：

```python
class Solution(object):
    def maxProfit(self, n, edges, score):
        """
        :type n: int
        :type edges: List[List[int]]
        :type score: List[int]
        :rtype: int
        """
        
        f = {}
        n = len(score)
        score_info = [[s, index] for index, s in enumerate(score)]
        score_info.sort()

        max_state = (1 << n) - 1
        depend = [0] * n
        for x, y in edges:
            depend[y] |= (1 << x)

        def calc(now):
            if now == max_state:
                return 0
            if now not in f:
                f[now] = 0
                tmp = now
                cnt = 0
                while tmp:
                    cnt += 1
                    tmp -= tmp & -tmp
                
                candidate = []
                flag = True
                for score, index in score_info:
                    if now & (1 << index) == 0:
                        if now & depend[index] == depend[index]:
                            candidate.append((score, index))
                        else:
                            flag = False

                if flag:
                    for score, index in candidate:
                        f[now] += score * (cnt + 1)
                        cnt += 1
                else:
                    for score, index in candidate:
                        f[now] = max(f[now], calc(now | (1 << index)) + score * (cnt + 1))
            
            return f[now]
        
        return calc(0)
```
