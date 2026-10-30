---
title: "590. N叉树的后序遍历"
aliases: ["yiduobo的每日leetcode 590.N叉树的后序遍历"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/267535277"
zhihu_id: "267535277"
zhihu_title: "yiduobo的每日leetcode 590.N叉树的后序遍历"
question_id: "590"
question: "N 叉树的后序遍历"
problem_url: "https://leetcode.cn/problems/n-ary-tree-postorder-traversal/"
difficulty: "Easy"
created: "2020-10-21T22:55:23+08:00"
updated: "2020-10-21T22:55:23+08:00"
upvotes: 0
comments: 0
---

# 590. N叉树的后序遍历

> **[yiduobo的每日leetcode 590.N叉树的后序遍历](https://zhuanlan.zhihu.com/p/267535277) · 知乎 · 2020-10-21 · 赞同 0**
> 力扣：[590. N 叉树的后序遍历](https://leetcode.cn/problems/n-ary-tree-postorder-traversal/) · Easy · 灵茶山艾府：[简单 DFS（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

590.N叉树的后序遍历<https://leetcode-cn.com/problems/n-ary-tree-postorder-traversal/>

注意到N叉树的后序遍历是

子树1 -> 子树2 -> ... -> 子树n -> 根节点

这种形式，那么如果将其翻转，就是

根节点 -> 子树n -> 子树n-1 -> ... ->子树1

这种形式与上一题N叉树的前序遍历非常类似，区别之处在于子树的顺序刚好是反过来的，因此在处理到某个节点时，直接按顺序将该节点的子树压入栈中。得到最终的答案后，将其反序输出即可。

最后附上python代码：

```python
"""
# Definition for a Node.
class Node(object):
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children
"""

class Solution(object):
    def postorder(self, root):
        """
        :type root: Node
        :rtype: List[int]
        """

        if not root:
            return []

        res = []
        stack = [root]
        while stack:
            now = stack.pop()
            res.append(now.val)
            stack.extend(now.children)
        
        return res[::-1]
```
