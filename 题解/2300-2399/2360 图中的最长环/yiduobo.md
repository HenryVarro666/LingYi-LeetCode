---
title: "2360. 图中的最长环"
aliases: ["yiduobo的每日leetcode 2360.图中的最长环"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/graph", "题单/图论算法", "题单/图论算法/二-拓扑排序"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/562371384"
zhihu_id: "562371384"
zhihu_title: "yiduobo的每日leetcode 2360.图中的最长环"
question_id: "2360"
question: "图中的最长环"
problem_url: "https://leetcode.cn/problems/longest-cycle-in-a-graph/"
difficulty: "Hard"
rating: 1897
created: "2022-09-08T01:40:57+08:00"
updated: "2022-09-08T01:40:57+08:00"
upvotes: 0
comments: 0
---

# 2360. 图中的最长环

> **[yiduobo的每日leetcode 2360.图中的最长环](https://zhuanlan.zhihu.com/p/562371384) · 知乎 · 2022-09-08 · 赞同 0**
> 力扣：[2360. 图中的最长环](https://leetcode.cn/problems/longest-cycle-in-a-graph/) · Hard · 灵茶山艾府：[在操场上跑步，跑一圈要多久（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2360.图中的最长环

[力扣](https://leetcode.cn/problems/longest-cycle-in-a-graph/)

与上一题类似，也是每个点只有一条出边，因此可以照搬上一题的，从每个点出发不断往下走，直到无法继续往下走或者走回到之前到过的节点为止。

对于本题，除了常规的行走外还需要记录环，在这里就需要使用另一组访问记录来储存本次行走到过的节点，而不能用全局的访问记录，因为新的环只可能是从本次行走路径上的某个节点出发，走回到本次行走路径上的某个节点，而一旦走到之前访问过的节点，那么在之前某次行走过程中就已经把从这个访问过的节点出发所能走到的节点都走过了，同时期间可能出现的环也已经记录下来了。这里有一个隐藏条件就是直到本轮行走才第一次访问到的这几个节点必然不在之前找到的环中，否则在之前的行走轮次中这几个节点就已经被访问过了。换言之，一旦走到之前访问过的节点，接下来的行走就不可能走回到本轮才访问到的节点，也就是说不会形成新的环了。

根据上面的结论，在这里就必须使用新的一组访问记录，同时这组访问记录还需要记录下访问某个节点的时间戳，那么如果有环存在，就会走到某个本轮才第一次访问到的节点，同时第一次和第二次访问的时间戳之差就是环的长度。当然，在完成本次访问后，还需要将这一组新的访问记录合并到全局的访问记录当中。

由于每个节点只会被访问一次，因此最终的时间复杂度还是O(n)。

最后附上python代码：

```python
class Solution(object):
    def longestCycle(self, edges):
        """
        :type edges: List[int]
        :rtype: int
        """

        n = len(edges)
        used = set()
        res = -1
        for index in range(n):
            if index not in used:
                now = index
                step = {}
                step[now] = 0
                while True:
                    next = edges[now]
                    if next == -1:
                        break

                    if next in step:
                        res = max(res, step[now] - step[next] + 1)
                        break
                    
                    if next in used:
                        break
                    
                    step[next] = step[now] + 1
                    now = next
                
                for num in step:
                    used.add(num)
        
        return res
```
