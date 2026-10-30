---
title: "1305. 两棵二叉搜索树中的所有元素"
aliases: ["yiduobo的每日leetcode 1305.两棵二叉搜索树中的所有元素"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/391582406"
zhihu_id: "391582406"
zhihu_title: "yiduobo的每日leetcode 1305.两棵二叉搜索树中的所有元素"
question_id: "1305"
question: "两棵二叉搜索树中的所有元素"
problem_url: "https://leetcode.cn/problems/all-elements-in-two-binary-search-trees/"
created: "2021-07-20T22:16:10+08:00"
updated: "2021-07-20T22:16:10+08:00"
upvotes: 0
comments: 0
---

# 1305. 两棵二叉搜索树中的所有元素

> **[yiduobo的每日leetcode 1305.两棵二叉搜索树中的所有元素](https://zhuanlan.zhihu.com/p/391582406) · 知乎 · 2021-07-20 · 赞同 0**
> 力扣：[1305. 两棵二叉搜索树中的所有元素](https://leetcode.cn/problems/all-elements-in-two-binary-search-trees/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1305.两棵二叉搜索树中的所有元素

[力扣](https://leetcode-cn.com/problems/all-elements-in-two-binary-search-trees/)

题目要求将两棵二叉搜索树中的所有元素按升序排列，由于二叉搜索树的中序遍历是天然按升序排列的，那么一个自然的想法就是分别对两棵树执行中序遍历，就可以得到两个升序的数组。接下来对这两个数组执行二路归并即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def getAllElements(self, root1, root2):
        """
        :type root1: TreeNode
        :type root2: TreeNode
        :rtype: List[int]
        """

        arr1 = []
        arr2 = []
        self.dfs(root1, arr1)
        self.dfs(root2, arr2)
        res = []
        i = 0
        j = 0
        while i < len(arr1) and j < len(arr2):
            if arr1[i] < arr2[j]:
                res.append(arr1[i])
                i += 1
            else:
                res.append(arr2[j])
                j += 1
        
        if i < len(arr1):
            res.extend(arr1[i:])
        else:
            res.extend(arr2[j:])
        
        return res
    
    def dfs(self, now, arr):
        if not now:
            return
        self.dfs(now.left, arr)
        arr.append(now.val)
        self.dfs(now.right, arr)
```
