---
title: "236. 二叉树的最近公共祖先"
aliases: ["yiduobo的每日leetcode 236.二叉树的最近公共祖先"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/binary-tree", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/LeetCode-热题-100/二叉树", "题单/面试经典-150-题/二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/150375415"
zhihu_id: "150375415"
zhihu_title: "yiduobo的每日leetcode 236.二叉树的最近公共祖先"
question_id: "236"
question: "二叉树的最近公共祖先"
problem_url: "https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/"
difficulty: "Medium"
created: "2020-06-23T23:25:43+08:00"
updated: "2020-06-23T23:25:43+08:00"
upvotes: 0
comments: 0
---

# 236. 二叉树的最近公共祖先

> **[yiduobo的每日leetcode 236.二叉树的最近公共祖先](https://zhuanlan.zhihu.com/p/150375415) · 知乎 · 2020-06-23 · 赞同 0**
> 力扣：[236. 二叉树的最近公共祖先](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/) · Medium · 灵茶山艾府：[【视频讲解】简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

236.二叉树的最近公共祖先<https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-tree/>

上一题的升级版本，由于这里不再是bst，于是上一题的做法在这里不再适用。不过这里也只需要找到一组节点的最近公共祖先，于是也用不着使用标准做法来处理。

通过一次dfs或者bfs，我们可以很容易地获取到从root到p以及从root到q的路径上的所有节点，那么我们将root到p路径上的所有节点存到set中，然后反过来从q到root逐个节点遍历，若当前节点出现在set中，那么就是p和q的最近公共祖先了。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def lowestCommonAncestor(self, root, p, q):
        """
        :type root: TreeNode
        :type p: TreeNode
        :type q: TreeNode
        :rtype: TreeNode
        """

        father = {root:None}
        queue = [root]
        l = 0
        r = 1
        while l < r:
            now = queue[l]
            l += 1
            if now.left:
                father[now.left] = now
                queue.append(now.left)
                r += 1
            if now.right:
                father[now.right] = now
                queue.append(now.right)
                r += 1

        father_set = set()
        while p:
            father_set.add(p)
            p = father[p]

        while q not in father_set:
            q = father[q]

        return q
```
