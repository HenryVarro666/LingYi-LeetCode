---
title: "LCP 44. 开幕式焰火"
aliases: ["yiduobo的每日leetcode LCP44.开幕式焰火"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/tree", "leetcode/depth-first-search", "leetcode/hash-table", "leetcode/binary-tree", "leetcode/dfs", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/576322894"
zhihu_id: "576322894"
zhihu_title: "yiduobo的每日leetcode LCP44.开幕式焰火"
question_id: "LCP 44"
question: "开幕式焰火"
problem_url: "https://leetcode.cn/problems/sZ59z6/"
difficulty: "Easy"
created: "2022-10-23T02:36:38+08:00"
updated: "2022-10-23T02:36:38+08:00"
upvotes: 1
comments: 0
---

# LCP 44. 开幕式焰火

> **[yiduobo的每日leetcode LCP44.开幕式焰火](https://zhuanlan.zhihu.com/p/576322894) · 知乎 · 2022-10-23 · 赞同 1**
> 力扣：[LCP 44. 开幕式焰火](https://leetcode.cn/problems/sZ59z6/) · Easy · 灵茶山艾府：[二叉树 DFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP44.开幕式焰火

[力扣](https://leetcode.cn/problems/sZ59z6/)

直接bfs遍历整棵树，使用哈希表记录树中的所有节点值。遍历完成后，哈希表的长度即为最终答案。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
class Solution(object):
    def numColor(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        color_set = set()
        q = [root]
        head, tail = 0, 1
        while head < tail:
            now = q[head]
            color_set.add(now.val)
            head += 1
            if now.left:
                q.append(now.left)
                tail += 1
            if now.right:
                q.append(now.right)
                tail += 1
        
        return len(color_set)
```
