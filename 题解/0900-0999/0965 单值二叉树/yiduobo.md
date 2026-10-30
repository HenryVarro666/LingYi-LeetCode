---
title: "965. 单值二叉树"
aliases: ["yiduobo的每日leetcode 965.单值二叉树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/361446054"
zhihu_id: "361446054"
zhihu_title: "yiduobo的每日leetcode 965.单值二叉树"
question_id: "965"
question: "单值二叉树"
problem_url: "https://leetcode.cn/problems/univalued-binary-tree/"
created: "2021-03-31T23:29:34+08:00"
updated: "2021-03-31T23:29:34+08:00"
upvotes: 0
comments: 0
---

# 965. 单值二叉树

> **[yiduobo的每日leetcode 965.单值二叉树](https://zhuanlan.zhihu.com/p/361446054) · 知乎 · 2021-03-31 · 赞同 0**
> 力扣：[965. 单值二叉树](https://leetcode.cn/problems/univalued-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

965.单值二叉树

[力扣](https://leetcode-cn.com/problems/univalued-binary-tree/)

直接对树进行dfs，对于每个节点，若其存在孩子节点那么就判断孩子节点的值是否与该节点的值一致即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def isUnivalTree(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """

        return self.dfs(root)
    
    def dfs(self, now):
        if now.left:
            if now.left.val != now.val or (not self.dfs(now.left)):
                return False
        
        if now.right:
            if now.right.val != now.val or (not self.dfs(now.right)):
                return False
            
        return True
```
