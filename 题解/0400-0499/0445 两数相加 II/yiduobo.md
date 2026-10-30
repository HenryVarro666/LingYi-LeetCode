---
title: "445. 两数相加II"
aliases: ["yiduobo的每日leetcode 445.两数相加II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/一-链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/206749805"
zhihu_id: "206749805"
zhihu_title: "yiduobo的每日leetcode 445.两数相加II"
question_id: "445"
question: "两数相加 II"
problem_url: "https://leetcode.cn/problems/add-two-numbers-ii/"
difficulty: "Medium"
created: "2020-08-30T18:00:43+08:00"
updated: "2020-08-30T18:00:43+08:00"
upvotes: 0
comments: 0
---

# 445. 两数相加II

> **[yiduobo的每日leetcode 445.两数相加II](https://zhuanlan.zhihu.com/p/206749805) · 知乎 · 2020-08-30 · 赞同 0**
> 力扣：[445. 两数相加 II](https://leetcode.cn/problems/add-two-numbers-ii/) · Medium · 灵茶山艾府：[反转链表+两数相加=秒杀！（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

445.两数相加II <https://leetcode-cn.com/problems/add-two-numbers-ii/>

链表下的高精度加法，由于题目要求不能翻转链表，而且加法一般要从最低位开始运算，因此在这里可以使用栈或者递归来进行运算。

我在这里使用的是递归，过程中使用三个参数now_len, len1以及len2分别表示当前答案的位数，当前l1链表中需要处理的位数以及l2链表中需要处理的位数。

初始状态下now_len为len1和len2中较大的那一个，在递归过程中，只有当now_len与len1相等时才处理链表l1，同时更len1的值，只有当now_len与len2相等时才处理链表2，同时更新len2的值。处理完当前节点值之后若now_len大于零，说明还未处理到最低位，此时递归计算now_len - 1位，获取返回的计算结果链表以及进位值。将进位值加到当前的处理结果上，同时将计算结果链表接在当前计算结果之后，返回当前的计算结果链表以及当前的进位值即可。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """

        now = l1
        len1 = 0
        while now:
            len1 += 1
            now = now.next

        now = l2
        len2 = 0
        while now:
            len2 += 1
            now = now.next

        add, res = self.dfs(max(len1, len2), l1, len1, l2, len2)
        if add:
            tmp = ListNode(1)
            tmp.next = res
            return tmp
        else:
            return res

    def dfs(self, now_len, l1, len1, l2, len2):
        val = 0
        if now_len == len1:
            val += l1.val
            len1 -= 1
            l1 = l1.next
        if now_len == len2:
            val += l2.val
            len2 -= 1
            l2 = l2.next

        if now_len > 1:
            add, res = self.dfs(now_len - 1, l1, len1, l2, len2)
        else:
            add, res = 0, None

        val += add
        tmp = ListNode(val % 10)
        tmp.next = res
        res = tmp
        return val / 10, res
```
