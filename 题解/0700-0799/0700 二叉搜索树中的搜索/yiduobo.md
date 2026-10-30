---
title: "700. 二叉搜索树中的搜索"
aliases: ["yiduobo的每日leetcode 700.二叉搜索树中的搜索"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/317616870"
zhihu_id: "317616870"
zhihu_title: "yiduobo的每日leetcode 700.二叉搜索树中的搜索"
question_id: "700"
question: "二叉搜索树中的搜索"
problem_url: "https://leetcode.cn/problems/search-in-a-binary-search-tree/"
created: "2020-11-28T15:23:54+08:00"
updated: "2020-11-28T15:23:54+08:00"
upvotes: 0
comments: 0
---

# 700. 二叉搜索树中的搜索

> **[yiduobo的每日leetcode 700.二叉搜索树中的搜索](https://zhuanlan.zhihu.com/p/317616870) · 知乎 · 2020-11-28 · 赞同 0**
> 力扣：[700. 二叉搜索树中的搜索](https://leetcode.cn/problems/search-in-a-binary-search-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

700.二叉搜索树中的搜索

[力扣](https://leetcode-cn.com/problems/search-in-a-binary-search-tree/)

根据二叉搜索树的定义，我们从根节点开始向下查找：

1、若now.val等于val，那么now就是我们要找的节点

2、若now.val小于val，说明now的左子树中所有的节点的值都小于val，因此我们需要在now的右子树now.right中继续查找

3、若now.val大于val，与情况2类似，我们需要在now的左子树now.left中继续查找

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def searchBST(self, root, val):
        """
        :type root: TreeNode
        :type val: int
        :rtype: TreeNode
        """

        now = root
        while now and now.val != val:
            if now.val < val:
                now = now.right
            else:
                now = now.left

        return now
```
