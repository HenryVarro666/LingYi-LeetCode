---
title: "1820. 最多邀请的个数"
aliases: ["yiduobo的每日leetcode 1820.最多邀请的个数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/621786013"
zhihu_id: "621786013"
zhihu_title: "yiduobo的每日leetcode 1820.最多邀请的个数"
question_id: "1820"
question: "最多邀请的个数"
problem_url: "https://leetcode.cn/problems/maximum-number-of-accepted-invitations/"
created: "2023-04-13T23:55:15+08:00"
updated: "2023-04-13T23:55:15+08:00"
upvotes: 1
comments: 0
---

# 1820. 最多邀请的个数

> **[yiduobo的每日leetcode 1820.最多邀请的个数](https://zhuanlan.zhihu.com/p/621786013) · 知乎 · 2023-04-13 · 赞同 1**
> 力扣：[1820. 最多邀请的个数](https://leetcode.cn/problems/maximum-number-of-accepted-invitations/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1820.最多要求的个数

[力扣](https://leetcode.cn/problems/maximum-number-of-accepted-invitations/)

非常标准的最大匹配问题，常规做法是匈牙利算法或者建图后求最大流。

我在这里采用的是匈牙利算法，实现起来很简单，但是正确性的证明非常复杂，在这里就不展开了。

具体的算法简单描述起来就是遍历每个男孩，若其可以与某个未配对的女孩配对，或者这个女孩之前已配对的男孩可以找到其他未配对的女孩配对，那么就将这个男孩与女孩配对。

最后附上python代码：

```python
class Solution(object):
    def maximumInvitations(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        p = [None] * n

        def match(i):
            for j in range(n):
                if grid[i][j] == 1 and not vis[j]:
                    vis[j] = True
                    if p[j] is None or match(p[j]):
                        p[j] = i
                        return True
            return False

        res = 0
        for i in range(m):
            vis = [False] * n
            if match(i):
                res += 1
        
        return res
```
