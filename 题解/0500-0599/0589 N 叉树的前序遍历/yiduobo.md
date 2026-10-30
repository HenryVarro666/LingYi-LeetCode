---
title: "589. N叉树的前序遍历"
aliases: ["yiduobo的每日leetcode 589.N叉树的前序遍历"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/tree", "leetcode/depth-first-search", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/267532965"
zhihu_id: "267532965"
zhihu_title: "yiduobo的每日leetcode 589.N叉树的前序遍历"
question_id: "589"
question: "N 叉树的前序遍历"
problem_url: "https://leetcode.cn/problems/n-ary-tree-preorder-traversal/"
difficulty: "Easy"
created: "2020-10-21T22:51:43+08:00"
updated: "2020-10-21T22:51:43+08:00"
upvotes: 0
comments: 0
---

# 589. N叉树的前序遍历

> **[yiduobo的每日leetcode 589.N叉树的前序遍历](https://zhuanlan.zhihu.com/p/267532965) · 知乎 · 2020-10-21 · 赞同 0**
> 力扣：[589. N 叉树的前序遍历](https://leetcode.cn/problems/n-ary-tree-preorder-traversal/) · Easy · 灵茶山艾府：[简单 DFS（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

589.N叉树的前序遍历<https://leetcode-cn.com/problems/n-ary-tree-preorder-traversal/>

与二叉树的前序遍历类似，迭代的做法也是用到栈。考虑到栈后进先出的特点，因此在处理到某个节点时，我们应该将当前节点的孩子反序压入栈中。

按上面的做法从根节点开始依次进行处理即可。

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
    def preorder(self, root):
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
            stack.extend(now.children[::-1])
        
        return res
```
