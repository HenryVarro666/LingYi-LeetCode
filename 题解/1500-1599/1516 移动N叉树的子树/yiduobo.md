---
title: "1516. 移动N叉树的子树"
aliases: ["yiduobo的每日leetcode 1516.移动N叉树的子树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/617230122"
zhihu_id: "617230122"
zhihu_title: "yiduobo的每日leetcode 1516.移动N叉树的子树"
question_id: "1516"
question: "移动N叉树的子树"
problem_url: "https://leetcode.cn/problems/move-sub-tree-of-n-ary-tree/"
created: "2023-03-27T00:45:50+08:00"
updated: "2023-03-27T00:45:50+08:00"
upvotes: 0
comments: 0
---

# 1516. 移动N叉树的子树

> **[yiduobo的每日leetcode 1516.移动N叉树的子树](https://zhuanlan.zhihu.com/p/617230122) · 知乎 · 2023-03-27 · 赞同 0**
> 力扣：[1516. 移动N叉树的子树](https://leetcode.cn/problems/move-sub-tree-of-n-ary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1516.移动N叉树的子树

[力扣](https://leetcode.cn/problems/move-sub-tree-of-n-ary-tree/)

这题目描述也是服了，对于最复杂的第一种情况，题目提示仔细阅读样例，结果样例里面恰好就是没有第一种情况对应的case。

实际上，第一种情况要求的是先找出p在其父亲节点的孩子列表中的下标位置，然后将这个位置的节点替换成q，然后再将p加入到q孩子列表的末尾。而对于后面两种情况，则只需要将p从其父亲节点的孩子列表中移除，并加入到q孩子列表的末尾即可。

那么对于这个问题，就需要知道p和q的父亲节点，以及二者的最近公共祖先，于是需要先进行一次dfs或者bfs，找出每个节点的父亲节点。

接下来从p开始向上迭代直到根节点，并将路径上的节点使用集合记录下来，然后再从q开始向上迭代，迭代过程中第一个出现在之前集合中的节点即为二者的最近公共祖先。

最后，只需要根据这个最近公共祖先判断p和q是属于题目中描述的哪种情况，然后按照上面所说的处理方法进行相应的移动即可。

需要特别注意的是，p和q可能是树中的根节点，而根节点是没有父亲节点的。为了方便处理，在这里可以额外添加一个假根节点p_root，这样一来p和q就总是存在父亲节点，处理完成后，只需返回这个假根节点的孩子即可。

最后附上python代码：

```python
"""
# Definition for a Node.
class Node(object):
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []
"""

class Solution(object):
    def moveSubTree(self, root, p, q):
        """
        :type root: Node
        :type p: Node
        :type q: Node
        :rtype: Node
        """

        p_root = Node()
        p_root.children.append(root)

        fa = {}
        fa[root] = p_root

        queue = [root]
        head, tail = 0, 1
        while head < tail:
            now = queue[head]
            head += 1
            for child in now.children:
                fa[child] = now
                queue.append(child)
                tail += 1
        
        if fa[p] == q:
            return p_root.children[0]
        
        now = p
        vis = set()
        while now != p_root:
            vis.add(now)
            now = fa[now]
        
        now = q
        while now:
            if now in vis:
                break
            now = fa[now]

        if now == p:
            fa[q].children.remove(q)
            pos = fa[p].children.index(p)
            fa[p].children[pos] = q
        else:
            fa[p].children.remove(p)
        
        q.children.append(p)
        return p_root.children[0]
```
