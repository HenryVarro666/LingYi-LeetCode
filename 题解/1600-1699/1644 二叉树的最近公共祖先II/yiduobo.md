---
title: "1644. 二叉树的最近公共祖先II"
aliases: ["yiduobo的每日leetcode 1644.二叉树的最近公共祖先II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/619223621"
zhihu_id: "619223621"
zhihu_title: "yiduobo的每日leetcode 1644.二叉树的最近公共祖先II"
question_id: "1644"
question: "二叉树的最近公共祖先II"
problem_url: "https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree-ii/"
created: "2023-04-03T22:28:57+08:00"
updated: "2023-04-03T22:28:57+08:00"
upvotes: 0
comments: 0
---

# 1644. 二叉树的最近公共祖先II

> **[yiduobo的每日leetcode 1644.二叉树的最近公共祖先II](https://zhuanlan.zhihu.com/p/619223621) · 知乎 · 2023-04-03 · 赞同 0**
> 力扣：[1644. 二叉树的最近公共祖先II](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1644.二叉树的最近公共祖先II

[力扣](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree-ii/)

题目中的节点只有左右孩子指针，但没有父亲节点指针，因此在这里就只能从根节点自顶向下来进行求解。

对于以now为根节点的子树，若子树中存在p和q，那么说明now是p和q的一个公共祖先。对于这些公共祖先，其中深度最深的就是答案要求的最近公共祖先。

综合自顶向下、子树的求解以及深度最深这三个因素，在这里就很适合从root开始向下dfs求解。如果在求解过程中首次出现某棵子树中同时存在p和q，这颗子树的根节点就是最终答案，理由是求解的方式是dfs，因此当前找到的就是深度最深的公共祖先。

具体实现上，就是从root开始向下dfs。对于当前处理的节点now，使用一个变量cnt记录当前子树中命中p或q的数量。接下来，若当前求解过程还没有找到最终答案，那么就递归求解now的左右孩子，根据左右子树中命中p或q的数量来更新cnt。另外，若now自身是p或q之一，那么也应该将cnt加上1。若最终的cnt等于2，且当前还没有找到答案，那么答案就是当前节点now。

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

        global res
        res = None

        def dfs(now):
            global res

            cnt = 0

            if res is None and now.left:
                cnt += dfs(now.left)
            
            if res is None and now.right:
                cnt += dfs(now.right)
            
            if now == p or now == q:
                cnt += 1
            
            if res is None and cnt == 2:
                res = now

            return cnt

        dfs(root)
        return res
```
