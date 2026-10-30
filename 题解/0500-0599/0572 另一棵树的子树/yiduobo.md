---
title: "572. 另一个树的子树"
aliases: ["yiduobo的每日leetcode 572.另一个树的子树"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/binary-tree", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/266579796"
zhihu_id: "266579796"
zhihu_title: "yiduobo的每日leetcode 572.另一个树的子树"
question_id: "572"
question: "另一棵树的子树"
problem_url: "https://leetcode.cn/problems/subtree-of-another-tree/"
difficulty: "Easy"
created: "2020-10-18T15:59:05+08:00"
updated: "2020-10-18T15:59:05+08:00"
upvotes: 0
comments: 0
---

# 572. 另一个树的子树

> **[yiduobo的每日leetcode 572.另一个树的子树](https://zhuanlan.zhihu.com/p/266579796) · 知乎 · 2020-10-18 · 赞同 0**
> 力扣：[572. 另一棵树的子树](https://leetcode.cn/problems/subtree-of-another-tree/) · Easy · 灵茶山艾府：[从 O(nm) 到 O(n+m)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

572.另一个树的子树<https://leetcode-cn.com/problems/subtree-of-another-tree/>

对于一棵树而言，可以通过前序遍历及中序遍历确定其形态。这里需要中序遍历的原因是前序遍历中不包含空节点，无法确定前序遍历中两个相邻节点是何种关系，而如果通过前序遍历求出的一段dfs序包含了空节点，那么就可以通过这段dfs序确定树的形态。需要注意的是，这里的空节点还必须区分左右。

由于一棵树的子树其dfs序在整棵树的dfs序中是连续的，因此在这里可以按前序遍历的顺序对s和t分别求出其包含空节点的dfs序，然后若t的dfs序是s的dfs序的子序列，那么就说明t是s的子树。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def isSubtree(self, s, t):
        """
        :type s: TreeNode
        :type t: TreeNode
        :rtype: bool
        """

        s_list = self.dfs(s)
        t_list = self.dfs(t)
        
        m = len(s_list)
        n = len(t_list)

        pos = 0
        f = [0]
        for index in range(1, n):
            while pos > 0 and t_list[pos] != t_list[index]:
                pos = f[pos - 1]
            if t_list[pos] == t_list[index]:
                pos += 1
            f.append(pos)

        pos = 0
        for index in range(m):
            while pos > 0 and t_list[pos] != s_list[index]:
                pos = f[pos - 1]
            if t_list[pos] == s_list[index]:
                pos += 1
            if pos == n:
                return True

        return False

    def dfs(self, now):
        ret = [str(now.val)]
        if now.left:
            ret.extend(self.dfs(now.left))
        else:
            ret.append('#')
        if now.right:
            ret.extend(self.dfs(now.right))
        else:
            ret.append('$')
        
        return ret
```
