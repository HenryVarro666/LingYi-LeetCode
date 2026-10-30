---
title: "2415. 反转二叉树的奇数层"
aliases: ["yiduobo的每日leetcode 2415.反转二叉树的奇数层"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/tree", "leetcode/depth-first-search", "leetcode/breadth-first-search", "leetcode/binary-tree", "leetcode/bfs", "leetcode/dfs", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/569197755"
zhihu_id: "569197755"
zhihu_title: "yiduobo的每日leetcode 2415.反转二叉树的奇数层"
question_id: "2415"
question: "反转二叉树的奇数层"
problem_url: "https://leetcode.cn/problems/reverse-odd-levels-of-binary-tree/"
difficulty: "Medium"
rating: 1431
created: "2022-09-29T02:36:51+08:00"
updated: "2022-09-29T02:36:51+08:00"
upvotes: 0
comments: 0
---

# 2415. 反转二叉树的奇数层

> **[yiduobo的每日leetcode 2415.反转二叉树的奇数层](https://zhuanlan.zhihu.com/p/569197755) · 知乎 · 2022-09-29 · 赞同 0**
> 力扣：[2415. 反转二叉树的奇数层](https://leetcode.cn/problems/reverse-odd-levels-of-binary-tree/) · Medium · 灵茶山艾府：[直接交换值：BFS / DFS](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2415.反转二叉树的奇数层

[力扣](https://leetcode.cn/problems/reverse-odd-levels-of-binary-tree/)

题目中的反转要求涉及到层数，那么一个自然的想法就是对二叉树进行层序遍历。由于层序遍历的每一轮恰好就是遍历某一层的所有节点，那么就可以在层序遍历的过程中记录当前遍历到了哪一层。若当前遍历到奇数层，那么就将这一层的节点值反转，也就是将当前队列中遍历的这一段的节点值反转过来。由于只修改了节点值，并没有影响到树的结构，因此对后续的层序遍历不会产生影响。

遍历完成后，返回树的根节点即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def reverseOddLevels(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: Optional[TreeNode]
        """

        q = [root]
        level = 0
        head, tail = 0, 1
        while head < tail:
            for now in q[head : tail]:
                if now.left:
                    q.append(now.left)
                    q.append(now.right)
            
            if level % 2 == 1:
                l, r = head, tail - 1
                while l < r:
                    q[l].val, q[r].val = q[r].val, q[l].val
                    l += 1
                    r -= 1
            
            head, tail = tail, len(q)
            level += 1
        
        return root
```
