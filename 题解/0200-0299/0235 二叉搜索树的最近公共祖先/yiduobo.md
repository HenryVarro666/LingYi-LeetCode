---
title: "235. 二叉搜索树的最近公共祖先"
aliases: ["yiduobo的每日leetcode 235.二叉搜索树的最近公共祖先"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/150374215"
zhihu_id: "150374215"
zhihu_title: "yiduobo的每日leetcode 235.二叉搜索树的最近公共祖先"
question_id: "235"
question: "二叉搜索树的最近公共祖先"
problem_url: "https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-search-tree/"
difficulty: "Medium"
created: "2020-06-23T23:21:47+08:00"
updated: "2020-06-23T23:21:47+08:00"
upvotes: 0
comments: 0
---

# 235. 二叉搜索树的最近公共祖先

> **[yiduobo的每日leetcode 235.二叉搜索树的最近公共祖先](https://zhuanlan.zhihu.com/p/150374215) · 知乎 · 2020-06-23 · 赞同 0**
> 力扣：[235. 二叉搜索树的最近公共祖先](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-search-tree/) · Medium · 灵茶山艾府：[【视频】分类讨论乱如麻？一个视频讲透！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

235.二叉搜索树的最近公共祖先<https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-search-tree/>

最近公共祖先(LCA)问题是二叉树的经典问题之一，一般的做法是先dfs获得搜索序列，然后将LCA问题转化为RMQ问题，使用线段树或者st来求解。使用tarjan算法也是经典的处理方法。

在这里，只需要找一组节点的最近公共祖先，且限制在bst内，于是有了优化的空间。

注意到bst满足对于任意节点，其左边的节点的val小于该节点的val，而其右边节点的val大于该节点的val，于是我们可以从根节点开始往下找，若当前节点now的值处于节点p和节点q的值的中间，说明p和q分别位于now的左子树和右子树上，即now就是要求的最近公共祖先。否则的话，p和q为与now的同一侧，那么将now迭代到对应的子树继续上面的判断即可。

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

        now = root
        while now:
            if now.val < p.val and now.val < q.val:
                now = now.right
            elif now.val > p.val and now.val > q.val:
                now = now.left
            else:
                return now
```
