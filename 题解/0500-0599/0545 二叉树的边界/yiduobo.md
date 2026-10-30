---
title: "545. 二叉树的边界"
aliases: ["yiduobo的每日leetcode 545.二叉树的边界"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/600957850"
zhihu_id: "600957850"
zhihu_title: "yiduobo的每日leetcode 545.二叉树的边界"
question_id: "545"
question: "二叉树的边界"
problem_url: "https://leetcode.cn/problems/boundary-of-binary-tree/"
created: "2023-01-25T23:49:36+08:00"
updated: "2023-01-25T23:49:36+08:00"
upvotes: 0
comments: 0
---

# 545. 二叉树的边界

> **[yiduobo的每日leetcode 545.二叉树的边界](https://zhuanlan.zhihu.com/p/600957850) · 知乎 · 2023-01-25 · 赞同 0**
> 力扣：[545. 二叉树的边界](https://leetcode.cn/problems/boundary-of-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

545.二叉树的边界

[力扣](https://leetcode.cn/problems/boundary-of-binary-tree/)

根据题目的描述，二叉树的边界由根节点、左边界、逆序右边界以及叶节点组成。在这里需要得到从上向下顺序的左右边界，以及从左向右顺序的叶子结点。

由于右边界的定义方式与左边界完全对称，在这里只需要考虑左边界的求解方法，然后反过来就可以得到右边界的求解方法了。对于左边界的求解，若根节点root不存在左孩子，那么树的左边界就为空，否则就从root.left开始向下迭代。

接下来，对于当前处理的节点now，若now是叶子节点，那么就停止迭代。若now有左孩子或者右孩子，那么就需要将其加入到储存左边界的数组当中，然后检测now是否有左孩子。若有，就将now迭代为now.left，否则将now迭代为now.right，然后继续上面的操作，直到now是一个叶子节点为止。

对于右边界的求解则如法炮制，不同的地方在于now的初始值应该是root.right，另外在每次迭代时应该优先向右孩子这一侧迭代。

最后则是关于叶子节点的求解。由于题目需要从左到右的顺序，那么在这里可以执行一次先序遍历，将遍历到的叶子节点依次加入储存叶子结点的数组中即可。

求解完成后，将根节点，左边界，叶子节点，逆序右边界全部拼接起来，就得到了最终答案。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def boundaryOfBinaryTree(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """

        left = []
        right = []
        leaf = []

        if root.left:
            now = root.left
            while now.left or now.right:
                left.append(now.val)
                if now.left:
                    now = now.left
                else:
                    now = now.right
        
        if root.right:
            now = root.right
            while now.left or now.right:
                right.append(now.val)
                if now.right:
                    now = now.right
                else:
                    now = now.left
            right.reverse()

        def dfs(now):
            if not now.left and not now.right:
                if now != root:
                    leaf.append(now.val)
            else:
                if now.left:
                    dfs(now.left)
                if now.right:
                    dfs(now.right)
        
        dfs(root)
        return [root.val] + left + leaf + right
```
