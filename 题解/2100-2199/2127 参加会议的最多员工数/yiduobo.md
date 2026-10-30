---
title: "2127. 参加会议的最多员工数"
aliases: ["yiduobo的每日leetcode 2127.参加会议的最多员工数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/topological-sort", "题单/图论算法", "题单/图论算法/二-拓扑排序"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/526188601"
zhihu_id: "526188601"
zhihu_title: "yiduobo的每日leetcode 2127.参加会议的最多员工数"
question_id: "2127"
question: "参加会议的最多员工数"
problem_url: "https://leetcode.cn/problems/maximum-employees-to-be-invited-to-a-meeting/"
difficulty: "Hard"
rating: 2449
created: "2022-06-09T00:07:34+08:00"
updated: "2022-06-09T00:07:34+08:00"
upvotes: 0
comments: 0
---

# 2127. 参加会议的最多员工数

> **[yiduobo的每日leetcode 2127.参加会议的最多员工数](https://zhuanlan.zhihu.com/p/526188601) · 知乎 · 2022-06-09 · 赞同 0**
> 力扣：[2127. 参加会议的最多员工数](https://leetcode.cn/problems/maximum-employees-to-be-invited-to-a-meeting/) · Hard · 灵茶山艾府：[内向基环树：拓扑排序 + 分类讨论（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2127.参加会议的最多员工数

[力扣](https://leetcode.cn/problems/maximum-employees-to-be-invited-to-a-meeting/)

很有意思的题目。很明显应该从图论的角度来看这个问题，那么题目给出的图中，每个点可能有若干条入边，但仅有一条出边。

从题目的三个样例来看，一个自然的想法就是找出图中最长的环，将环上的员工按环的顺序直接安排在会议桌上就行了。由于题目的图中每个点只有一条出边，因此一趟遍历，利用栈模拟dfs就能找出图中所有的环。

但是实际上还有一种特殊情况，就是两个员工互相喜欢，也就是环的长度等于2的情况。对于这种情况，将这两个员工安排在一起之后，这两个员工分别都有一侧的位置是可以安排无关人员的。例如0和1互相喜欢，那么可以安排成[0, 1]，此时0的左边和1的右边都是可以任意安排人员的。那么在这里，完全可以在0的左边安排一个喜欢0的人，在1的右边安排一个喜欢1的人。更一般的，如果以0和1为终点，可以在图中找到两条长度最长的链，那么将这两条链上的人员按顺序分别安排在这两个员工空闲的那一侧同样也是合法的安排，此时安排的人员总数就是这两条链的长度之和。

值得注意的是，这种情况与上面环长度大于等于3的情况不兼容，但是可以兼容其他环长度为2的情况。

举个例子，0和1互相喜欢，2喜欢0，3喜欢1，4和5互相喜欢，6喜欢4，7喜欢5，那么图中就有两组长度为2的环，分别是[0, 1]和[4, 5]。更进一步的，按照上面的结论可以得到两组安排，分别是[2, 0, 1, 3]和[6, 4, 5, 7]。可以发现，如果让2和6，3和7安排在一起，得到的仍是合法的安排，此时安排的人数就是四条链上的长度之和了。

更一般的，由于在最开始已经找出了图中的所有环，那么从中找出长度为2的环，然后从环上的两个节点开始执行逆向bfs，就能找到以环上点为终点的最长的链。由于长度为2的环可以互相兼容，那么此时所有的链都可以同时安排在一起，因此此时应该用所有链的长度之和与图中最长环的长度对比来得到最终的答案。

本题可以用上面方法的所有前提都是每个点只有一条出边，这也就意味这可以高效地得到图中的环，同时在执行逆向bfs时，保证了不会出现两条不同的链上有重复的点。

最后附上python代码：

```python
class Solution(object):
    def maximumInvitations(self, favorite):
        """
        :type favorite: List[int]
        :rtype: int
        """

        g = {}
        used = set()
        n = len(favorite)
        res = 0
        pair = []
        for index in range(n):
            if favorite[index] not in g:
                g[favorite[index]] = set()
            g[favorite[index]].add(index)

            if index not in used:
                used.add(index)
                next = favorite[index]
                stack = [index]
                circle = set([index])
                while next not in circle and next not in used:
                    used.add(next)
                    circle.add(next)
                    stack.append(next)
                    next = favorite[next]
                
                if next not in circle:
                    continue

                step = 0
                while stack:
                    now = stack.pop()
                    step += 1
                    if now == next:
                        break

                if step == 2:
                    pair.append([now, favorite[now]])
                else:
                    res = max(res, step)

        def bfs(start):
            q = [start]
            l = 0
            r = 1
            step = 0
            while l < r:
                step += 1
                for now in q[l : r]:
                    for next in g.get(now, set()):
                        q.append(next)
                
                l, r = r, len(q)

            return step

        cnt = 0
        for x, y in pair:
            g[x].remove(y)
            g[y].remove(x)
            cnt += bfs(x) + bfs(y)

        return max(res, cnt)
```
