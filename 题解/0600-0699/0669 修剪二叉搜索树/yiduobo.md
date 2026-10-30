---
title: "669. 修剪二叉搜索树"
aliases: ["yiduobo的每日leetcode 669.修剪二叉搜索树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/293098417"
zhihu_id: "293098417"
zhihu_title: "yiduobo的每日leetcode 669.修剪二叉搜索树"
question_id: "669"
question: "修剪二叉搜索树"
problem_url: "https://leetcode.cn/problems/trim-a-binary-search-tree/"
created: "2020-11-14T13:08:22+08:00"
updated: "2020-11-14T13:08:22+08:00"
upvotes: 0
comments: 0
---

# 669. 修剪二叉搜索树

> **[yiduobo的每日leetcode 669.修剪二叉搜索树](https://zhuanlan.zhihu.com/p/293098417) · 知乎 · 2020-11-14 · 赞同 0**
> 力扣：[669. 修剪二叉搜索树](https://leetcode.cn/problems/trim-a-binary-search-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

669.修剪二叉搜索树

[力扣](https://leetcode-cn.com/problems/trim-a-binary-search-tree/)

题目要求树中的每个结点值都在low到high之间，那么对于结点node：

1、若node.val \< low，说明此时node应该被删除掉，同时由于node左子树中所有结点的值都必然小于node.val，因此node左子树也应该一起删除掉。于是此时直接将node的右孩子顶替到node的位置上即可

2、若node.val > high，与情况1类似，此时只需将node的左孩子顶替到node的位置上即可

3、若low \<\= node.val \<\= high，说明此时node本身是合法的结点，因此我们可以递归求解node的左子树和右子树。

注意到上面的求解过程中，有顶替这种操作，因此我们需要在递归时记录当前结点的父亲，然后在顶替操作发生时判断当前结点是父亲的左孩子还是右孩子。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def trimBST(self, root, low, high):
        """
        :type root: TreeNode
        :type low: int
        :type high: int
        :rtype: TreeNode
        """

        phead = TreeNode(left = root)
        self.cut(root, phead, low, high)

        return phead.left
    
    def cut(self, now, fa, low, high):
        if not now:
            return
            
        if now.val < low:
            if now == fa.left:
                fa.left = now.right
            else:
                fa.right = now.right

            self.cut(now.right, fa, low, high)

        elif now.val > high:
            if now == fa.left:
                fa.left = now.left
            else:
                fa.right = now.left

            self.cut(now.left, fa, low, high)

        else:
            self.cut(now.left, now, low, high)
            self.cut(now.right, now, low, high)
```
