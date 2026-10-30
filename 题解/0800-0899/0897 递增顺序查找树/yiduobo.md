---
title: "897. 递增顺序查找树"
aliases: ["yiduobo的每日leetcode 897.递增顺序查找树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/352980692"
zhihu_id: "352980692"
zhihu_title: "yiduobo的每日leetcode 897.递增顺序查找树"
question_id: "897"
question: "递增顺序查找树"
problem_url: "https://leetcode.cn/problems/increasing-order-search-tree/"
created: "2021-02-25T22:24:39+08:00"
updated: "2021-02-25T22:24:39+08:00"
upvotes: 0
comments: 0
---

# 897. 递增顺序查找树

> **[yiduobo的每日leetcode 897.递增顺序查找树](https://zhuanlan.zhihu.com/p/352980692) · 知乎 · 2021-02-25 · 赞同 0**
> 力扣：[897. 递增顺序查找树](https://leetcode.cn/problems/increasing-order-search-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

897.递增顺序查找树

[力扣](https://leetcode-cn.com/problems/increasing-order-search-tree/)

可以直接在中序遍历时修改树的结构，但是有更简单的做法就是使用一个变量p表示当前答案中最右侧的节点，然后对原树执行中序遍历，设目前执行到节点now，根据中序遍历左-根-右的顺序可以得到如下做法：

1、若now有左孩子，则递归求解now.left

2、新建值为now.val的节点，同时将p.right指向该节点，然后将p置为p.right

3、若now有右孩子，则递归求解now.right

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def increasingBST(self, root):
        """
        :type root: TreeNode
        :rtype: TreeNode
        """

        self.ans = TreeNode(0)
        p_root = self.ans
        self.dfs(root)
        return p_root.right
    
    def dfs(self, now):
        if now.left:
            self.dfs(now.left)
        self.ans.right = TreeNode(now.val)
        self.ans = self.ans.right
        if now.right:
            self.dfs(now.right)
```
