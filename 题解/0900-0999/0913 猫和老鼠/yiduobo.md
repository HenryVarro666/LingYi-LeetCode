---
title: "913. 猫和老鼠"
aliases: ["yiduobo的每日leetcode 913.猫和老鼠"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/graph", "leetcode/topological-sort", "leetcode/dynamic-programming", "题单/动态规划", "题单/数学算法", "题单/动态规划/十三-图-DP", "题单/动态规划/十四-博弈-DP", "题单/数学算法/四-博弈论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/354963055"
zhihu_id: "354963055"
zhihu_title: "yiduobo的每日leetcode 913.猫和老鼠"
question_id: "913"
question: "猫和老鼠"
problem_url: "https://leetcode.cn/problems/cat-and-mouse/"
difficulty: "Hard"
rating: 2800
created: "2021-03-06T00:06:10+08:00"
updated: "2021-03-06T00:06:10+08:00"
upvotes: 3
comments: 1
---

# 913. 猫和老鼠

> **[yiduobo的每日leetcode 913.猫和老鼠](https://zhuanlan.zhihu.com/p/354963055) · 知乎 · 2021-03-06 · 赞同 3**
> 力扣：[913. 猫和老鼠](https://leetcode.cn/problems/cat-and-mouse/) · Hard · 灵茶山艾府：[逆向思维 + 拓扑序 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

913.猫和老鼠

[力扣](https://leetcode-cn.com/problems/cat-and-mouse/)

很有意思的题目。

首先，由于是回合制下的最优行动，那么很自然可以想到使用状态机来解决这个问题。设图中一共有n个节点，那么使用一个n \* n的数组mouse和一个n \* n的数组cat，其中mouse[i][j]表示当老鼠处于节点i，猫处于节点j时如果老鼠先行动的最终结果，cat[i][j]则表示当老鼠处于节点i，猫处于节点j时如果猫先行动的最终结果。

显然，一开始我们就能确定一系列的值，例如mouse[0][x]以及cat[0][x]必然为老鼠获胜，而mouse[x][x]以及cat[x][x]则必然为猫获胜。需要注意猫不能进老鼠洞，因此这里的x大于0。

接下来，我们需要想办法求出其他状态的值。

由于题目中可能出现平局状态，例如样例中的老鼠在节点3和4反复横跳，而猫则是在节点2和5跟着反复横跳，因此使用普通的bfs会出现死循环的情况。

不过既然我们知道了一些确定的值，那么我们可以换一种思路，从这些确定的值开始倒推，这就联想到了某种类似拓扑排序的做法。

不妨设当前确定的状态为(i, j, now)，表示当前老鼠在节点i，猫在节点j，行动的是now：

1、若now为老鼠，那么说明上一步行动的是猫。为了到达(i, j, 老鼠)，那么猫可以从与j相连的非零节点走过来，于是我们可以枚举j的非0相邻节点，设为last：

1-1、若mouse[i][j]为猫获胜，那么对于(i, last, 猫)而言，此时猫只需要从last走到j就达到了状态(i, j, 老鼠)，而此时已知该状态下猫获胜，因此可以推导出cat[i][last]也是猫获胜。

1-2、若mouse[i][j]为老鼠获胜，那么对于(i, last, 猫)而言，此时猫应该避免从last走到j。

在这里，如果我们从(i, last, 猫)的角度来看这个问题，就可以得到结论：

1)若猫可以走到一个猫最终获胜的状态，那么cat[i][last]为猫获胜。此时应该将(i, last, 猫)也加入到倒推的队列当中。

2)若猫接下来走到的状态都是老鼠获胜，那么cat[i][last]为老鼠获胜，否则说明猫接下来走到的状态中有不确定的情况，因此cat[i][last]暂时也无法确定。当然，这里猫从last出发可以走的方案数有限，因此一旦从确定状态推到到cat[i][last]的次数达到了这个方案数，且其中没有猫获胜的状态，那么就可以确定此时获胜的是老鼠。

具体实现时就可以参考拓扑排序，使用一个oud_cat数组，其中oud_cat[i][j]表示老鼠处于节点i，猫处于节点j时剩余可行的非必败方案数，初始化为猫从j出发可以到达的节点数，也就是graph[j]中非0值的个数。当每次从老鼠必胜态推导到cat[i][j]时，就将oud_cat[i][j]减去1，若某个时刻oud_cat[i][j]等于0，那么就可以确定此时老鼠获胜。此时也应该将(i, last, 猫)加入到倒推的队列当中。

2、若now为老鼠，此时的处理与猫完全对称。这里的老鼠虽然比猫多出一个节点0可以去，但是实际上所有老鼠处于节点0的状态都是已经确定的状态，无需再进行求解，因此对老鼠求解的过程与猫完全对称。

当整个倒推完成之后，返回mouse[1][2]的结果即可。

最后附上python代码：

```python
class Solution(object):
    def catMouseGame(self, graph):
        """
        :type graph: List[List[int]]
        :rtype: int
        """

        zero_connect = set()
        for x in graph[0]:
            zero_connect.add(x)

        n = len(graph)
        mouse = [[0] * n for _ in range(n)]
        cat = [[0] * n for _ in range(n)]
        oud_mouse = [[0] * n for _ in range(n)]
        oud_cat = [[0] * n for _ in range(n)]

        q = []
        for i in range(n):
            for j in range(1, n):
                if i == 0:
                    mouse[i][j] = 1
                    cat[i][j] = 1
                    q.append([i, j, 1])
                    q.append([i, j, 2])
                elif i == j:
                    mouse[i][j] = 2
                    cat[i][j] = 2
                    q.append([i, j, 1])
                    q.append([i, j, 2])
                else:
                    oud_mouse[i][j] = len(graph[i])
                    oud_cat[i][j] = len(graph[j])
                    if j in zero_connect:
                        oud_cat[i][j] -= 1

        l = 0
        r = len(q)
        while l < r:
            i, j, now = q[l]
            l += 1
            if now == 1:
                for last in graph[j]:
                    if last == 0:
                        continue
                    if cat[i][last] == 0:
                        if mouse[i][j] == 2:
                            cat[i][last] = 2
                            q.append([i, last, 2])
                            r += 1
                        elif mouse[i][j] == 1:
                            oud_cat[i][last] -= 1
                            if oud_cat[i][last] == 0:
                                cat[i][last] = 1
                                q.append([i, last, 2])
                                r += 1
            else:
                for last in graph[i]:
                    if mouse[last][j] == 0:
                        if cat[i][j] == 1:
                            mouse[last][j] = 1
                            q.append([last, j, 1])
                            r += 1
                        elif cat[i][j] == 2:
                            oud_mouse[last][j] -= 1
                            if oud_mouse[last][j] == 0:
                                mouse[last][j] = 2
                                q.append([last, j, 1])
                                r += 1

        return mouse[1][2]
```
