---
title: "987. 二叉树的垂序遍历"
aliases: ["yiduobo的每日leetcode 987.二叉树的垂序遍历"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/array", "leetcode/hash-table", "leetcode/ordered-set", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/363949551"
zhihu_id: "363949551"
zhihu_title: "yiduobo的每日leetcode 987.二叉树的垂序遍历"
question_id: "987"
question: "二叉树的垂序遍历"
problem_url: "https://leetcode.cn/problems/vertical-order-traversal-of-a-binary-tree/"
difficulty: "Hard"
rating: 1676
created: "2021-04-11T15:06:41+08:00"
updated: "2021-04-11T15:06:41+08:00"
upvotes: 0
comments: 0
---

# 987. 二叉树的垂序遍历

> **[yiduobo的每日leetcode 987.二叉树的垂序遍历](https://zhuanlan.zhihu.com/p/363949551) · 知乎 · 2021-04-11 · 赞同 0**
> 力扣：[987. 二叉树的垂序遍历](https://leetcode.cn/problems/vertical-order-traversal-of-a-binary-tree/) · Hard · 灵茶山艾府：[四种写法：DFS+哈希表/双数组/单数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

987.二叉树的垂序遍历

[力扣](https://leetcode-cn.com/problems/vertical-order-traversal-of-a-binary-tree/)

直接按照题目意思带着行和列的信息对树进行一趟dfs，在dfs过程中使用一个dict记录下来当前所处的列和行有哪些节点。

设当前处理到的节点位于第row行第col列，那么其左孩子就位于第row + 1行，第col - 1列，而其右孩子则位于第row + 1行，第col + 1列。

由于最终是按列输出，因此dict的一级key为列，二级key为行。

dfs完成后，先按列排序，然后按行排序，最后按当前列、行中节点的大小排序然后输出到答案中即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def verticalTraversal(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """

        num_dict = {}
        self.dfs(root, 0, 0, num_dict)
    
        res = []
        for col in sorted(num_dict.keys()):
            res.append([])
            for row in sorted(num_dict[col].keys()):
                res[-1].extend(sorted(num_dict[col][row]))
        
        return res

    def dfs(self, now, row, col, num_dict):
        if col not in num_dict:
            num_dict[col] = {}
        
        if row not in num_dict[col]:
            num_dict[col][row] = []
        
        num_dict[col][row].append(now.val)
    
        if now.left:
            self.dfs(now.left, row + 1, col - 1, num_dict)
        
        if now.right:
            self.dfs(now.right, row + 1, col + 1, num_dict)
```
