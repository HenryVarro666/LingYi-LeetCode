---
title: "3157. 找到具有最小和的树的层数"
aliases: ["yiduobo的每日leetcode 3157.找到具有最小和的树的层数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/704158311"
zhihu_id: "704158311"
zhihu_title: "yiduobo的每日leetcode 3157.找到具有最小和的树的层数"
question_id: "3157"
question: "找到具有最小和的树的层数"
problem_url: "https://leetcode.cn/problems/find-the-level-of-tree-with-minimum-sum/"
created: "2024-06-19T00:14:27+08:00"
updated: "2024-06-19T00:14:27+08:00"
upvotes: 0
comments: 0
---

# 3157. 找到具有最小和的树的层数

> **[yiduobo的每日leetcode 3157.找到具有最小和的树的层数](https://zhuanlan.zhihu.com/p/704158311) · 知乎 · 2024-06-19 · 赞同 0**
> 力扣：[3157. 找到具有最小和的树的层数](https://leetcode.cn/problems/find-the-level-of-tree-with-minimum-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3157.找到具有最小和的树的层数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-level-of-tree-with-minimum-sum/description/)

题目给出一颗节点具有权重的二叉树的树根root，要求找出其中层和最小且最低的层数是多少。

由于需要计算层和，那么在这里就可以从root开始向下进行层序遍历。每一轮只需一边计算当前层的层和并更新答案，一边将下一层节点加入到层序遍历的队列中。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def minimumLevel(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: int
        """

        head, tail = 0, 1
        q = [root]
        mi = root.val
        res = 1
        level = 1
        while head < tail:
            s = 0
            for now in q[head : tail]:
                s += now.val
                if now.left:
                    q.append(now.left)
                if now.right:
                    q.append(now.right)
            
            if s < mi:
                mi = s
                res = level

            head, tail = tail, len(q)
            level += 1
        
        return res
```
