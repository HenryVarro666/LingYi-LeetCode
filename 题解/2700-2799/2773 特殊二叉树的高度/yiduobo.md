---
title: "2773. 特殊二叉树的高度"
aliases: ["yiduobo的每日leetcode 2773.特殊二叉树的高度"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/655689269"
zhihu_id: "655689269"
zhihu_title: "yiduobo的每日leetcode 2773.特殊二叉树的高度"
question_id: "2773"
question: "特殊二叉树的高度"
problem_url: "https://leetcode.cn/problems/height-of-special-binary-tree/"
created: "2023-09-12T03:38:02+08:00"
updated: "2023-09-12T03:38:02+08:00"
upvotes: 1
comments: 0
---

# 2773. 特殊二叉树的高度

> **[yiduobo的每日leetcode 2773.特殊二叉树的高度](https://zhuanlan.zhihu.com/p/655689269) · 知乎 · 2023-09-12 · 赞同 1**
> 力扣：[2773. 特殊二叉树的高度](https://leetcode.cn/problems/height-of-special-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2773.特殊二叉树的高度

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/height-of-special-binary-tree/)

对于常规二叉树高度的求解，可以使用对树进行层序遍历，遍历的轮次减去1即为树的高度。对于本题，由于叶子节点可能形成环，那么只需保证层序遍历时不会到达叶子字节，那么遍历的轮次就恰好是树的高度了。现在的问题就是如何确定哪些节点是叶子节点。

由于叶子节点形成了环，那么只需从根节点不断向左侧行走，若当前节点不存在左孩子，则向右侧行走。这样一来，一旦来到某个叶子节点，那么就会不断向左行走，直到走回到这个叶子节点。根据这个结论，就只需使用一个集合记录过程中经过的节点，若某个节点的左侧节点已经出现在集合中，那么当前节点就必然是环上的一个叶子节点。接下来，从这个节点开始向左侧不断行走直到走回该节点，期间经过的所有节点就都是叶子节点。

找出叶子节点后，只需从根节点向下进行层序遍历，并保证不遍历到任意叶子节点，而遍历的轮次即为最终答案。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def heightOfTree(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: int
        """

        vis = set()
        now = root
        while now and now.val not in vis:
            vis.add(now.val)
            if now.left:
                now = now.left
            else:
                now = now.right
        
        if now:
            leaf_set = set([now.val])
            now = now.left
            while now.val not in leaf_set:
                leaf_set.add(now.val)
                now = now.left
        else:
            leaf_set = set()

        q = [root]
        head, tail = 0, 1
        level = 0
        while head < tail:
            level += 1
            for now in q[head: tail]:
                if now.left and now.left.val not in leaf_set:
                    q.append(now.left)
                if now.right and now.right.val not in leaf_set:
                    q.append(now.right)
            
            head, tail = tail, len(q)
        
        return level
```
