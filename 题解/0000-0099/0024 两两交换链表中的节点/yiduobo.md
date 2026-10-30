---
title: "24. 两两交换链表中的节点"
aliases: ["yiduobo的每日leetcode 24.两两交换链表中的节点"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/recursion", "leetcode/linked-list", "leetcode/bian-li", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/链表-二叉树与回溯/一-链表", "题单/LeetCode-热题-100/链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/116109830"
zhihu_id: "116109830"
zhihu_title: "yiduobo的每日leetcode 24.两两交换链表中的节点"
question_id: "24"
question: "两两交换链表中的节点"
problem_url: "https://leetcode.cn/problems/swap-nodes-in-pairs/"
difficulty: "Medium"
created: "2020-03-25T00:04:01+08:00"
updated: "2020-03-25T00:04:01+08:00"
upvotes: 0
comments: 0
---

# 24. 两两交换链表中的节点

> **[yiduobo的每日leetcode 24.两两交换链表中的节点](https://zhuanlan.zhihu.com/p/116109830) · 知乎 · 2020-03-25 · 赞同 0**
> 力扣：[24. 两两交换链表中的节点](https://leetcode.cn/problems/swap-nodes-in-pairs/) · Medium · 灵茶山艾府：[【图解】迭代/递归，一张图秒懂！（Python/Java/C++/C/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

24.两两交换链表中的节点<https://leetcode-cn.com/problems/swap-nodes-in-pairs/>

链表操作的题目，需要注意的是，交换两个节点的时候，一般是

now - > node1 -> node2 -> right的形式，显然我们当前应该处于now，然后通过now.next, now.next.next以及now.next.next.next来对应node1，node2与right。**在这里需要特别注意的是，一旦靠前的节点产生变动，那么就无法根据next找到后面的节点了。**例如这里我们如果直接把now.next指向node2，那么我们就无法再定位到node1了，因此在交换的时候必须要注意顺序，并利用临时节点储存信息。

我在这里的处理顺序是

1、记录下node2为tmp，我们可以直接访问到的节点为now以及tmp。此时链接情况为：

now- > node1 -> node2(tmp) -> right

2、将node1的next指向right。此时的node1为now.next，right为tmp.next，因此具体操作为now.next.next \= tmp.next。此时链接情况为：

now- > node1 - > right

node2(tmp) - > right

3、将tmp的next指向node1。此时的node1为now.next，因此具体操作为tmp.next \= now.next。此时链接情况为：

now- > node1 - > right

node2(tmp) - > node1 - > right

4、将now的next指向tmp。now和tmp都可以直接访问，因此具体操作为now.next \= tmp。此时链接情况为：

left - > node2(tmp) - > node1 -> right

5、此时node1和node2交换已经完成了，我们跳到node1继续进行right以及之后的交换即可。此时的node1为tmp.next，因此具体操作为now \= tmp.next。

重复上述步骤直到链表不足两个节点即可，时间复杂度为O(n)，空间复杂度位O(1)。

另外，我们依然在链表头部加上一个假表头，方便充当最开始的now节点。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def swapPairs(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """

        new_head = ListNode(0)
        new_head.next = head

        now = new_head

        while now.next and now.next.next:
            tmp = now.next.next
            now.next.next = tmp.next
            tmp.next = now.next
            now.next = tmp
            now = tmp.next

        return new_head.next
```
