---
title: "234. 回文链表"
aliases: ["yiduobo的每日leetcode 234.回文链表"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/recursion", "leetcode/two-pointers", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/链表-二叉树与回溯/一-链表", "题单/LeetCode-热题-100/链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/150106654"
zhihu_id: "150106654"
zhihu_title: "yiduobo的每日leetcode 234.回文链表"
question_id: "234"
question: "回文链表"
problem_url: "https://leetcode.cn/problems/palindrome-linked-list/"
difficulty: "Easy"
created: "2020-06-22T21:41:49+08:00"
updated: "2020-06-22T21:41:49+08:00"
upvotes: 0
comments: 0
---

# 234. 回文链表

> **[yiduobo的每日leetcode 234.回文链表](https://zhuanlan.zhihu.com/p/150106654) · 知乎 · 2020-06-22 · 赞同 0**
> 力扣：[234. 回文链表](https://leetcode.cn/problems/palindrome-linked-list/) · Easy · 灵茶山艾府：[两种方法：递归 / 寻找中间节点+反转链表（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

234.回文链表<https://leetcode-cn.com/problems/palindrome-linked-list/>

又是一道缝合怪，依照惯例，还是加入假头p_head接在head的前面方便操作。

首先，因为需要常数的时间复杂度，因此不能使用递归之类的做法，因此想判断回文，就必须找到回文的中心。

若链表是回文链表，那么其中心一定位于正中间的节点，于是可以使用快慢指针来找到中心节点。这一步的时间复杂度为O(n)。

接下来，需要判断从中心开始往两边的节点是否是回文的，但是这里链表不能往回走，因此一个自然的想法就是将链表的后半部分反序，然后从p_head和中心节点开始往后遍历逐个判断。于是就需要从中心节点开始翻转链表，然后一趟扫描进行判断。这一步的时间复杂度也是O(n)。

例如链表A -> B -> C -> D -> E -> D -> C -> B -> A，首先通过快慢指针找到中心节点，为节点E。

接下来，将节点E之后的链表进行翻转，变成A -> B -> C -> D -> E -> A -> B -> C -> D，此时从表头和E开始逐个扫描判断是否相等即可。

需要注意对于长度为偶数的链表，中心节点需要取在len/2的位置，因为后半部分的链表是需要翻转的。例如链表A -> B -> C -> D -> D -> C -> B -> A，我们需要选择第一个D作为中心节点，因为从第二D开始的D -> C -> B -> A是需要翻转的部分。

当然，如果从p_head出发做快慢指针的话，慢指针自然就会停留在len/2的位置，此时就需要判断快指针后方是否存在节点，如果存在，那么说明链表长度为奇数，于是需要将慢指针再往后移动一位作为中心节点。

最后附上python代码，三个循环分别为找中心节点，翻转后半部分以及扫描判断是否相等：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def isPalindrome(self, head):
        """
        :type head: ListNode
        :rtype: bool
        """

        if not head or not head.next:
            return True

        p_head = ListNode(0)
        p_head.next = head
        fast = slow = p_head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        if fast.next:
            slow = slow.next

        prev = slow.next
        now = prev.next
        prev.next = None

        while now:
            tmp = now.next
            now.next = prev
            prev = now
            now = tmp

        slow.next = prev

        first = head
        second = slow.next
        while second:
            if second.val != first.val:
                return False
            first = first.next
            second = second.next

        return True
```
