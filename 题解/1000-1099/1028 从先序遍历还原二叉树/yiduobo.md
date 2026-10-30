---
title: "1028. 从先序遍历还原二叉树"
aliases: ["yiduobo的每日leetcode 1028.从先序遍历还原二叉树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/369457006"
zhihu_id: "369457006"
zhihu_title: "yiduobo的每日leetcode 1028.从先序遍历还原二叉树"
question_id: "1028"
question: "从先序遍历还原二叉树"
problem_url: "https://leetcode.cn/problems/recover-a-tree-from-preorder-traversal/"
created: "2021-05-02T22:46:03+08:00"
updated: "2021-05-02T22:46:03+08:00"
upvotes: 0
comments: 0
---

# 1028. 从先序遍历还原二叉树

> **[yiduobo的每日leetcode 1028.从先序遍历还原二叉树](https://zhuanlan.zhihu.com/p/369457006) · 知乎 · 2021-05-02 · 赞同 0**
> 力扣：[1028. 从先序遍历还原二叉树](https://leetcode.cn/problems/recover-a-tree-from-preorder-traversal/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1028.从先序遍历还原二叉树

[力扣](https://leetcode-cn.com/problems/recover-a-tree-from-preorder-traversal/)

题目给出的先序遍历中附带了节点的层次信息，那么对于一个位于第k层的节点而言：

1、其父节点必然是离该节点最近，且先序遍历在其之前的第k - 1层的节点

2、若某个位于第k层的节点后面出现了层次小于等于k的其他节点，那么就说明以这个第k层的节点为根节点的子树已经遍历完了

由于先序遍历本身也可以看作二叉树的某种dfs序，那么根据以上两点，我们就可以使用一个栈来维护当前正在处理的节点。对于当前处理的节点now：

1、先对比now与栈顶节点的层次。若栈不为空且栈顶元素的层次大于等于now的层次，那么就将栈顶节点弹出，直到栈为空或者栈顶元素的层次小于now的层次。

2、若此时的栈为空，说明now是整棵树的根节点，否则栈顶节点必然是now的父节点。若此时栈顶节点没有左孩子，那么根据题目描述，应该先将now置为栈顶节点的左孩子。若此时栈顶节点有左孩子，那么就将now置为栈顶节点的右孩子。

按这个流程遍历完整个先序遍历，最后返回根节点即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def recoverFromPreorder(self, S):
        """
        :type S: str
        :rtype: TreeNode
        """

        stack = []
        l = len(S)
        now = 0

        while now < l:
            level = 0
            while now < l and S[now] == '-':
                level += 1
                now += 1
            
            num = 0
            while now < l and S[now] != '-':
                num = num * 10 + ord(S[now]) - 48
                now += 1

            while level < len(stack):
                stack.pop()
            
            node = TreeNode(num)
            if len(stack) > 0:
                if stack[-1].left is None:
                    stack[-1].left = node
                else:
                    stack[-1].right = node
            
            stack.append(node)
        
        return stack[0]
```
