---
title: "2920. 收集所有金币可获得的最大积分"
aliases: ["yiduobo的每日leetcode 2920.收集所有金币可获得的最大积分"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/tree", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/665118837"
zhihu_id: "665118837"
zhihu_title: "yiduobo的每日leetcode 2920.收集所有金币可获得的最大积分"
question_id: "2920"
question: "收集所有金币可获得的最大积分"
problem_url: "https://leetcode.cn/problems/maximum-points-after-collecting-coins-from-all-nodes/"
difficulty: "Hard"
rating: 2351
created: "2023-11-05T04:50:46+08:00"
updated: "2023-11-05T04:50:46+08:00"
upvotes: 0
comments: 0
---

# 2920. 收集所有金币可获得的最大积分

> **[yiduobo的每日leetcode 2920.收集所有金币可获得的最大积分](https://zhuanlan.zhihu.com/p/665118837) · 知乎 · 2023-11-05 · 赞同 0**
> 力扣：[2920. 收集所有金币可获得的最大积分](https://leetcode.cn/problems/maximum-points-after-collecting-coins-from-all-nodes/) · Hard · 灵茶山艾府：[树形 DP：记忆化搜索 / 递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2920.收集所有金币可获得的最大积分

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-points-after-collecting-coins-from-all-nodes/description/)

非常标准的树形动态规划的题目。对于题目中的两种操作，其中减k这一项无需讨论，而对于除以二向下取整这一项，除了对当前节点生效之外，还会对当前节点子树中的所有节点生效。注意到除以二向下取整实际上相当于右移操作，那么在这里就可以使用f[now][right_shift]表示以now为根节点的子树，其中now的祖先节点已经执行了right_shift次右移操作时，子树中可以得到的最大积分。

由于coins的最大值不超过10000，那么当右移的次数达到14次时，树中的节点值就都为0了，又因为k非负，因此子树中可以得到的最大积分必然为0，无需进行计算，而对于右移次数小于14次的f[now][right_shift]：

1、选择方案一。首先当前节点提供的积分为(coins[now] >> right_shift) - k，接下来遍历now的所有孩子节点child，递归求解f[child][right_shift]并将其累加起来，就是这种方案的积分v1

2、选择方案二。首先当前节点提供的节分为(coins[now] >> (right_shift + 1))，接下来遍历now的所有孩子节点child，递归求解f[child][right_shift + 1]并将其累加起来，就是这种方案的积分v2

使用v1和v2中的较大值作为f[now][right_shift]的值即可。

最后附上python代码：

```python
class Solution(object):
    def maximumPoints(self, edges, coins, k):
        """
        :type edges: List[List[int]]
        :type coins: List[int]
        :type k: int
        :rtype: int
        """

        n = len(edges) + 1
        g = {index : set() for index in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        f = [[None] * 14 for _ in range(n)]

        def dfs(now, right_shift, fa):
            if right_shift == 14:
                return 0

            if f[now][right_shift] is None:
                v1 = (coins[now] >> right_shift) - k
                v2 = coins[now] >> (right_shift + 1)
                for child in g[now]:
                    if child == fa:
                        continue
                    
                    v1 += dfs(child, right_shift, now)
                    v2 += dfs(child, right_shift + 1, now)
            
                f[now][right_shift] = max(v1, v2)
            
            return f[now][right_shift]
        
        return dfs(0, 0, None)
```
