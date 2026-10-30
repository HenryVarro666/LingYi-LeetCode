---
title: "2. 两数相加"
aliases: ["yiduobo的每日leetcode 2.两数相加"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/一-链表", "题单/LeetCode-热题-100/链表", "题单/面试经典-150-题/链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/112284805"
zhihu_id: "112284805"
zhihu_title: "yiduobo的每日leetcode 2.两数相加"
question_id: "2"
question: "两数相加"
problem_url: "https://leetcode.cn/problems/add-two-numbers/"
difficulty: "Medium"
created: "2020-03-10T21:07:22+08:00"
updated: "2020-03-10T21:07:22+08:00"
upvotes: 0
comments: 0
---

# 2. 两数相加

> **[yiduobo的每日leetcode 2.两数相加](https://zhuanlan.zhihu.com/p/112284805) · 知乎 · 2020-03-10 · 赞同 0**
> 力扣：[2. 两数相加](https://leetcode.cn/problems/add-two-numbers/) · Medium · 灵茶山艾府：[【动画】简洁写法！从递归到迭代！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2.两数相加<https://leetcode-cn.com/problems/add-two-numbers/>

链表操作的题目，相加之后链表指针同时往后移动即可。需要注意几个细节：

1、进位的处理。由于是加法，因此每次最多进1，用一个标记记录一下即可。

2、指针同时移动时某个链表走完了。此时需要继续走另一个链表。

3、两个链表都走到头时最高位有进位。需要把进位加到结果链表当中。

最后附上python的代码：

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
        
        add_flag = 0
        head = ListNode(0)
        now = None
        
        while l1 != None or l2 != None or add_flag != 0:
            sum = add_flag
            if l1:
                sum += l1.val
                l1 = l1.next
            if l2:
                sum += l2.val
                l2 = l2.next
                
            add_flag = sum / 10
            sum %= 10
            
            if not now:
                head.val = sum
                now = head
            else:
                new_node = ListNode(sum)
                now.next = new_node
                now = new_node
            
        return head
```
