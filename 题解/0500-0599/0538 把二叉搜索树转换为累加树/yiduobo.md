---
title: "538. 把二叉搜索树转换为累加树"
aliases: ["yiduobo的每日leetcode 538.把二叉搜索树转换为累加树"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261205202"
zhihu_id: "261205202"
zhihu_title: "yiduobo的每日leetcode 538.把二叉搜索树转换为累加树"
question_id: "538"
question: "把二叉搜索树转换为累加树"
problem_url: "https://leetcode.cn/problems/convert-bst-to-greater-tree/"
difficulty: "Medium"
rating: 1375
created: "2020-10-07T01:27:21+08:00"
updated: "2020-10-07T01:27:21+08:00"
upvotes: 1
comments: 0
---

# 538. 把二叉搜索树转换为累加树

> **[yiduobo的每日leetcode 538.把二叉搜索树转换为累加树](https://zhuanlan.zhihu.com/p/261205202) · 知乎 · 2020-10-07 · 赞同 1**
> 力扣：[538. 把二叉搜索树转换为累加树](https://leetcode.cn/problems/convert-bst-to-greater-tree/) · Medium · 灵茶山艾府：[简洁写法，利用二叉搜索树的性质（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

538.把二叉搜索树转换为累加树<https://leetcode-cn.com/problems/convert-bst-to-greater-tree/>

如果是对于一个数组做这个累加操作，一般做法就是先排序，然后从大到小依次进行累加。在这里，bst已经提供了有序性，那么我们接下来就只需要从最大的节点开始进行累加操作。

对于bst某个节点而言，其值必然大于左子树中的任意节点，且小于其右子树中的任意节点，因此可以优先递归求解右子树，返回整个右子树的累加和，然后将这个累加和加到当前节点上，再将加上累加和之后的当前节点值带到左子树的递归当中即可。

最后附上python代码，其中delta表示当前节点右侧的累加和：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def convertBST(self, root):
        """
        :type root: TreeNode
        :rtype: TreeNode
        """

        if not root:
            return root

        self.dfs(root, 0)
        return root

    def dfs(self, now, delta):
        if now.right:
            delta = self.dfs(now.right, delta)
        now.val += delta
        delta = now.val
        if now.left:
            delta = self.dfs(now.left, delta)
        return delta
```
