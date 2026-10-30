---
title: "404. 左叶子之和"
aliases: ["yiduobo的每日leetcode 404.左叶子之和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/183980354"
zhihu_id: "183980354"
zhihu_title: "yiduobo的每日leetcode 404.左叶子之和"
question_id: "404"
question: "左叶子之和"
problem_url: "https://leetcode.cn/problems/sum-of-left-leaves/"
difficulty: "Easy"
created: "2020-08-14T23:43:30+08:00"
updated: "2020-08-14T23:43:30+08:00"
upvotes: 0
comments: 0
---

# 404. 左叶子之和

> **[yiduobo的每日leetcode 404.左叶子之和](https://zhuanlan.zhihu.com/p/183980354) · 知乎 · 2020-08-14 · 赞同 0**
> 力扣：[404. 左叶子之和](https://leetcode.cn/problems/sum-of-left-leaves/) · Easy · 灵茶山艾府：[两种 DFS 写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

404.左叶子之和<https://leetcode-cn.com/problems/sum-of-left-leaves/>

比较基础的题目。一趟dfs，在过程中标记当前节点是否为其父亲节点的左孩子。那么对于一个节点：

1、若该节点为空，那么返回0。

2、其没有孩子节点，且左孩子标记为True，说明其为左叶子节点，那么返回当前节点的值。

3、其没有孩子节点，且左孩子标记为False，说明其为右叶子节点，那么返回0。

4、若其有孩子节点，那么递归计算其左孩子和右孩子的值，然后返回二者之和。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def sumOfLeftLeaves(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        return self.dfs(root, False)

    def dfs(self, now, left_flag):
        if not now:
            return 0

        if not now.left and not now.right:
            if left_flag:
                return now.val
            else:
                return 0

        else:
            return self.dfs(now.left, True) + self.dfs(now.right, False)
```
