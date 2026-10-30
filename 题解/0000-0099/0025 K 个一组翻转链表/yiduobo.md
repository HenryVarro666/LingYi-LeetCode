---
title: "25. K个一组翻转链表"
aliases: ["yiduobo的每日leetcode 25.K个一组翻转链表"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/linked-list", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/一-链表", "题单/LeetCode-热题-100/链表", "题单/面试经典-150-题/链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/116889575"
zhihu_id: "116889575"
zhihu_title: "yiduobo的每日leetcode 25.K个一组翻转链表"
question_id: "25"
question: "K 个一组翻转链表"
problem_url: "https://leetcode.cn/problems/reverse-nodes-in-k-group/"
difficulty: "Hard"
created: "2020-03-25T22:40:37+08:00"
updated: "2020-03-25T22:40:37+08:00"
upvotes: 0
comments: 0
---

# 25. K个一组翻转链表

> **[yiduobo的每日leetcode 25.K个一组翻转链表](https://zhuanlan.zhihu.com/p/116889575) · 知乎 · 2020-03-25 · 赞同 0**
> 力扣：[25. K 个一组翻转链表](https://leetcode.cn/problems/reverse-nodes-in-k-group/) · Hard · 灵茶山艾府：[【视频讲解】从反转链表到 K 个一组反转（Python/Java/C++/C/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

25.K个一组翻转链表<https://leetcode-cn.com/problems/reverse-nodes-in-k-group/>

上一题的推广形式，可以先通过在链表上走k部找出需要翻转的部分，然后这个部分的头部开始逐个翻转。例如对于

left -> node_1 -> node_2 -> node_3 -> ... -> node_k -> right的形式，假设我们从node_1开始走k步停在了node_k这个节点上，即now \= node_k。我们需要记录下这个part的头部，也就是start \= node_1，此时链接情况如下：

left -> node_1(start) -> node_2 -> node_3 -> ... -> node_k(now) -> right

接下来将left的next指向这K个节点的末尾，即left.next \= now，同时由于完成翻转后，node_1将处于现在now的位置，成为right和之和部分的新头部，因此将left改成node_1，即left \= start，此时链接情况如下：

(1) old_left -> node_k(now) -> right

(2) node_1(start, left) -> node_2 -> node_3 -> ... -> node_k(now) -> right

接下来可以发现，我们只需要将(2)中的节点，从start开始到now，一个一个插在right的前方即可。我们定义一个last_one表示当前处理节点在答案中的下一个节点是什么，那么对于node_1，有last_one为right，对于node_2，last_one为node_1，对于node_n，last_one就是node_n-1。

因此在逐个插入的时候，需要一起更新last_one以及start。

此时每次插入后的链接情况如下，其中(3)代表插入在right前方得到的链表：

(1.1) old_left -> node_k(now) -> right

(1.2) node_2(start) -> node_3 -> ... -> node_k(now) -> right

(1.3) node_1(last_one, left) -> right

(2.1) old_left -> node_k(now) -> right

(2.2) node_3(start) -> ... -> node_k(now) -> right

(2.3) node_2(last_one) -> node_1(left) -> right

...

(k-1.1) old_left -> node_k(now) -> right

(k-1.2) node_k(start, now) -> right

(k-1.3) node_k-1(last_one) -> ... -> node_1(left) -> right

最后为了继续操作right以及之后部分的操作，需要将now移动到right上，即now \= start.next，之后再将上面的(k-1.1)与(k-1.3)合并起来，即start.next \= last_one即可。最后将得到下面这个形式：

old_left -> node_k(start) -> node_k-1(last_one) -> ... -> node_1(left) -> right(now)

与之前的链表题目一样，这里也增加一个假头new_head，用来表示前k个节点的left。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def reverseKGroup(self, head, k):
        """
        :type head: ListNode
        :type k: int
        :rtype: ListNode
        """

        new_head = ListNode(0)
        new_head.next = head

        left = new_head
        now = head
        cnt = 0
        start = None
        while now:
            cnt += 1
            if cnt == 1:
                start = now
                now = now.next
            elif cnt == k:
                right = now.next
                left.next = now
                left = start
                last_one = right
                while start != now:
                    tmp = start
                    start = start.next
                    tmp.next = last_one
                    last_one = tmp
                now = start.next
                start.next = last_one
                cnt = 0
            else:
                now = now.next

        return new_head.next
```
