---
title: "559. N叉树的最大深度"
aliases: ["yiduobo的每日leetcode 559.N叉树的最大深度"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/266049184"
zhihu_id: "266049184"
zhihu_title: "yiduobo的每日leetcode 559.N叉树的最大深度"
question_id: "559"
question: "N叉树的最大深度"
problem_url: "https://leetcode.cn/problems/maximum-depth-of-n-ary-tree/"
created: "2020-10-15T21:46:20+08:00"
updated: "2020-10-15T21:46:20+08:00"
upvotes: 0
comments: 0
---

# 559. N叉树的最大深度

> **[yiduobo的每日leetcode 559.N叉树的最大深度](https://zhuanlan.zhihu.com/p/266049184) · 知乎 · 2020-10-15 · 赞同 0**
> 力扣：[559. N叉树的最大深度](https://leetcode.cn/problems/maximum-depth-of-n-ary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

昨日有事外出，今天补上。

559.N叉树的最大深度<https://leetcode-cn.com/problems/maximum-depth-of-n-ary-tree/>

对于以节点p为根节点的子树而言，其深度取决于其最深的子树有多深，于是可以优先递归求解其所有子树的深度，然后其中的最大值加一即为以p为根节点的子树。

最后附上python代码：

```python
"""
# Definition for a Node.
class Node(object):
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children
"""

class Solution(object):
    def maxDepth(self, root):
        """
        :type root: Node
        :rtype: int
        """

        return self.dfs(root)

    def dfs(self, now):
        if not now:
            return 0
        
        depth = 0
        for child in now.children:
            depth = max(depth, self.dfs(child))
        return depth + 1
```
