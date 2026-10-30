---
title: "LCP 09. 最小跳跃次数"
aliases: ["yiduobo的每日leetcode LCP09.最小跳跃次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/570888370"
zhihu_id: "570888370"
zhihu_title: "yiduobo的每日leetcode LCP09.最小跳跃次数"
question_id: "LCP 09"
question: "最小跳跃次数"
problem_url: "https://leetcode.cn/problems/zui-xiao-tiao-yue-ci-shu/"
created: "2022-10-06T03:54:11+08:00"
updated: "2022-10-06T03:54:11+08:00"
upvotes: 1
comments: 0
---

# LCP 09. 最小跳跃次数

> **[yiduobo的每日leetcode LCP09.最小跳跃次数](https://zhuanlan.zhihu.com/p/570888370) · 知乎 · 2022-10-06 · 赞同 1**
> 力扣：[LCP 09. 最小跳跃次数](https://leetcode.cn/problems/zui-xiao-tiao-yue-ci-shu/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP09.最小跳跃次数

[力扣](https://leetcode.cn/problems/zui-xiao-tiao-yue-ci-shu/)

如果从数组的角度来看，本题是非常典型的动态规划问题。如果从图论的角度来看，本题则是非常典型的最短路问题。我在这里采用的是图论的视角。

题目给出了n个点，编号为0到n - 1。对于每个点i，都存在一条i到i + jump[i]的有向边，以及从i到0、i到1、...、i到i - 1这一系列往回走的有向边。图中所有的边权重都为1，问从0走到n - 1的最短路径长度是多少。

题目中的图，边的规模是O(n^2)级的，因此常规的dijkstra算法是不行的。注意到边权重都为1，那么在这里可以尝试使用bfs来解决问题。常规bfs的时间复杂度依然与边的数量挂钩，在这里时间复杂度还是太高了，需要想办法进行优化。

可以发现，bfs中大量的时间实际上被用在了往回走这个操作上，但是很多情况下已经没有往回走的必要了。举个例子：如果到达节点p的最短路径长度为k，那么到达节点1、节点2、...、节点p - 1这些节点的最短路径长度最多就是k + 1了，因为可以先走到p再往回走。在这个前提下，若到达某个节点q的最短路径长度为m，且m >\= k，那么就从q开始往回走的时候就没有必要再计算节点1到节点p - 1这些节点了，因为这样得到的路径长度必然不是最优的。

更一般的，可以使用一个变量last_backfill记录当前已经处理过的最远的节点，那么对于当前节点now，由于bfs的特性，走到now的最短路径长度必然是大于等于走到last_backfill的最短路径长度的，因此就没必要从now出发走回1到last_backfill中的任意节点了，只需要考虑走回到last_backfill + 1到now - 1之间的节点，以及从now向右走到达的now + jump[now]这个节点。这样一来，就可以在均摊O(1)的时间内完成整个bfs了。

最后附上python代码：

```python
class Solution(object):
    def minJump(self, jump):
        """
        :type jump: List[int]
        :rtype: int
        """

        n = len(jump)
        f = [None] * n
        f[0] = 0
        q = [0]
        head, tail = 0, 1
        last_backfill = 0
        while head < tail:
            now = q[head]
            head += 1
            if now + jump[now] >= n:
                return f[now] + 1
            
            if f[now + jump[now]] is None:
                q.append(now + jump[now])
                f[now + jump[now]] = f[now] + 1
                tail += 1

            for index in range(last_backfill + 1, now):
                if f[index] is None:
                    q.append(index)
                    f[index] = f[now] + 1
                    tail += 1
            
            last_backfill = max(last_backfill, now)
```
