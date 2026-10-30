---
title: "2976. 转换字符串的最小成本I"
aliases: ["yiduobo的每日leetcode 2976.转换字符串的最小成本I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/shortest-path", "题单/图论算法", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/692024735"
zhihu_id: "692024735"
zhihu_title: "yiduobo的每日leetcode 2976.转换字符串的最小成本I"
question_id: "2976"
question: "转换字符串的最小成本 I"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-convert-string-i/"
difficulty: "Medium"
rating: 1882
created: "2024-04-12T01:46:00+08:00"
updated: "2024-04-12T01:46:00+08:00"
upvotes: 1
comments: 0
---

# 2976. 转换字符串的最小成本I

> **[yiduobo的每日leetcode 2976.转换字符串的最小成本I](https://zhuanlan.zhihu.com/p/692024735) · 知乎 · 2024-04-12 · 赞同 1**
> 力扣：[2976. 转换字符串的最小成本 I](https://leetcode.cn/problems/minimum-cost-to-convert-string-i/) · Medium · 灵茶山艾府：[Floyd 算法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2976.转换字符串的最小成本I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-cost-to-convert-string-i/description/)

将字符视为图中的节点，转换的代价视为图中的边，那么交换两个字符的最小代价就是图中对应节点的最短路径长度，于是使用floyd算法提前预处理出交换任意两个字符的代价，接下来就只需一趟遍历，将转换的代价累加起来即可。

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, source, target, original, changed, cost):
        """
        :type source: str
        :type target: str
        :type original: List[str]
        :type changed: List[str]
        :type cost: List[int]
        :rtype: int
        """

        max_dis = 10 ** 6
        dis = [[-1] * 26 for _ in range(26)]
        for index in range(26):
            dis[index][index] = 0

        m = len(original)
        for index in range(m):
            x = ord(original[index]) - 97
            y = ord(changed[index]) - 97
            if dis[x][y] == -1 or dis[x][y] > cost[index]:
                dis[x][y] = cost[index]
        
        for k in range(26):
            for i in range(26):
                for j in range(26):
                    if dis[i][k] != -1 and dis[k][j] != -1 and (dis[i][j] == -1 or dis[i][j] > dis[i][k] + dis[k][j]):
                        dis[i][j] = dis[i][k] + dis[k][j]
        
        res = 0
        n = len(source)
        for index in range(n):
            x = ord(source[index]) - 97
            y = ord(target[index]) - 97
            if dis[x][y] != -1:
                res += dis[x][y]
            else:
                return -1
        
        return res
```
