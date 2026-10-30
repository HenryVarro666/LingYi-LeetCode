---
title: "515. 在每个树行中找最大值"
aliases: ["yiduobo的每日leetcode 515.在每个树行中找最大值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/260179190"
zhihu_id: "260179190"
zhihu_title: "yiduobo的每日leetcode 515.在每个树行中找最大值"
question_id: "515"
question: "在每个树行中找最大值"
problem_url: "https://leetcode.cn/problems/find-largest-value-in-each-tree-row/"
created: "2020-09-28T20:18:17+08:00"
updated: "2020-09-28T20:18:17+08:00"
upvotes: 0
comments: 0
---

# 515. 在每个树行中找最大值

> **[yiduobo的每日leetcode 515.在每个树行中找最大值](https://zhuanlan.zhihu.com/p/260179190) · 知乎 · 2020-09-28 · 赞同 0**
> 力扣：[515. 在每个树行中找最大值](https://leetcode.cn/problems/find-largest-value-in-each-tree-row/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

515.在每个树行中找最大值<https://leetcode-cn.com/problems/find-largest-value-in-each-tree-row/>

题目需要找到树中每一层的最大值，于是很自然想到求解树的层次遍历。由于这里需要找到同一层中的最大值，因此使用bfs一层一层来求解层次遍历是比较好的做法。

具体来说，就是在bfs过程中使用一组l和r来表示当前准备处理的这一层，在bfs队列中的头尾位置，然后从l遍历到r。对于当前层的每个节点，首先根据其val更新这一层的最大值，然后判断其是否具有left和right，若有，则将left和right加入到队列的末尾。处理完这一层之后，更新l和r求解下一层，重复上面的过程直到求解完整棵树为止。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def largestValues(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """

        if not root:
            return []

        q = [root]
        l = 0
        r = 1
        new_r = r
        res = []
        while l < r:
            level_max = None
            for index in range(l, r):
                now = q[index]
                if level_max is None or level_max < now.val:
                    level_max = now.val
                if now.left:
                    q.append(now.left)
                    new_r += 1
                if now.right:
                    q.append(now.right)
                    new_r += 1
            res.append(level_max)

            l = r
            r = new_r

        return res
```
