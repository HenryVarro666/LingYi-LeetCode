---
title: "1214. 查找两颗二叉搜索树之和"
aliases: ["yiduobo的每日leetcode 1214.查找两颗二叉搜索树之和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/613234268"
zhihu_id: "613234268"
zhihu_title: "yiduobo的每日leetcode 1214.查找两颗二叉搜索树之和"
question_id: "1214"
question: "查找两颗二叉搜索树之和"
problem_url: "https://leetcode.cn/problems/two-sum-bsts/"
created: "2023-03-11T21:54:40+08:00"
updated: "2023-03-11T21:54:40+08:00"
upvotes: 0
comments: 0
---

# 1214. 查找两颗二叉搜索树之和

> **[yiduobo的每日leetcode 1214.查找两颗二叉搜索树之和](https://zhuanlan.zhihu.com/p/613234268) · 知乎 · 2023-03-11 · 赞同 0**
> 力扣：[1214. 查找两颗二叉搜索树之和](https://leetcode.cn/problems/two-sum-bsts/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1214.查找两颗二叉搜索树之和

[力扣](https://leetcode.cn/problems/two-sum-bsts/)

最直观的做法是对其中一棵树进行遍历，使用哈希表储存其中出现的所有节点值，接下来对另一棵树进行遍历，然后通过哈希表来判断哈希表中是否存在某个值与当前遍历到的值之和等于target。

不过上面的做法没有利用到二叉搜索树的性质，需要想办法将中序遍历运用起来。一种可行的做法是使用之前94题中修改左子树中最右侧节点的方式，使得通过迭代而不是递归来进行中序遍历成为可能。

[yiduobo：yiduobo的每日leetcode 94.二叉树的中序遍历](https://zhuanlan.zhihu.com/p/137080593)

不过需要注意的是，对于一棵树正序遍历的同时，应该对另一棵树进行倒序遍历，因此在修改第二棵树时应该针对右子树中最左侧的节点进行处理。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def twoSumBSTs(self, root1, root2, target):
        """
        :type root1: TreeNode
        :type root2: TreeNode
        :type target: int
        :rtype: bool
        """

        def maintainLeft():
            global p1

            while p1.left:
                rightest = p1.left
                while rightest.right:
                    rightest = rightest.right
            
                rightest.right = p1
                p1 = p1.left
                rightest.right.left = None
        
        def maintainRight():
            global p2

            while p2.right:
                leftest = p2.right
                while leftest.left:
                    leftest = leftest.left
            
                leftest.left = p2
                p2 = p2.right
                leftest.left.right = None
        

        global p1, p2
        p1 = root1
        p2 = root2
        maintainLeft()
        maintainRight()

        while p1 and p2:
            s = p1.val + p2.val
            if s == target:
                return True
            
            if s < target:
                p1 = p1.right
                if not p1:
                    break
                maintainLeft()
            else:
                p2 = p2.left
                if not p2:
                    break
                maintainRight()
        
        return False
```
