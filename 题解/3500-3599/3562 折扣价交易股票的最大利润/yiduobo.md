---
title: "3562. 折扣价交易股票的最大利润"
aliases: ["yiduobo的每日leetcode 3562.折扣价交易股票的最大利润"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/三-背包", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1910525012022101249"
zhihu_id: "1910525012022101249"
zhihu_title: "yiduobo的每日leetcode 3562.折扣价交易股票的最大利润"
question_id: "3562"
question: "折扣价交易股票的最大利润"
problem_url: "https://leetcode.cn/problems/maximum-profit-from-trading-stocks-with-discounts/"
difficulty: "Hard"
rating: 2458
created: "2025-05-29T22:22:25+08:00"
updated: "2025-05-29T22:22:25+08:00"
upvotes: 0
comments: 0
---

# 3562. 折扣价交易股票的最大利润

> **[yiduobo的每日leetcode 3562.折扣价交易股票的最大利润](https://zhuanlan.zhihu.com/p/1910525012022101249) · 知乎 · 2025-05-29 · 赞同 0**
> 力扣：[3562. 折扣价交易股票的最大利润](https://leetcode.cn/problems/maximum-profit-from-trading-stocks-with-discounts/) · Hard · 灵茶山艾府：[树上背包 + 状态机 DP，两种写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3562.折扣价交易股票的最大利润

[3562. 折扣价交易股票的最大利润 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-profit-from-trading-stocks-with-discounts/description/)

题目给出一个整数n，表示公司中员工的数目，n的规模不超过150。每位员工都分配了一个从1到n的唯一ID，其中1号员工是CEO。

另外给出两个下标从1开始的整数数组present以及future，长度均为n，两个数组中的元素大小都不超过50。其中present[index]表示index号员工今天可以购买股票的当前价格，future[index]则表示index号员工明天可以卖出股票的预期价格，每支股票只能购买一次。

公司的层级关系由二维数组hierarchy表示，长度为n - 1。其中hierarchy\[index\] \= \[u\[index\], v\[index\]\]，表示员工u\[index\]是v\[index\]的直属上级。题目保证CEO是所有员工的直接或者间接上级，同时hierarchy中无环。

再给出一个整数budget，表示可以用于投资的总预算，budget不超过160。

公司现在由一项折扣政策：如果某位员工的直属上级购买了自己的股票，那么该员工就可以半价购买自己的股票，也就是present[index] // 2。

问如何分配budget这些预算，使得明天的预期收益最大。

n个点，n - 1条边，同时CEO还是所有人的直接或者间接上级，那么题目给出的就是一颗树，同时树中的节点要么为根节点，要么只有唯一的父亲节点。

对于这类树中节点二选一的问题，一般是使用动态规划，自顶向下递归进行求解。令f[now][b][pre_buy]表示以now为根节点的子树中，如果有b的预算，且now的父亲节点购买状态为pre_buy时可以得到的最大收益，其中pre_buy为0表示父节点没买，为1则表示买了。在这里使用01而不是false、true的理由是后续计算now的购买代价时可以直接用present[now - 1] // (pre_buy + 1)来计算。

对于f[now][b][pre_buy]：

首先考虑now不买的情况。这种情况下，所有预算都可以分配给其中的某个孩子，因此就需要先遍历now的所有孩子节点nxt，然后从0到b枚举分配给nxt的预算sub，递归计算f[nxt][sub][0]。

得到所有的f[nxt][sub][0]之后，题目就变成了背包问题：对于nxt，使用sub的代价可以获取f[nxt][sub][0]的收益，问如何分配当前的预算b可以使得收益最大。

令g[b]表示分配b的预算可以得到的最大收益，那么对于g[b]，可以遍历所有孩子nxt以及对应的所有sub，使用g[b - sub] + f[nxt][sub][0]来更新g[b]。

需要注意这里b必须倒序遍历，因为这种实现方法实际上是基于g[index][b]表示将预算b分配给前index个孩子节点可以获得的最大收益这种状态表示，通过倒序遍历迭代省去index这一维的实现方法。

接下来考虑now买的情况。这种情况下与上面类似，不过在这里需要先计算出now本身消耗掉的预算，也就是buy_cost \= present[now - 1] // (pre_buy + 1)。

此时就相当于将b - buy_cost的预算分配给now的孩子节点，于是就需要遍历now的所有孩子节点nxt，然后从0到b - buy_cost枚举分配给nxt的预算sub，递归计算f[nxt][sub][1]。

得到所有的f[nxt][sub][1]之后，依然是使用动态规划求解背包问题。

令h[b]表示分配b的预算可以得到的最大收益，那么对于h[b]，可以遍历所有的孩子nxt以及对应的所有sub，使用h[b - sub] + f[nxt][sub][1]来更新g[b]。需要特别注意的是，这里b的应该从b - buy_cost开始向下遍历，因为必须预留buy_cost让now购买自己的股票。

得到g和h后，就可以用max(g[b], h[b - buy_cost] + future[now - 1] - buy_cost)来更新f[now][b][pre_buy]，而最终答案即为f[1][budget][0]。

另外本题对python似乎不太友好，当然也可能是我对python的变量在内存中的排布方式以及访问消耗理解不够，使用标准的O(n \* b^2)的算法依然会超时。最后只能将写法改为非递归，具体来说就是从孩子节点开始，自底向上计算，而计算的顺序则可以通过反向建图后使用拓扑排序来决定。在计算的顺序上，可以在计算完f[now]的所有状态之后直接使用f[now]中的值来更新now的父节点对应的g和h。

最后附上python代码：

```python
class Solution(object):
    def maxProfit(self, n, present, future, hierarchy, budget):
        """
        :type n: int
        :type present: List[int]
        :type future: List[int]
        :type hierarchy: List[List[int]]
        :type budget: int
        :rtype: int
        """
        
        t = [[] for _ in range(n + 1)]
        ind = [0] * (n + 1)
        for x, y in hierarchy:
            t[y].append(x)
            ind[x] += 1
        
        q = deque()
        f = [[[0] * 2 for _ in range(budget + 1)] for _ in range(n + 1)]
        g = [[0] * (budget + 1) for _ in range(n + 1)]
        h = [[0] * (budget + 1) for _ in range(n + 1)]
        for index in range(1, n + 1):
            if ind[index] == 0:
                q.append(index)

        while q:
            now = q.popleft()
            for pre_buy in range(2):
                buy_cost = present[now - 1] // (pre_buy + 1)
                buy_reward = future[now - 1] - buy_cost

                for b in range(budget + 1):
                    f[now][b][pre_buy] = g[now][b]
                    if b >= buy_cost:
                        f[now][b][pre_buy] = max(f[now][b][pre_buy], h[now][b - buy_cost] + buy_reward)

            for pre in t[now]:
                ind[pre] -= 1
                if ind[pre] == 0:
                    q.append(pre)
                
                for b in range(budget, -1, -1):
                    for sub in range(b + 1):
                        g[pre][b] = max(g[pre][b], g[pre][b - sub] + f[now][sub][0])
                
                for b in range(budget - present[pre - 1] // 2, -1, -1):
                    for sub in range(b + 1):
                        h[pre][b] = max(h[pre][b], h[pre][b - sub] + f[now][sub][1])
    
        return f[1][budget][0]
```
