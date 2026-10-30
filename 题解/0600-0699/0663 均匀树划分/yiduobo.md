---
title: "663. 均匀树划分"
aliases: ["yiduobo的每日leetcode 663.均匀树划分"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/603547360"
zhihu_id: "603547360"
zhihu_title: "yiduobo的每日leetcode 663.均匀树划分"
question_id: "663"
question: "均匀树划分"
problem_url: "https://leetcode.cn/problems/equal-tree-partition/"
created: "2023-02-04T23:52:01+08:00"
updated: "2023-02-04T23:52:01+08:00"
upvotes: 0
comments: 0
---

# 663. 均匀树划分

> **[yiduobo的每日leetcode 663.均匀树划分](https://zhuanlan.zhihu.com/p/603547360) · 知乎 · 2023-02-04 · 赞同 0**
> 力扣：[663. 均匀树划分](https://leetcode.cn/problems/equal-tree-partition/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

663.均匀树划分

[力扣](https://leetcode.cn/problems/equal-tree-partition/)

题目要求找出一条边，将这条边从树中删除后剩下两个部分节点值之和相等。

对于这条边，其两端的节点在原树中必然是父子关系，对于孩子的那一端，在删除这条边之后剩下的必然是一颗完整的子树，那么问题就可以转化为给出一棵树，问是否存在某个子树的节点之和恰好等于整棵树节点之和的一半。需要特别注意的是，这颗子树的根节点不能是原树的根节点，因为在最开始的假设中这颗子树的根节点是删除的边另一端的孩子节点。

有了这个结论，就可以从根节点向下进行dfs，计算每棵子树中所有节点之和，并在过程中使用一个哈希表记录所有出现过的和。需要注意不要记录原树的和。

dfs完成后，若树中所有节点之和为偶数，且这个值除以2出现在哈希表中，那么就返回true，否则返回false。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def checkEqualTree(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """

        sum_set = set()

        def dfs(now):
            s = now.val
            if now.left:
                s += dfs(now.left)
            if now.right:
                s += dfs(now.right)
            
            if now != root:
                sum_set.add(s)
            return s
        
        tot_s = dfs(root)
        return tot_s % 2 == 0 and tot_s / 2 in sum_set
```
