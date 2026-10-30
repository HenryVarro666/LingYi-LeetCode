---
title: "617. 合并二叉树"
aliases: ["yiduobo的每日leetcode 617.合并二叉树"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/binary-tree", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/269295471"
zhihu_id: "269295471"
zhihu_title: "yiduobo的每日leetcode 617.合并二叉树"
question_id: "617"
question: "合并二叉树"
problem_url: "https://leetcode.cn/problems/merge-two-binary-trees/"
difficulty: "Easy"
created: "2020-10-27T23:18:00+08:00"
updated: "2020-10-27T23:18:00+08:00"
upvotes: 0
comments: 0
---

# 617. 合并二叉树

> **[yiduobo的每日leetcode 617.合并二叉树](https://zhuanlan.zhihu.com/p/269295471) · 知乎 · 2020-10-27 · 赞同 0**
> 力扣：[617. 合并二叉树](https://leetcode.cn/problems/merge-two-binary-trees/) · Easy · 灵茶山艾府：[【视频】看到递归就晕？带你理解递归的本质！附题单（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

617.合并二叉树<https://leetcode-cn.com/problems/merge-two-binary-trees/>

比价基础的题目。从根节点开始合并两颗二叉树：

1、若当前t1为空，那么合并结果就是t2

2、若当前t2位空，那么合并结果就是t1

3、否则设置合并结果节点的值为t1.val + t2.val，然后递归求解左右子树

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def mergeTrees(self, t1, t2):
        """
        :type t1: TreeNode
        :type t2: TreeNode
        :rtype: TreeNode
        """

        return self.dfs(t1, t2)

    def dfs(self, t1, t2):
        if t1 is None:
            return t2
        
        if t2 is None:
            return t1

        tmp = TreeNode(t1.val + t2.val)
        tmp.left = self.dfs(t1.left, t2.left)
        tmp.right = self.dfs(t1.right, t2.right)
        return tmp
```
