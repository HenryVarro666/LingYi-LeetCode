---
title: "2477. 到达首都的最少油耗"
aliases: ["yiduobo的每日leetcode 2477.到达首都的最少油耗"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/贪心算法", "题单/链表-二叉树与回溯/三-一般树", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/588759005"
zhihu_id: "588759005"
zhihu_title: "yiduobo的每日leetcode 2477.到达首都的最少油耗"
question_id: "2477"
question: "到达首都的最少油耗"
problem_url: "https://leetcode.cn/problems/minimum-fuel-cost-to-report-to-the-capital/"
difficulty: "Medium"
rating: 2012
created: "2022-12-02T22:45:52+08:00"
updated: "2022-12-02T22:45:52+08:00"
upvotes: 0
comments: 0
---

# 2477. 到达首都的最少油耗

> **[yiduobo的每日leetcode 2477.到达首都的最少油耗](https://zhuanlan.zhihu.com/p/588759005) · 知乎 · 2022-12-02 · 赞同 0**
> 力扣：[2477. 到达首都的最少油耗](https://leetcode.cn/problems/minimum-fuel-cost-to-report-to-the-capital/) · Medium · 灵茶山艾府：[【图解】没有思路？一张图秒懂！（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2477.到达首都的最少油耗

[力扣](https://leetcode.cn/problems/minimum-fuel-cost-to-report-to-the-capital/)

由于题目中的换乘没有任何代价，且拼车的油耗必然是小于等于单独搭车的，因此每次乘车都应该尽量拼车，同时每次都只坐一站，然后在下一站与其他子树中的代表汇合之后，再继续考虑拼车的方案。

根据上面的结论，就得到了一种递归算法。对于当前节点now，遍历now的所有子节点child，先递归求解以child为根节点的子树，得到child这颗子树中代表的总数child_cnt，以及这些代表到达now所需的最小代价child_cost，同时使用两个变量tot_cnt和tot_cost分别将每颗子树的cnt和cost累加起来，tot_cnt和tot_cost的初始值应该为1和0。

遍历完所有子树之后，now这颗子树中的代表总数就是tot_cnt，而这些代表在now汇合之后到达now的父亲节点所需的代价就是tot_cnt / seats，向上取整。这里向上取整可以写成(tot \_cnt - 1) / seats + 1，因此总的代价就是tot_cost + (tot_cnt - 1) / seats + 1。

从root开始向下执行上述的递归算法，返回的cost就是最终答案了。

最后附上python代码：

```python
class Solution(object):
    def minimumFuelCost(self, roads, seats):
        """
        :type roads: List[List[int]]
        :type seats: int
        :rtype: int
        """

        g = {}
        for x, y in roads:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)

        def dfs(now, fa):
            tot_cnt = 1
            tot_cost = 0

            for child in g.get(now, set()):
                if child == fa:
                    continue
                child_cnt, child_cost = dfs(child, now)
                tot_cnt += child_cnt
                tot_cost += child_cost + (child_cnt - 1) / seats + 1

            return tot_cnt, tot_cost

        return dfs(0, -1)[1]
```
