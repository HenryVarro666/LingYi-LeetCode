---
title: "725. 分隔链表"
aliases: ["yiduobo的每日leetcode 725.分隔链表"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/334786398"
zhihu_id: "334786398"
zhihu_title: "yiduobo的每日leetcode 725.分隔链表"
question_id: "725"
question: "分隔链表"
problem_url: "https://leetcode.cn/problems/split-linked-list-in-parts/"
created: "2020-12-08T22:38:52+08:00"
updated: "2020-12-08T22:38:52+08:00"
upvotes: 0
comments: 0
---

# 725. 分隔链表

> **[yiduobo的每日leetcode 725.分隔链表](https://zhuanlan.zhihu.com/p/334786398) · 知乎 · 2020-12-08 · 赞同 0**
> 力扣：[725. 分隔链表](https://leetcode.cn/problems/split-linked-list-in-parts/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

725.分隔链表

[力扣](https://leetcode-cn.com/problems/split-linked-list-in-parts/)

题目要求将链表分隔成等长的k个部分，因此我们需要先从头往后走一趟，获取链表的总长度l，那么每个部分的长度就是part_l \= l / k，同时还会有l % k个节点逐个被分到靠前的l % k个部分。

有了part_l之后，我们从root开始，每次在答案数组中添加一个空的子数组，然后往后走part_l个节点，同时将这些节点加入这个空的子数组中，这样一共执行k轮。需要注意前l % k轮需要额外多往后走一个节点。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def splitListToParts(self, root, k):
        """
        :type root: ListNode
        :type k: int
        :rtype: List[ListNode]
        """

        now = root
        l = 0
        while now:
            l += 1
            now = now.next
        
        part_l = l / k
        l %= k

        now = root
        last = None
        res = []
        for _ in range(k):
            res.append(now)
            if last:
                last.next = None
            for _ in range(part_l):
                last = now
                now = now.next
            if l > 0:
                last = now
                now = now.next
                l -= 1
        
        return res
```
