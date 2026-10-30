---
title: "2816. 翻倍以链表形式表示的数字"
aliases: ["yiduobo的每日leetcode 2816.翻倍以链表形式表示的数字"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/linked-list", "leetcode/math", "leetcode/bian-li", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/一-链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/658601364"
zhihu_id: "658601364"
zhihu_title: "yiduobo的每日leetcode 2816.翻倍以链表形式表示的数字"
question_id: "2816"
question: "翻倍以链表形式表示的数字"
problem_url: "https://leetcode.cn/problems/double-a-number-represented-as-a-linked-list/"
difficulty: "Medium"
created: "2023-09-26T23:57:12+08:00"
updated: "2023-09-26T23:57:12+08:00"
upvotes: 0
comments: 0
---

# 2816. 翻倍以链表形式表示的数字

> **[yiduobo的每日leetcode 2816.翻倍以链表形式表示的数字](https://zhuanlan.zhihu.com/p/658601364) · 知乎 · 2023-09-26 · 赞同 0**
> 力扣：[2816. 翻倍以链表形式表示的数字](https://leetcode.cn/problems/double-a-number-represented-as-a-linked-list/) · Medium · 灵茶山艾府：[两种方法：调用 445 题 / 一次遍历（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2816.翻倍以链表形式表示的数字

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/double-a-number-represented-as-a-linked-list/)

本题比较不好处理的地方主要在于进位，不过注意到本题是翻倍操作，也可以理解成加法操作，那么对于加法操作的进位，其有一个性质就是进位的值只能为1。在这里可以使用简单归纳法来证明。首先最低位的进位只能是1，而对于不是最低位的任意位，若其低位上的进位也最多为1的话，那么对于当前位，即使是两个9相加，再加上进位的1，最大也只有19，也就是说当前位也最多只会产生1的进位。

另一方面，由于本题是自己加自己，因此实际上进位的1也不会对当前位是否会再次进位产生任何影响。更进一步的，只有当某一位的数值大于等于5时，该位才会发生进位。

根据这一点，就需要先判断链表头部节点的值是否大于等于5，若是，那么最终会产生额外的进位，在这里就需要新建立一个值为1的节点作为新的头部节点。接下来从链表头部开始向后遍历。若当前节点存在后继节点，且后继节点的值大于等于5，那么当前节点就会接受后继节点的进位。另外，当前节点的进位已经在当前节点的前驱节点被考虑过了，因此在这里只需将当前节点值翻倍然后模10，再根据是否接受后继节点的进位来决定是否需要加上1就行了。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def doubleIt(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """

        res = head
        if head.val >= 5:
            res = ListNode(1)
            res.next = head
        
        now = head
        while now:
            now.val = (now.val + now.val) % 10
            if now.next and now.next.val >= 5:
                now.val += 1
            now = now.next
        
        return res
```
