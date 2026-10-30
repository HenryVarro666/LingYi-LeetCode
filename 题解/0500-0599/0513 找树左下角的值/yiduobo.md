---
title: "513. 找树左下角的值"
aliases: ["yiduobo的每日leetcode 513.找树左下角的值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/queue", "leetcode/binary-tree", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/259888221"
zhihu_id: "259888221"
zhihu_title: "yiduobo的每日leetcode 513.找树左下角的值"
question_id: "513"
question: "找树左下角的值"
problem_url: "https://leetcode.cn/problems/find-bottom-left-tree-value/"
difficulty: "Medium"
created: "2020-09-27T21:22:39+08:00"
updated: "2020-09-27T21:22:39+08:00"
upvotes: 0
comments: 0
---

# 513. 找树左下角的值

> **[yiduobo的每日leetcode 513.找树左下角的值](https://zhuanlan.zhihu.com/p/259888221) · 知乎 · 2020-09-27 · 赞同 0**
> 力扣：[513. 找树左下角的值](https://leetcode.cn/problems/find-bottom-left-tree-value/) · Medium · 灵茶山艾府：[【视频讲解】简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

513.找树左下角的值<https://leetcode-cn.com/problems/find-bottom-left-tree-value/>

对于一颗树而言，求解其左下角的值可以对树的根节点root分成这几种情况进行讨论：

1、若root既没有左孩子也没有右孩子，那么左下角节点就是root本身。

2、若root缺失一侧的孩子，那么左下角节点必然位于另一侧的子树中。

3、若root同时具有左孩子和右孩子，那么对比左子树和右子树的深度。若左子树的深度大于等于右子树的深度，那么左下角节点必然位于左子树中，否则位于右子树中。

我们可以从整棵树的根节点开始，带着深度往下进行dfs。对于当前节点now，判断其属于上面哪种情况，有必要的话就将当前深度加一，然后递归求解其子树左下角的值，最后得到以now为根节点的子树左下角的值。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def findBottomLeftValue(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        return self.dfs(root, 1)[0]

    def dfs(self, now, depth):
        if not now.left:
            if not now.right:
                return now.val, depth
            else:
                return self.dfs(now.right, depth + 1)
        else:
            if not now.right:
                return self.dfs(now.left, depth + 1)
            else:
                left_val, left_depth = self.dfs(now.left, depth + 1)
                right_val, right_depth = self.dfs(now.right, depth + 1)
                if left_depth >= right_depth:
                    return left_val, left_depth
                else:
                    return right_val, right_depth
```
