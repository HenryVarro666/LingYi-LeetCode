---
title: "116. 填充每个节点的下一个右侧节点指针"
aliases: ["yiduobo的每日leetcode 116.填充每个节点的下一个右侧节点指针"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/breadth-first-search", "leetcode/recursion", "leetcode/linked-list", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/139108969"
zhihu_id: "139108969"
zhihu_title: "yiduobo的每日leetcode 116.填充每个节点的下一个右侧节点指针"
question_id: "116"
question: "填充每个节点的下一个右侧节点指针"
problem_url: "https://leetcode.cn/problems/populating-next-right-pointers-in-each-node/"
difficulty: "Medium"
created: "2020-05-08T22:08:20+08:00"
updated: "2020-05-08T22:08:20+08:00"
upvotes: 0
comments: 0
---

# 116. 填充每个节点的下一个右侧节点指针

> **[yiduobo的每日leetcode 116.填充每个节点的下一个右侧节点指针](https://zhuanlan.zhihu.com/p/139108969) · 知乎 · 2020-05-08 · 赞同 0**
> 力扣：[116. 填充每个节点的下一个右侧节点指针](https://leetcode.cn/problems/populating-next-right-pointers-in-each-node/) · Medium · 灵茶山艾府：[三种方法：DFS/BFS/BFS+链表（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

116.填充每个节点的下一个右侧节点指针<https://leetcode-cn.com/problems/populating-next-right-pointers-in-each-node/>

比较有意思的题目。

对于一个节点p，若p有左孩子，那么p的左孩子的next一定是指向p的右孩子的，于是有p.left.next \= p.right。另外，对于p的右孩子，可以发现其一定是指向了p的next的左孩子的，于是有p.right.next \= p.next.left。之后，只需要递归处理p.left与p.right即可。

需要注意的是，因为题目保证了这是一颗满二叉树，因此才能保证p.left与p.right的next是一定存在于树中的。

每个节点处理一次，因此最终的时间复杂度为O(n)，n为节点的数目。

最后附上python代码：

```python
"""
# Definition for a Node.
class Node(object):
    def __init__(self, val=0, left=None, right=None, next=None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next
"""

class Solution(object):
    def connect(self, root):
        """
        :type root: Node
        :rtype: Node
        """

        if not root:
            return root
        self.dfs(root)
        return root

    def dfs(self, now):
        if now.left:
            now.left.next = now.right
            if now.next:
                now.right.next = now.next.left
            self.dfs(now.left)
            self.dfs(now.right)
```
