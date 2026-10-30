---
title: "1379. 找出克隆二叉树中的相同节点"
aliases: ["yiduobo的每日leetcode 1379.找出克隆二叉树中的相同节点"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/401972672"
zhihu_id: "401972672"
zhihu_title: "yiduobo的每日leetcode 1379.找出克隆二叉树中的相同节点"
question_id: "1379"
question: "找出克隆二叉树中的相同节点"
problem_url: "https://leetcode.cn/problems/find-a-corresponding-node-of-a-binary-tree-in-a-clone-of-that-tree/"
difficulty: "Easy"
created: "2021-08-20T23:06:28+08:00"
updated: "2021-08-20T23:06:28+08:00"
upvotes: 0
comments: 0
---

# 1379. 找出克隆二叉树中的相同节点

> **[yiduobo的每日leetcode 1379.找出克隆二叉树中的相同节点](https://zhuanlan.zhihu.com/p/401972672) · 知乎 · 2021-08-20 · 赞同 0**
> 力扣：[1379. 找出克隆二叉树中的相同节点](https://leetcode.cn/problems/find-a-corresponding-node-of-a-binary-tree-in-a-clone-of-that-tree/) · Easy · 灵茶山艾府：[简洁写法（Python/Java/C++/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1379.找出克隆二叉树中的相同节点

[力扣](https://leetcode-cn.com/problems/find-a-corresponding-node-of-a-binary-tree-in-a-clone-of-that-tree/)

若original就是target，那么直接返回cloned即可，否则我们从cloned开始进行bfs。由于树中每个节点的值都不一样，因此只要在bfs过程中遇到一个值等于target.val的节点，那么该节点就是最终答案，返回该节点即可。

进阶中提到了可能出现重复节点值的情况，那么我们可以两棵树同步进行bfs。若某一时刻在原树中遇到了target，那么此时遍历到的cloned树中的节点就是答案。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def getTargetCopy(self, original, cloned, target):
        """
        :type original: TreeNode
        :type cloned: TreeNode
        :type target: TreeNode
        :rtype: TreeNode
        """

        if original == target:
            return cloned

        q = [cloned]
        l = 0
        r = 1
        while l < r:
            now = q[l]
            l += 1
            if now.left:
                q.append(now.left)
                r += 1
                if now.left.val == target.val:
                    return q[-1]
            
            if now.right:
                q.append(now.right)
                r += 1
                if now.right.val == target.val:
                    return q[-1]
```
