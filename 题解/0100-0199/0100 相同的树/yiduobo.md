---
title: "100. 相同的树"
aliases: ["yiduobo的每日leetcode 100.相同的树"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/面试经典-150-题/二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/137722119"
zhihu_id: "137722119"
zhihu_title: "yiduobo的每日leetcode 100.相同的树"
question_id: "100"
question: "相同的树"
problem_url: "https://leetcode.cn/problems/same-tree/"
difficulty: "Easy"
created: "2020-05-01T23:40:15+08:00"
updated: "2020-05-01T23:40:15+08:00"
upvotes: 0
comments: 0
---

# 100. 相同的树

> **[yiduobo的每日leetcode 100.相同的树](https://zhuanlan.zhihu.com/p/137722119) · 知乎 · 2020-05-01 · 赞同 0**
> 力扣：[100. 相同的树](https://leetcode.cn/problems/same-tree/) · Easy · 灵茶山艾府：[【视频】如何灵活运用递归？（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

100.相同的树<https://leetcode-cn.com/problems/same-tree/>

比较基础的题目。

对于两棵树，可以先比较二者根节点的值是否相同，然后递归地比较左子树和右子树即可。

过程中需要注意判断左子树或者右子树为空的情况。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def isSameTree(self, p, q):
        """
        :type p: TreeNode
        :type q: TreeNode
        :rtype: bool
        """

        if not p:
            if not q:
                return True
            else:
                return False
        elif not q:
            return False
        else:
            return self.check(p, q)

    def check(self, p, q):
        if p.val != q.val:
            return False

        if p.left:
            if not q.left or not self.check(p.left, q.left):
                return False
        else:
            if q.left:
                return False
        
        if p.right:
            if not q.right or not self.check(p.right, q.right):
                return False
        else:
            if q.right:
                return False

        return True
```
