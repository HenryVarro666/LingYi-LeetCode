---
title: "141. 环形链表 & 142. 环形链表II"
aliases: ["yiduobo的每日leetcode 141.环形链表 && 142.环形链表II", "141. 环形链表", "142. 环形链表II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/linked-list", "leetcode/two-pointers", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/一-链表", "题单/LeetCode-热题-100/链表", "题单/面试经典-150-题/链表", "leetcode/medium", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/142167493"
zhihu_id: "142167493"
zhihu_title: "yiduobo的每日leetcode 141.环形链表 && 142.环形链表II"
question_id: ["141", "142"]
question: ["环形链表", "环形链表 II"]
problem_url: ["https://leetcode.cn/problems/linked-list-cycle/", "https://leetcode.cn/problems/linked-list-cycle-ii/"]
difficulty: ["Easy", "Medium"]
created: "2020-05-19T23:28:17+08:00"
updated: "2020-05-19T23:28:17+08:00"
upvotes: 0
comments: 0
---

# 141. 环形链表 & 142. 环形链表II

> **[yiduobo的每日leetcode 141.环形链表 && 142.环形链表II](https://zhuanlan.zhihu.com/p/142167493) · 知乎 · 2020-05-19 · 赞同 0**
> 力扣：[141. 环形链表](https://leetcode.cn/problems/linked-list-cycle/) · Easy · 灵茶山艾府：[没想明白？一个视频讲透快慢指针！（Python/Java/C++/C/Go/JS）](灵茶山艾府.md)
> 力扣：[142. 环形链表 II](https://leetcode.cn/problems/linked-list-cycle-ii/) · Medium · 灵茶山艾府：[【图解】一张图秒懂环形链表 II，Floyd 判圈算法（Python/Java/C++/C/Go/JS）](../0142%20环形链表%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

141.环形链表<https://leetcode-cn.com/problems/linked-list-cycle/>

142.环形链表II <https://leetcode-cn.com/problems/linked-list-cycle-ii/>

141题需要判断链表中是否存在环，142题则是需要找出入环的节点。

还是经典的快慢指针做法，即设置两个指针fast与slow，从head出发，fast每次走两步，slow则是每次走一步。

如果链表中没有环，那么fast一定会先走到链表结尾。

如果有环，那么当fast与slow都进入环中后，每次操作fast与slow的距离都将缩短1，那么fast与slow最终一定会相遇。

接下来是如何寻找入环节点。

不妨设相遇时fast走了m \* 2步，slow走了m步。设入环需要从head往后走k步，环的长度为l，那么就有：

((m \* 2 - k) - (m - k)) % l \= 0

其中m \* 2 - k表示fast在环中走的步数，m - k表示slow在环中走的步数。由于二者相遇，那么二者步数差一定是环长l的倍数。

将上面的式子化简后可以得到m % l \= 0，即如果从入环点开始，走m步，那么一定会走回到入环点。

注意到当前的slow节点，先从head开始在环外走了k步，然后在环内走了m - k步。那么如果slow继续在环内走k步，那么slow就在环内走了m步，换言之，slow将走回到入环点。

另外，如果某个节点从head开始出发走k步，那么其也将走到入环点。

于是我们可以让fast回到head，然后fast与slow每次同时走一步，那么在k步之后，fast与slow将在入环点相遇，此时返回结果即可。

最后附上142题的python代码，141题的可以参考第一个while里面的部分：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def detectCycle(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """

        if not head:
            return None

        fast = slow = head

        while True:
            if not fast or not fast.next:
                return None
            fast = fast.next.next
            slow = slow.next
            if fast == slow:
                break

        fast = head

        while fast != slow:
            fast = fast.next
            slow = slow.next

        return fast
```
