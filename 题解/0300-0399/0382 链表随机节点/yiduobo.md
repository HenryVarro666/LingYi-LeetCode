---
title: "382. 链表随机节点"
aliases: ["yiduobo的每日leetcode 382.链表随机节点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/166411338"
zhihu_id: "166411338"
zhihu_title: "yiduobo的每日leetcode 382.链表随机节点"
question_id: "382"
question: "链表随机节点"
problem_url: "https://leetcode.cn/problems/linked-list-random-node/"
created: "2020-08-03T20:57:21+08:00"
updated: "2020-08-03T20:57:21+08:00"
upvotes: 0
comments: 0
---

# 382. 链表随机节点

> **[yiduobo的每日leetcode 382.链表随机节点](https://zhuanlan.zhihu.com/p/166411338) · 知乎 · 2020-08-03 · 赞同 0**
> 力扣：[382. 链表随机节点](https://leetcode.cn/problems/linked-list-random-node/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

382.链表随机节点<https://leetcode-cn.com/problems/linked-list-random-node/submissions/>

就简单的思路自然是将链表转化为数组，然后通过数组下标实现O(1)的随机取。

不过当链表长度未知且只能用常数空间，那么就只能通过一趟遍历的做法来实现了。不妨设当前是链表中的第k个节点，那么在不知道后续还有没有节点的情况下，我们需要想办法让每个节点取到的可能性为1/k。

在这个假设的前提下，我们可以认为在前k - 1个节点做完后已经从前k - 1个节点中，通过某种方法以1/(k - 1)的概率取到了某个节点。那么对于这个节点以及第k个节点，都应该有1/k的概率被取出来。此时如果按1/k的几率取第k个节点，而按(k - 1)/k的概率取前k - 1个节点得到的那个节点，那么两种情况下的概率分别为1/k与1/(k - 1) \* (k - 1) / k \= 1/k，恰好符合我们的要求。

于是到了这里，就可以一趟扫描，每次按当前节点总数分之一的概率，决定是否用当前节点替代答案节点。

上面算法是经典的蓄水池算法，与之类似的还有扑克牌的洗牌算法。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):

    def __init__(self, head):
        """
        @param head The linked list's head.
        Note that the head is guaranteed to be not null, so it contains at least one node.
        :type head: ListNode
        """
        self.head = head

    def getRandom(self):
        """
        Returns a random node's value.
        :rtype: int
        """
        cnt = 0
        ret = None

        now = self.head
        while now:
            if random.randint(0, cnt) == 0:
                ret = now.val
            cnt += 1
            now = now.next

        return ret

# Your Solution object will be instantiated and called as such:
# obj = Solution(head)
# param_1 = obj.getRandom()
```
