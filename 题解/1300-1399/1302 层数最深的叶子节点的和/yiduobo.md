---
title: "1302. 层数最深的叶子节点的和"
aliases: ["yiduobo的每日leetcode 1302.层数最深的叶子节点的和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/391231666"
zhihu_id: "391231666"
zhihu_title: "yiduobo的每日leetcode 1302.层数最深的叶子节点的和"
question_id: "1302"
question: "层数最深的叶子节点的和"
problem_url: "https://leetcode.cn/problems/deepest-leaves-sum/"
created: "2021-07-19T22:21:14+08:00"
updated: "2021-07-19T22:21:14+08:00"
upvotes: 0
comments: 0
---

# 1302. 层数最深的叶子节点的和

> **[yiduobo的每日leetcode 1302.层数最深的叶子节点的和](https://zhuanlan.zhihu.com/p/391231666) · 知乎 · 2021-07-19 · 赞同 0**
> 力扣：[1302. 层数最深的叶子节点的和](https://leetcode.cn/problems/deepest-leaves-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1302.层数最深的叶子节点的和

[力扣](https://leetcode-cn.com/problems/deepest-leaves-sum/)

题目要求最深那一层叶子节点之和，那么我们可以直接执行一次层序遍历，并使用一个变量记录当前层所有节点之和。在层序遍历结束后，这个变量中记录的自然就是最深那一层叶子节点之后了。

最后附上python代码:

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def deepestLeavesSum(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        res = 0
        q = [root]
        l = 0
        r = 1
        while l < r:
            res = 0
            for now in q[l : r]:
                res += now.val
                if now.left:
                    q.append(now.left)
                if now.right:
                    q.append(now.right)
            
            l, r = r, len(q)
        
        return res
```
