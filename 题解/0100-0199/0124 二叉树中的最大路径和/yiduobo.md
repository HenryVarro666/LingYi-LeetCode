---
title: "124. 二叉树中的最大路径和"
aliases: ["yiduobo的每日leetcode 124.二叉树中的最大路径和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/dynamic-programming", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/动态规划/十二-树形-DP", "题单/LeetCode-热题-100/二叉树", "题单/面试经典-150-题/二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/140056374"
zhihu_id: "140056374"
zhihu_title: "yiduobo的每日leetcode 124.二叉树中的最大路径和"
question_id: "124"
question: "二叉树中的最大路径和"
problem_url: "https://leetcode.cn/problems/binary-tree-maximum-path-sum/"
difficulty: "Hard"
created: "2020-05-12T21:55:32+08:00"
updated: "2020-05-12T21:55:32+08:00"
upvotes: 0
comments: 0
---

# 124. 二叉树中的最大路径和

> **[yiduobo的每日leetcode 124.二叉树中的最大路径和](https://zhuanlan.zhihu.com/p/140056374) · 知乎 · 2020-05-12 · 赞同 0**
> 力扣：[124. 二叉树中的最大路径和](https://leetcode.cn/problems/binary-tree-maximum-path-sum/) · Hard · 灵茶山艾府：[【视频】彻底掌握直径 DP！从二叉树到一般树！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

124.二叉树中的最大路径和<https://leetcode-cn.com/problems/binary-tree-maximum-path-sum/>

可以理解成动态规划。

首先，对于题目要求的这条路径，这条路径的形式一定是某棵子树的root，以及root连接起来的左子树中包含root.left的路径和右子树中的包含root.right的路径。当然，左右子树中的这两条路径都是可以为空的。

样例一中，就是整棵树。

样例二中，则是以20为root的子树。

接下来，我们只需要想办法求出以root的其中一端的最优路径值即可。我们可以定义f[p]表示以p为根的子树中，以p为端点的最大路径值是多少。

对于一个节点p，其作为路径的一端，那么这条路径的下一个节点可能是p.left或者p.right，即以p.left或者p.right为一端的最优路径，再加上p形成的。于是我们可以先递归求解f[p.left]与f[p.right]，然后通过f[p.left]与f[p.right]得到f[p]。当然，若f[p.left]或f[p.right]小于0，那么对应的那一侧路径不应该加入到以p为端点的路径中。具体的转移方程为：

f[p] \= max(f[p.left], f[p.right], 0) + p.val

在计算f[p]的同时，通过f[p.left]与f[p.right]配合p.val来形成题目要求的路径。当然，若f[p.left]或f[p.right]小于0，那么对应的那一侧路径就是空的，即：

res \= max(res, max(f[p.left], 0) + max(f[p.right, 0) + p.val)

另外，由于每个节点的f值只计算一次，而且只会用来更新其父亲节点，于是不需要维护整个f，在递归过程中传递这个值就行了。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def maxPathSum(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        self.res = root.val
        self.dfs(root)
        return self.res

    def dfs(self, now):
        if not now:
            return 0
        
        max_left = self.dfs(now.left)
        max_right = self.dfs(now.right)

        self.res = max(self.res, now.val + max(max_left, 0) + max(max_right, 0))
        return max(max_left, max_right, 0) + now.val
```
