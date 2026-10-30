---
title: "1973. 值等于子节点之和的节点数量"
aliases: ["yiduobo的每日leetcode 1973.值等于子节点之和的节点数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/624347717"
zhihu_id: "624347717"
zhihu_title: "yiduobo的每日leetcode 1973.值等于子节点之和的节点数量"
question_id: "1973"
question: "值等于子节点之和的节点数量"
problem_url: "https://leetcode.cn/problems/count-nodes-equal-to-sum-of-descendants/"
created: "2023-04-24T00:18:10+08:00"
updated: "2023-04-24T00:18:10+08:00"
upvotes: 0
comments: 0
---

# 1973. 值等于子节点之和的节点数量

> **[yiduobo的每日leetcode 1973.值等于子节点之和的节点数量](https://zhuanlan.zhihu.com/p/624347717) · 知乎 · 2023-04-24 · 赞同 0**
> 力扣：[1973. 值等于子节点之和的节点数量](https://leetcode.cn/problems/count-nodes-equal-to-sum-of-descendants/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1973.值等于子节点之和的节点数量

[力扣](https://leetcode.cn/problems/count-nodes-equal-to-sum-of-descendants/)

非常经典的子树节点和问题，常见的做法是从根节点向下一趟dfs递归求解每个节点。

对于当前节点now，先递归求解now的左右孩子节点，并取得左右子树中所有节点值之和，若左右子树节点之和恰好等于now.val，那么就更新答案，然后将返回左右节点值之和再加上now.val提供给上层的节点使用。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def equalToDescendants(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: int
        """

        global res
        res = 0

        def dfs(now):
            s = 0
            if now.left:
                s += dfs(now.left)
            if now.right:
                s += dfs(now.right)
            
            global res
            if s == now.val:
                res += 1
            
            return s + now.val
        
        dfs(root)
        return res
```
