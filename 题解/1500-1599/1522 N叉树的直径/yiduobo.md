---
title: "1522. N叉树的直径"
aliases: ["yiduobo的每日leetcode 1522.N叉树的直径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/617230833"
zhihu_id: "617230833"
zhihu_title: "yiduobo的每日leetcode 1522.N叉树的直径"
question_id: "1522"
question: "N叉树的直径"
problem_url: "https://leetcode.cn/problems/diameter-of-n-ary-tree/"
created: "2023-03-27T00:53:23+08:00"
updated: "2023-03-27T00:53:23+08:00"
upvotes: 0
comments: 0
---

# 1522. N叉树的直径

> **[yiduobo的每日leetcode 1522.N叉树的直径](https://zhuanlan.zhihu.com/p/617230833) · 知乎 · 2023-03-27 · 赞同 0**
> 力扣：[1522. N叉树的直径](https://leetcode.cn/problems/diameter-of-n-ary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1522.N叉树的直径

[力扣](https://leetcode.cn/problems/diameter-of-n-ary-tree/)

对于树的直径这个问题，经典的做法是一次dfs找出一个最远端节点，然后从这个节点出发再一次dfs找出树的直径，不过本题给出的树的根节点，那么也可以采用分析最长链的递归算法来进行求解。

具体来说，树的直径必然是由两条从某棵子树的根节点出发的树链构成的，于是可以从整颗树的根节点开始向下递归求解，对于当前处理的节点now，遍历其所有的孩子节点并递归求解，在这个过程中记录顺便计算这些孩子节点为根节点的子树中从根节点出发的最长的树链长度，取其中的top 2就组成了以now为根节点的子树中最长的路径，接下来只需使用这个长度更新答案，并返回子树中最长树链长度加1供上层节点使用即可。

最后附上python代码：

```python
"""
# Definition for a Node.
class Node(object):
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []
"""

class Solution(object):
    def diameter(self, root):
        """
        :type root: 'Node'
        :rtype: int
        """

        if not root:
            return 0

        global res
        res = 0

        def dfs(now):
            first = second = 0
            for child in now.children:
                d = dfs(child)
                if d > first:
                    first, second = d, first
                elif d > second:
                    second = d
            
            global res

            res = max(res, first + second + 1)
            return first + 1
        
        dfs(root)
        return res - 1
```
