---
title: "1377. T秒后青蛙的位置"
aliases: ["yiduobo的每日leetcode 1377.T秒后青蛙的位置"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/401971149"
zhihu_id: "401971149"
zhihu_title: "yiduobo的每日leetcode 1377.T秒后青蛙的位置"
question_id: "1377"
question: "T 秒后青蛙的位置"
problem_url: "https://leetcode.cn/problems/frog-position-after-t-seconds/"
difficulty: "Hard"
rating: 1824
created: "2021-08-20T23:01:54+08:00"
updated: "2021-08-20T23:01:54+08:00"
upvotes: 0
comments: 0
---

# 1377. T秒后青蛙的位置

> **[yiduobo的每日leetcode 1377.T秒后青蛙的位置](https://zhuanlan.zhihu.com/p/401971149) · 知乎 · 2021-08-20 · 赞同 0**
> 力扣：[1377. T 秒后青蛙的位置](https://leetcode.cn/problems/frog-position-after-t-seconds/) · Hard · 灵茶山艾府：[DFS + 记一次有趣的 hack](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1377.T秒后青蛙的位置

[力扣](https://leetcode-cn.com/problems/frog-position-after-t-seconds/)

令f[i]表示首次到达节点i的概率，那么对于节点i而言：

1、若其为根节点，那么f[i] \= 1.0

2、若其不为根节点，设其父亲节点为j，那么首次到达节点j的概率为f[j]。接下来我们从j走到i，设j有k个孩子，那么走到每个孩子的概率都是1/k，那么就有f[i] \= f[j] / k。

于是我们可以先将整棵树构造出来，接下来从根节点开始进行bfs，一共执行t轮。此时又有几种情况：

1、若t轮后依然没有到达target，那么答案为0

2、若t轮后恰好到达了target，那么答案就是f[target]

3、若第p轮就到达了target，且p \< t，那么此时应该根据target是否有孩子节点来进行判断。若target有孩子节点，那么在第p + 1轮青蛙就会从target跳走，且之后不会再跳回来，因此答案为0。若target没有孩子节点，那么青蛙会一直留在target，因此答案为f[target]

最后附上python代码：

```python
class Solution(object):
    def frogPosition(self, n, edges, t, target):
        """
        :type n: int
        :type edges: List[List[int]]
        :type t: int
        :type target: int
        :rtype: float
        """

        if n == 1:
            return 1.0

        g = {x : set() for x in range(1, n + 1)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)
        
        g[1].add(0)

        f = [0] * (n + 1)
        f[1] = 1.0
        q = [1]
        l = 0
        r = 1
        used = set([0, 1])
        step = 0
        while l < r:
            h = [0] * (n + 1)
            step += 1
            if step > t:
                break
            for now in q[l : r]:
                for next in g[now]:
                    if next not in used:
                        h[next] = f[now] * (len(g[now]) - 1)
                        q.append(next)
                        used.add(next)
                        if next == target:
                            if len(g[next]) == 1 or step == t:
                                return 1.0 / h[next]
                            else:
                                return 0.0

            l, r = r, len(q)
            f = h[:]
        
        return 0.0
```
