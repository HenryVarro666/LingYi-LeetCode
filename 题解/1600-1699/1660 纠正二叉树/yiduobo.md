---
title: "1660. 纠正二叉树"
aliases: ["yiduobo的每日leetcode 1660.纠正二叉树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/619469410"
zhihu_id: "619469410"
zhihu_title: "yiduobo的每日leetcode 1660.纠正二叉树"
question_id: "1660"
question: "纠正二叉树"
problem_url: "https://leetcode.cn/problems/correct-a-binary-tree/"
created: "2023-04-04T19:27:09+08:00"
updated: "2023-04-04T19:27:09+08:00"
upvotes: 0
comments: 0
---

# 1660. 纠正二叉树

> **[yiduobo的每日leetcode 1660.纠正二叉树](https://zhuanlan.zhihu.com/p/619469410) · 知乎 · 2023-04-04 · 赞同 0**
> 力扣：[1660. 纠正二叉树](https://leetcode.cn/problems/correct-a-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1660.纠正二叉树

[力扣](https://leetcode.cn/problems/correct-a-binary-tree/)

首先，题目中有问题的节点的右孩子指向的是同一层的右侧某个节点，因此本题大的解决思路自然就是层序遍历，且每一层应该从右向左执行，理由是题目是要找出发出错误指针的节点，而不是被错误指针指向的节点，那么如果按照从左向右的顺序执行的话，只能检测到某个节点被指向了两次，但是无法直接反查到这个节点是被同层的哪个节点指向。

另一方面，题目要求直接移除以这个错误节点为根节点的子树，因此在这里应该是每个节点检测其左右孩子是否为错误节点，而不是检测自身，因为这样一来检测出问题后就可以直接将对应的孩子删去。

最后，题目中保证了每个节点的val不同，因此可以使用集合来帮助判断每个节点是否已经被指向过。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def correctBinaryTree(self, root):
        """
        :type root: TreeNode
        :rtype: TreeNode
        """

        vis = set([root.val])
        head, tail = 0, 1
        q = [root]
        while head < tail:
            for now in q[head : tail]:
                if now.right:
                    if now.right.right and now.right.right.val in vis:
                        now.right = None
                        return root
                    
                    q.append(now.right)
                    vis.add(now.right.val)
                
                if now.left:
                    if now.left.right and now.left.right.val in vis:
                        now.left = None
                        return root
                
                    q.append(now.left)
                    vis.add(now.left.val)
            
            head, tail = tail, len(q)
```
