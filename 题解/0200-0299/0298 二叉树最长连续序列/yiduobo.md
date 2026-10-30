---
title: "298. 二叉树最长连续序列"
aliases: ["yiduobo的每日leetcode 298.二叉树最长连续序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/595579390"
zhihu_id: "595579390"
zhihu_title: "yiduobo的每日leetcode 298.二叉树最长连续序列"
question_id: "298"
question: "二叉树最长连续序列"
problem_url: "https://leetcode.cn/problems/binary-tree-longest-consecutive-sequence/"
created: "2022-12-30T21:48:01+08:00"
updated: "2022-12-30T21:48:01+08:00"
upvotes: 0
comments: 0
---

# 298. 二叉树最长连续序列

> **[yiduobo的每日leetcode 298.二叉树最长连续序列](https://zhuanlan.zhihu.com/p/595579390) · 知乎 · 2022-12-30 · 赞同 0**
> 力扣：[298. 二叉树最长连续序列](https://leetcode.cn/problems/binary-tree-longest-consecutive-sequence/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

298.二叉树最长连续序列

[力扣](https://leetcode.cn/problems/binary-tree-longest-consecutive-sequence/)

对于这类问题，通常的做法是利用递归求解。

对于当前节点now，不妨先递归求解其左右子树，分别得到以now.left和now.right为起点的连续序列的长度，记为left_v和right_v。

若now.val加上1之后恰好等于now.left.val，那么就可以将now作为新的起点接在以now.left为起点的连续序列的头部。同样地，若now.val加上1之后恰好等于now.right.val，那么也可以将now作为新的起点接在以now.right为起点的连续序列的头部。接下来只需要根据具体情况就可以求解出以now为起点的连续序列的长度了，使用这个长度更新最终答案，同时返回给now的父亲节点使用。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def longestConsecutive(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        global res
        res = 0

        def dfs(now):
            global res

            v = 1
            if now.left:
                left_v = dfs(now.left)
                if now.left.val == now.val + 1:
                    v = max(v, left_v + 1)
            
            if now.right:
                right_v = dfs(now.right)
                if now.right.val == now.val + 1:
                    v = max(v, right_v + 1)

            res = max(res, v)
            return v
        
        dfs(root)
        return res
```
