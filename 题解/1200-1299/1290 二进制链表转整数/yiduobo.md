---
title: "1290. 二进制链表转整数"
aliases: ["yiduobo的每日leetcode 1290.二进制链表转整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/linked-list", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/一-链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/389777668"
zhihu_id: "389777668"
zhihu_title: "yiduobo的每日leetcode 1290.二进制链表转整数"
question_id: "1290"
question: "二进制链表转整数"
problem_url: "https://leetcode.cn/problems/convert-binary-number-in-a-linked-list-to-integer/"
difficulty: "Easy"
created: "2021-07-14T22:48:11+08:00"
updated: "2021-07-14T22:48:11+08:00"
upvotes: 0
comments: 0
---

# 1290. 二进制链表转整数

> **[yiduobo的每日leetcode 1290.二进制链表转整数](https://zhuanlan.zhihu.com/p/389777668) · 知乎 · 2021-07-14 · 赞同 0**
> 力扣：[1290. 二进制链表转整数](https://leetcode.cn/problems/convert-binary-number-in-a-linked-list-to-integer/) · Easy · 灵茶山艾府：[遍历链表（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1290.二进制链表转整数

[力扣](https://leetcode-cn.com/problems/convert-binary-number-in-a-linked-list-to-integer/)

设链表长度为l，其中第k个值为a[k]，那么最终得到的整数就是

res \= a[0] \* 2^(l - 1) + a[1] \* 2^(l - 2) + ... + a[l - 1] \* 2^0

变形之后可得

res \= (((a[0] \* 2 + a[1]) \* 2 + a[2]) \* 2 + ...) \* 2 + a[l - 1]

那么我们就可以从链表头部开始向后走，并初始化res为0。接下来每一步都将res乘以2，并加上当前链表中的值。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def getDecimalValue(self, head):
        """
        :type head: ListNode
        :rtype: int
        """

        now = head
        res = now.val
        while now.next:
            now = now.next
            res += res + now.val
        
        return res
```
