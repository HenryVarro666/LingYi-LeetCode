---
title: "637. 二叉树的层平均值"
aliases: ["yiduobo的每日leetcode 637.二叉树的层平均值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/270976109"
zhihu_id: "270976109"
zhihu_title: "yiduobo的每日leetcode 637.二叉树的层平均值"
question_id: "637"
question: "二叉树的层平均值"
problem_url: "https://leetcode.cn/problems/average-of-levels-in-binary-tree/"
created: "2020-11-01T15:57:20+08:00"
updated: "2020-11-01T15:57:20+08:00"
upvotes: 0
comments: 0
---

# 637. 二叉树的层平均值

> **[yiduobo的每日leetcode 637.二叉树的层平均值](https://zhuanlan.zhihu.com/p/270976109) · 知乎 · 2020-11-01 · 赞同 0**
> 力扣：[637. 二叉树的层平均值](https://leetcode.cn/problems/average-of-levels-in-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

637.二叉树的层平均值

[力扣](https://leetcode-cn.com/problems/average-of-levels-in-binary-tree/)

使用bfs执行二叉树的层序遍历，每计算一层则统计盖层的节点值和从而计算出平均值。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def averageOfLevels(self, root):
        """
        :type root: TreeNode
        :rtype: List[float]
        """

        res = []
        q = [root]
        l = 0
        r = 1
        while l < r:
            newr = r
            tmp = 0
            for index in range(l, r):
                now = q[index]
                tmp += now.val
                if now.left:
                    q.append(now.left)
                    newr += 1
                if now.right:
                    q.append(now.right)
                    newr += 1
            
            res.append(tmp * 1.0 / (r - l))
            l = r
            r = newr

        return res
```
