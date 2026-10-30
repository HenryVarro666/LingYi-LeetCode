---
title: "314. 二叉树的垂直遍历"
aliases: ["yiduobo的每日leetcode 314.二叉树的垂直遍历"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/595939660"
zhihu_id: "595939660"
zhihu_title: "yiduobo的每日leetcode 314.二叉树的垂直遍历"
question_id: "314"
question: "二叉树的垂直遍历"
problem_url: "https://leetcode.cn/problems/binary-tree-vertical-order-traversal/"
created: "2023-01-02T03:30:07+08:00"
updated: "2023-01-02T03:30:07+08:00"
upvotes: 1
comments: 0
---

# 314. 二叉树的垂直遍历

> **[yiduobo的每日leetcode 314.二叉树的垂直遍历](https://zhuanlan.zhihu.com/p/595939660) · 知乎 · 2023-01-02 · 赞同 1**
> 力扣：[314. 二叉树的垂直遍历](https://leetcode.cn/problems/binary-tree-vertical-order-traversal/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

314.二叉树的垂直遍历

[力扣](https://leetcode.cn/problems/binary-tree-vertical-order-traversal/)

从树个根节点开始向下进行bfs，同时记录当前节点的垂直位置。当向左子树走时，将这个垂直位置减去1，反之当向右子树走时，则将这个垂直位置加上1。在bfs过程中使用哈希表将所有节点按照其对应的垂直位置收集起来，bfs完成后只需将哈希表的值按照key从小到大排序即为最终答案。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def verticalOrder(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """

        if not root:
            return []

        res = {}
        q = [[root, 0]]
        head, tail = 0, 1
        while head < tail:
            now, p = q[head]
            if p not in res:
                res[p] = []
            res[p].append(now.val)
            head += 1

            if now.left:
                q.append([now.left, p - 1])
                tail += 1
            if now.right:
                q.append([now.right, p + 1])
                tail += 1
        
        return [x[1] for x in sorted(res.items(), key=lambda d:d[0])]
```
