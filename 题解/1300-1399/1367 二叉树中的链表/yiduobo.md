---
title: "1367. 二叉树中的列表"
aliases: ["yiduobo的每日leetcode 1367.二叉树中的列表"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/backtracking", "leetcode/enumeration", "leetcode/sliding-window", "leetcode/hash-function", "leetcode/rolling-hash", "题单/链表-二叉树与回溯", "题单/字符串", "题单/链表-二叉树与回溯/二-二叉树", "题单/字符串/四-字符串哈希"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/400039259"
zhihu_id: "400039259"
zhihu_title: "yiduobo的每日leetcode 1367.二叉树中的列表"
question_id: "1367"
question: "二叉树中的链表"
problem_url: "https://leetcode.cn/problems/linked-list-in-binary-tree/"
difficulty: "Medium"
rating: 1650
created: "2021-08-15T18:29:57+08:00"
updated: "2021-08-15T18:29:57+08:00"
upvotes: 0
comments: 0
---

# 1367. 二叉树中的列表

> **[yiduobo的每日leetcode 1367.二叉树中的列表](https://zhuanlan.zhihu.com/p/400039259) · 知乎 · 2021-08-15 · 赞同 0**
> 力扣：[1367. 二叉树中的链表](https://leetcode.cn/problems/linked-list-in-binary-tree/) · Medium · 灵茶山艾府：[两种方法：暴力匹配 / 滚动哈希（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1367.二叉树中的列表

[力扣](https://leetcode-cn.com/problems/linked-list-in-binary-tree/)

没有什么特别好的思路，我选择的做法是在树中进行dfs，枚举答案的起点。对于每个起点，我们同样是进行dfs来判断从当前点开始是否能与链表进行匹配。

具体的检测方式为先判断当前处理的树节点是否与链表节点值相等，若相等，那么就分别递归匹配树的左右孩子以及链表的下一个节点，直到匹配到链表末尾，或者出现值不相等的情况。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def isSubPath(self, head, root):
        """
        :type head: ListNode
        :type root: TreeNode
        :rtype: bool
        """

        return self.dfs(root, head)
    
    def dfs(self, now_root, now_head):
        if now_head is None:
            return True
        if now_root is None:
            return False
        
        return self.check(now_root, now_head) or self.dfs(now_root.left, now_head) or self.dfs(now_root.right, now_head)
    
    def check(self, now_root, now_head):
        if now_head is None:
            return True
        if now_root is None:
            return False
        
        if now_root.val != now_head.val:
            return False
        
        return self.check(now_root.left, now_head.next) or self.check(now_root.right, now_head.next)
```
