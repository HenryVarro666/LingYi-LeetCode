---
title: "109. 有序链表转化二叉搜索树"
aliases: ["yiduobo的每日leetcode 109.有序链表转化二叉搜索树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/138536682"
zhihu_id: "138536682"
zhihu_title: "yiduobo的每日leetcode 109.有序链表转化二叉搜索树"
question_id: "109"
question: "有序链表转化二叉搜索树"
problem_url: "https://leetcode.cn/problems/convert-sorted-list-to-binary-search-tree/"
created: "2020-05-06T17:52:42+08:00"
updated: "2020-05-06T17:52:42+08:00"
upvotes: 0
comments: 0
---

# 109. 有序链表转化二叉搜索树

> **[yiduobo的每日leetcode 109.有序链表转化二叉搜索树](https://zhuanlan.zhihu.com/p/138536682) · 知乎 · 2020-05-06 · 赞同 0**
> 力扣：[109. 有序链表转化二叉搜索树](https://leetcode.cn/problems/convert-sorted-list-to-binary-search-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

昨日有事外出，今天补上。

109.有序链表转换二叉搜索树<https://leetcode-cn.com/problems/convert-sorted-list-to-binary-search-tree/>
上一题的升级版本（传送门在这里[yiduobo：yiduobo的每日leetcode 108.将有序数组转化成二叉搜索树](https://zhuanlan.zhihu.com/p/138530184)）。
由于题目从有序数组变成了有序链表，那么意味着我们无法很方便地取到最中间那个节点，于是上一题的做法在这里需要进行修改。
由于链表元素只能一个一个遍历，因此我们不能再使用之前根-左-右的生成方式，而应该使用中序遍历左-根-右的生成方式。由于这里采用中序遍历的方式来生成，这个有序的链表正好能与中序遍历得到的序列对应，因此在递归过程中逐个往后移动链表的指针即可。
于是具体做法只需要进行一点小的修改：根节点依然是最中间的节点，但是这次我们先生成左子树。设置指针指向链表的头部，每生成一个节点则往后移动一步。当生成好左子树之后，链表当前指向的就是根节点。生成好根节点之后再往后生成右子树即可。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def sortedListToBST(self, head):
        """
        :type head: ListNode
        :rtype: TreeNode
        """

        self.head = head
        l = 0
        while head:
            l += 1
            head = head.next

        return self.dfs(0, l)

    def dfs(self, left, right):
        if left == right:
            return None
        mid = (left + right) / 2
        left_tree = self.dfs(left, mid)
        root = TreeNode(self.head.val)
        self.head = self.head.next
        right_tree = self.dfs(mid + 1, right)
        root.left = left_tree
        root.right = right_tree
        return root
```
