---
title: "1676. 二叉树的最近公共祖先IV"
aliases: ["yiduobo的每日leetcode 1676.二叉树的最近公共祖先IV"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/619657793"
zhihu_id: "619657793"
zhihu_title: "yiduobo的每日leetcode 1676.二叉树的最近公共祖先IV"
question_id: "1676"
question: "二叉树的最近公共祖先IV"
problem_url: "https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree-iv/"
created: "2023-04-05T19:24:24+08:00"
updated: "2023-04-05T19:24:24+08:00"
upvotes: 0
comments: 0
---

# 1676. 二叉树的最近公共祖先IV

> **[yiduobo的每日leetcode 1676.二叉树的最近公共祖先IV](https://zhuanlan.zhihu.com/p/619657793) · 知乎 · 2023-04-05 · 赞同 0**
> 力扣：[1676. 二叉树的最近公共祖先IV](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree-iv/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1676.二叉树的最近公共祖先IV

[力扣](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree-iv/)

本题与之前的版本II类似，不同之处是本题要找的是多个节点的最近公共祖先，而版本II中的是找两个节点的最近公共祖先，不过依然可以沿用之前的处理方法。

[yiduobo：yiduobo的每日leetcode 1644.二叉树的最近公共祖先II](https://zhuanlan.zhihu.com/p/619223621)

从根节点向下进行dfs，计算当前子树内命中目标节点的数目，而其中最深的且命中了所有目标节点的子树树根即为最终答案。对于判断是否命中目标节点，则可以利用题设中的val互不相同这个条件，利用哈希表来辅助判断。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def lowestCommonAncestor(self, root, nodes):
        """
        :type root: TreeNode
        :type nodes: List[TreeNode]
        """

        global res
        res = None

        v_set = set()
        for node in nodes:
            v_set.add(node.val)
        

        def dfs(now):
            global res

            cnt = 0
            if res is None and now.left:
                cnt += dfs(now.left)
            
            if res is None and now.right:
                cnt += dfs(now.right)
            
            if now.val in v_set:
                cnt += 1
            
            if res is None and len(v_set) == cnt:
                res = now
            
            return cnt
            

        dfs(root)
        return res
```
