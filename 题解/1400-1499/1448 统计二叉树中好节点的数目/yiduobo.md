---
title: "1448. 统计二叉树中好节点的数目"
aliases: ["yiduobo的每日leetcode 1448.统计二叉树中好节点的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/411190702"
zhihu_id: "411190702"
zhihu_title: "yiduobo的每日leetcode 1448.统计二叉树中好节点的数目"
question_id: "1448"
question: "统计二叉树中好节点的数目"
problem_url: "https://leetcode.cn/problems/count-good-nodes-in-binary-tree/"
difficulty: "Medium"
rating: 1360
created: "2021-09-16T23:25:56+08:00"
updated: "2021-09-16T23:25:56+08:00"
upvotes: 0
comments: 0
---

# 1448. 统计二叉树中好节点的数目

> **[yiduobo的每日leetcode 1448.统计二叉树中好节点的数目](https://zhuanlan.zhihu.com/p/411190702) · 知乎 · 2021-09-16 · 赞同 0**
> 力扣：[1448. 统计二叉树中好节点的数目](https://leetcode.cn/problems/count-good-nodes-in-binary-tree/) · Medium · 灵茶山艾府：[简洁写法（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1448.统计二叉树中好节点的数目

[力扣](https://leetcode-cn.com/problems/count-good-nodes-in-binary-tree/)

对于某个节点now，如果想判断其是否为好节点，那么需要知道从根节点开始到now的路径上所有节点的最大值，不妨设其为f[now]。

对于f\[now\]而言，则可以通过f\[father\[now\]\]与now.val的得来，也就是说只需要在计算f\[now\]之前优先计算好f\[father\[now\]\]的情况，于是一个自然的想法是从根节点开始进行bfs，在bfs的过程同步更新f值以及答案即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def goodNodes(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        q = [[root, root.val]]
        l = 0
        r = 1
        res = 0
        while l < r:
            now, max_num = q[l]
            l += 1
            if now.val >= max_num:
                max_num = now.val
                res += 1
            if now.left:
                q.append([now.left, max_num])
                r += 1
            if now.right:
                q.append([now.right, max_num])
                r += 1
        
        return res
```
