---
title: "110. 平衡二叉树"
aliases: ["yiduobo的每日leetcode 110.平衡二叉树"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/138537841"
zhihu_id: "138537841"
zhihu_title: "yiduobo的每日leetcode 110.平衡二叉树"
question_id: "110"
question: "平衡二叉树"
problem_url: "https://leetcode.cn/problems/balanced-binary-tree/"
difficulty: "Easy"
created: "2020-05-06T17:55:32+08:00"
updated: "2020-05-06T17:55:32+08:00"
upvotes: 1
comments: 0
---

# 110. 平衡二叉树

> **[yiduobo的每日leetcode 110.平衡二叉树](https://zhuanlan.zhihu.com/p/138537841) · 知乎 · 2020-05-06 · 赞同 1**
> 力扣：[110. 平衡二叉树](https://leetcode.cn/problems/balanced-binary-tree/) · Easy · 灵茶山艾府：[【视频】如何灵活运用递归？（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

110.平衡二叉树<https://leetcode-cn.com/problems/balanced-binary-tree/>

比较基础的题目。先分别递归求解左右子树是否满足平衡的条件，同时在求解过程中计算左右子树各自的高度。接下来比较左右子树的高度差是否在1以内，并将较高的那一边加一作为当前树的高度返回。

方便起见，我在实现的时候约定如果不平衡，则返回-1，否则返回树的高度。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def isBalanced(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """

        return self.check(root) >= 0

    def check(self, now):
        if now is None:
            return 0

        left_height = 0
        if now.left:
            left_height = self.check(now.left)

        right_height = 0
        if now.right:
            right_height = self.check(now.right)
        
        if left_height < 0 or right_height < 0 or abs(left_height - right_height) > 1:
            return -1

        return max(left_height, right_height) + 1
```
