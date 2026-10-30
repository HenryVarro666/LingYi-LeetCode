---
title: "865. 具有所有最深节点的最小子树"
aliases: ["yiduobo的每日leetcode 865.具有所有最深节点的最小子树"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/349837858"
zhihu_id: "349837858"
zhihu_title: "yiduobo的每日leetcode 865.具有所有最深节点的最小子树"
question_id: "865"
question: "具有所有最深节点的最小子树"
problem_url: "https://leetcode.cn/problems/smallest-subtree-with-all-the-deepest-nodes/"
difficulty: "Medium"
rating: 1534
created: "2021-02-09T22:03:28+08:00"
updated: "2021-02-09T22:03:28+08:00"
upvotes: 0
comments: 0
---

# 865. 具有所有最深节点的最小子树

> **[yiduobo的每日leetcode 865.具有所有最深节点的最小子树](https://zhuanlan.zhihu.com/p/349837858) · 知乎 · 2021-02-09 · 赞同 0**
> 力扣：[865. 具有所有最深节点的最小子树](https://leetcode.cn/problems/smallest-subtree-with-all-the-deepest-nodes/) · Medium · 灵茶山艾府：[一次 DFS，两种写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

865.具有所有最深节点的最小子树

[力扣](https://leetcode-cn.com/problems/smallest-subtree-with-all-the-deepest-nodes/)

为了获取到所有的最深节点，一个自然的想法就是对树进行一趟层次遍历，那么最后那一层的节点就是最深的节点。

接下来，要找到具有所有这些节点的最小子树，那么可以从这些节点开始向上爬，直到所有节点最终汇集到某个节点，那么以该节点就是最终答案。为了向上爬升，就需要直到每个节点的父亲节点是什么，而这个信息正好可以在层次遍历时得到。

于是现在的做法就是：

1、从根节点开始进行层次遍历，同时在遍历过程中储存每个节点的父亲节点是什么

2、从层次遍历最底层的节点开始进行爬升，同样是采用bfs，对于当前节点，若将当前节点的父亲节点没有在队列中，那么就将其加入到队列中，直到当前轮次的bfs队列中只有一个节点为止。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def subtreeWithAllDeepest(self, root):
        """
        :type root: TreeNode
        :rtype: TreeNode
        """

        if not root:
            return root

        fa = {}
        q = [root]
        l = 0
        r = 1
        last_l = last_r = None
        while l < r:
            for now in q[l:r]:
                if now.left:
                    fa[now.left] = now
                    q.append(now.left)
                if now.right:
                    fa[now.right] = now
                    q.append(now.right)
        
            last_l, last_r, l, r = l, r, r, len(q)

        q = q[last_l:last_r]
        l = 0
        r = len(q)
        used = set()
        while l < r - 1:
            for now in q[l:r]:
                if now in fa and fa[now].val not in used:
                    q.append(fa[now])
                    used.add(fa[now].val)

            l, r = r, len(q)

        return q[l]
```
