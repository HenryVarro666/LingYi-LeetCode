---
title: "3062. 链表游戏的获胜者"
aliases: ["yiduobo的每日leetcode 3062.链表游戏的获胜者"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/696676538"
zhihu_id: "696676538"
zhihu_title: "yiduobo的每日leetcode 3062.链表游戏的获胜者"
question_id: "3062"
question: "链表游戏的获胜者"
problem_url: "https://leetcode.cn/problems/winner-of-the-linked-list-game/"
created: "2024-05-09T03:00:10+08:00"
updated: "2024-05-09T03:00:10+08:00"
upvotes: 1
comments: 0
---

# 3062. 链表游戏的获胜者

> **[yiduobo的每日leetcode 3062.链表游戏的获胜者](https://zhuanlan.zhihu.com/p/696676538) · 知乎 · 2024-05-09 · 赞同 1**
> 力扣：[3062. 链表游戏的获胜者](https://leetcode.cn/problems/winner-of-the-linked-list-game/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3062.链表游戏的获胜者

[. - 力扣（LeetCode）](https://leetcode.cn/problems/winner-of-the-linked-list-game/description/)

题目保证的链表长度为偶数，那么只需从链表头开始以步长为2向后移动，每次对比当前节点与下一个节点的值的大小即可。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def gameResult(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: str
        """

        now = head
        diff = 0
        while now:
            if now.val > now.next.val:
                diff += 1
            elif now.val < now.next.val:
                diff -= 1
            
            now = now.next.next
        
        if diff > 0:
            return "Even"
        elif diff < 0:
            return "Odd"
        else:
            return "Tie"
```
