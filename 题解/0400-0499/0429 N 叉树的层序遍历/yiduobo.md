---
title: "429. N叉树的层序遍历"
aliases: ["yiduobo的每日leetcode 429.N叉树的层序遍历"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/queue", "leetcode/array", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/195626669"
zhihu_id: "195626669"
zhihu_title: "yiduobo的每日leetcode 429.N叉树的层序遍历"
question_id: "429"
question: "N 叉树的层序遍历"
problem_url: "https://leetcode.cn/problems/n-ary-tree-level-order-traversal/"
difficulty: "Medium"
created: "2020-08-23T16:56:13+08:00"
updated: "2020-08-23T16:56:13+08:00"
upvotes: 0
comments: 0
---

# 429. N叉树的层序遍历

> **[yiduobo的每日leetcode 429.N叉树的层序遍历](https://zhuanlan.zhihu.com/p/195626669) · 知乎 · 2020-08-23 · 赞同 0**
> 力扣：[429. N 叉树的层序遍历](https://leetcode.cn/problems/n-ary-tree-level-order-traversal/) · Medium · 灵茶山艾府：[两种 BFS 写法：双数组/队列（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

429.N叉树的层序遍历<https://leetcode-cn.com/problems/n-ary-tree-level-order-traversal/>

与二叉树的层序遍历没有什么不同，依然是一遍bfs就可以了。

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
    def levelOrder(self, root):
        """
        :type root: Node
        :rtype: List[List[int]]
        """

        if not root:
            return []

        q = [root]
        l = 0
        r = 1
        res = []
        while l < r:
            res.append([])
            newr = r
            for index in range(l, r):
                now = q[index]
                res[-1].append(now.val)
                for child in now.children:
                    q.append(child)
                    newr += 1
            l = r
            r = newr

        return res
```
