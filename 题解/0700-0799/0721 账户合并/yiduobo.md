---
title: "721. 账户合并"
aliases: ["yiduobo的每日leetcode 721.账户合并"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/graph", "leetcode/recursion", "题单/常用数据结构", "题单/图论算法", "题单/常用数据结构/七-并查集", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/332525109"
zhihu_id: "332525109"
zhihu_title: "yiduobo的每日leetcode 721.账户合并"
question_id: "721"
question: "账户合并"
problem_url: "https://leetcode.cn/problems/accounts-merge/"
difficulty: "Medium"
created: "2020-12-06T18:37:20+08:00"
updated: "2020-12-06T18:37:20+08:00"
upvotes: 0
comments: 0
---

# 721. 账户合并

> **[yiduobo的每日leetcode 721.账户合并](https://zhuanlan.zhihu.com/p/332525109) · 知乎 · 2020-12-06 · 赞同 0**
> 力扣：[721. 账户合并](https://leetcode.cn/problems/accounts-merge/) · Medium · 灵茶山艾府：[哈希表 + DFS（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

721.账户合并

[力扣](https://leetcode-cn.com/problems/accounts-merge/)

由于题目中的email都是独一无二的，因此可以将每个email视为图中的一个点，对于同一个用户下的email，将这些email两两之间用边连起来。对于每个用户而言，其所有的email之间都是互相连通的，而不属于该用户的email则不相连。

接下来，对图中所有的节点进行染色，相连的节点染成同一种颜色，表示这些email属于同一个用户。

最后，根据节点对应的颜色合并email，排序后输出即可。

最后附上python代码：

```python
class Solution(object):
    def accountsMerge(self, accounts):
        """
        :type accounts: List[List[str]]
        :rtype: List[List[str]]
        """

        email_dict = {}
        email_list = []
        g = {}
        for account in accounts:
            owner = account[0]
            for email in account[1:]:
                if email not in email_dict:
                    email_dict[email] = len(email_list)
                    email_list.append([email, owner])
        
            for email_a in account[1:]:
                num_a = email_dict[email_a]
                if num_a not in g:
                    g[num_a] = []
                for email_b in account[1:]:
                    num_b = email_dict[email_b]
                    if num_a != num_b:
                        g[num_a].append(num_b)

        color = [0] * len(email_dict)

        now = 1
        for index in range(len(email_dict)):
            if color[index] == 0:
                self.dfs(index, now, color, g)
                now += 1
        
        res = {}
        for index, [email, owner] in enumerate(email_list):
            if color[index] not in res:
                res[color[index]] = [owner]
            res[color[index]].append(email)

        return [[x[0]] + sorted(x[1:]) for x in res.values()]

    def dfs(self, num, now, color, g):
        color[num] = now
        for next in g[num]:
            if color[next] == 0:
                self.dfs(next, now, color, g)
```
