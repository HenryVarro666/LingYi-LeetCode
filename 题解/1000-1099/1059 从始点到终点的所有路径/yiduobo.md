---
title: "1059. 从始点到终点的所有路径"
aliases: ["yiduobo的每日leetcode 1059.从始点到终点的所有路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/607471272"
zhihu_id: "607471272"
zhihu_title: "yiduobo的每日leetcode 1059.从始点到终点的所有路径"
question_id: "1059"
question: "从始点到终点的所有路径"
problem_url: "https://leetcode.cn/problems/all-paths-from-source-lead-to-destination/"
created: "2023-02-18T20:13:04+08:00"
updated: "2023-02-18T20:13:04+08:00"
upvotes: 0
comments: 0
---

# 1059. 从始点到终点的所有路径

> **[yiduobo的每日leetcode 1059.从始点到终点的所有路径](https://zhuanlan.zhihu.com/p/607471272) · 知乎 · 2023-02-18 · 赞同 0**
> 力扣：[1059. 从始点到终点的所有路径](https://leetcode.cn/problems/all-paths-from-source-lead-to-destination/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1059.从始点到终点的所有路径

[力扣](https://leetcode.cn/problems/all-paths-from-source-lead-to-destination/)

首先，如果存在从destination出发的边，那么destination必然不是路径终点，此时直接返回false。

接下来，可能有以下几种情况使得最终答案为false，分别为：

1、从source出发的路径中存在环，包括自环。这里需要特别注意的是，不是从source出发的路径中存在环并不会影响最终结果，这也就意味着不能直接从source开始进行拓扑排序来判环，而是需要从source开始执行tarjan算法，通过low和dfn来判环。

在这里判环的处理方式只需对寻找强联通分量的处理方式进行一点修改，即出现low[now] \= dfn[now]时，判断当前栈顶元素是否为now，若不是，说明出现了环。

2、从source出发的路径在某个非destination节点终止。这种情况相对好判断，只需判断当前节点是否没有出边，且不是destination。

3、从source出发的路径没有经过destination。这种情况也很好判断，只需使用一个变量记录遍历的节点是否经过了destination。

根据上面的结论，就只需从source开始执行一趟target算法，在遍历的过程中顺便进行情况2和情况3的相关处理即可。

最后附上python代码：

```python
class Solution(object):
    def leadsToDestination(self, n, edges, source, destination):
        """
        :type n: int
        :type edges: List[List[int]]
        :type source: int
        :type destination: int
        :rtype: bool
        """

        g = {}
        for x, y in edges:
            if x == destination:
                return False

            if x not in g:
                g[x] = set()
            if y not in g[x]:
                g[x].add(y)

        dfn = [None] * n
        low = [None] * n
        stack = []
        in_stack = set()
        global flag, vis_des, cnt
        flag = True
        vis_des = False
        cnt = 0

        def dfs(now):
            global flag, vis_des, cnt
            dfn[now] = low[now] = cnt
            cnt += 1
            stack.append(now)
            in_stack.add(now)

            if now not in g:
                if now == destination:
                    vis_des = True
                else:
                    flag = False
                    return
            else:
                for next in g.get(now, set()):
                    if now == next:
                        flag = False
                        return
                    if dfn[next] is None:
                        dfs(next)
                        if not flag:
                            return
                        low[now] = min(low[now], low[next])
                    elif next in in_stack:
                        low[now] = min(low[now], low[next])
            
            if dfn[now] == low[now]:
                if stack[-1] != now:
                    flag = False
                    return
                
                stack.pop()
                in_stack.remove(now)

        dfs(source)
        return flag and vis_des
```
