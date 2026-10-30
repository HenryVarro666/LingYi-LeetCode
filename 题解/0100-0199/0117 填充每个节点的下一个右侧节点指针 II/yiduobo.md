---
title: "117. 填充每个节点的下一个右侧节点指针II"
aliases: ["yiduobo的每日leetcode 117.填充每个节点的下一个右侧节点指针II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/breadth-first-search", "leetcode/recursion", "leetcode/linked-list", "leetcode/binary-tree", "题单/链表-二叉树与回溯", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/面试经典-150-题/二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/139360215"
zhihu_id: "139360215"
zhihu_title: "yiduobo的每日leetcode 117.填充每个节点的下一个右侧节点指针II"
question_id: "117"
question: "填充每个节点的下一个右侧节点指针 II"
problem_url: "https://leetcode.cn/problems/populating-next-right-pointers-in-each-node-ii/"
difficulty: "Medium"
created: "2020-05-09T21:55:43+08:00"
updated: "2020-05-09T21:55:43+08:00"
upvotes: 0
comments: 0
---

# 117. 填充每个节点的下一个右侧节点指针II

> **[yiduobo的每日leetcode 117.填充每个节点的下一个右侧节点指针II](https://zhuanlan.zhihu.com/p/139360215) · 知乎 · 2020-05-09 · 赞同 0**
> 力扣：[117. 填充每个节点的下一个右侧节点指针 II](https://leetcode.cn/problems/populating-next-right-pointers-in-each-node-ii/) · Medium · 灵茶山艾府：[三种方法：DFS/BFS/BFS+链表（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

117.填充每个节点的下一个右侧节点指针II<https://leetcode-cn.com/problems/populating-next-right-pointers-in-each-node-ii/>

上一题的升级版本（传送门在这里：[yiduobo：yiduobo的每日leetcode 116.填充每个节点的下一个右侧节点指针](https://zhuanlan.zhihu.com/p/139108969)）

由于这一题不再能保证左右子树的存在性，因此不能在采取上一题的“a节点的next是b节点”这种做法，因为我们无法保证b节点的存在性，而是需要改成，当我们处理到a节点时，才能得到同一层已经处理过的最后一个节点的next是a节点。

具体的例子可以看样例中第三层的5与7：

在上一题中，我们处理到2的右孩子5时，就可以确定5的next一定是2的next的左孩子，即3的左孩子。但是在这里，3是没有左孩子的，而只有当我们处理到3的右孩子7时，才能确定同一层已经处理过的最后一个节点5的next是7。

于是我们现在的做法还是一层一层往下做，利用这一层的next来构建下一层的next。不同的地方是我们需要维护好下一个层已经处理过的最后一个节点next_tail。

这个next_tail一开始是下一层的第一个节点，然后每次处理到一个节点p时，分别检测p是否存在左右孩子，然后将next_tail的next指向对应的节点，同时更新next_tail即可。

当完成某一层的操作时，需要继续在下一行进行操作，于是也需要额外维护好下一层的第一个节点next_head，然后在完成当前行的操作之后从next_head开始进行下一行的操作。

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

        now = root
        while now:
            next_head = None
            next_tail = None
            while now:
                if now.left:
                    if not next_head:
                        next_head = now.left
                    else:
                        next_tail.next = now.left
                    next_tail = now.left
                if now.right:
                    if not next_head:
                        next_head = now.right
                    else:
                        next_tail.next = now.right
                    next_tail = now.right
                now = now.next

            now = next_head

        return root
```
