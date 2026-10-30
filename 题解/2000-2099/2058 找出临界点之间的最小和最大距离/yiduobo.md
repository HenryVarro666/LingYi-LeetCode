---
title: "2058. 找出临界点之间的最小和最大距离"
aliases: ["yiduobo的每日leetcode 2058.找出临界点之间的最小和最大距离"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/一-链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/513562991"
zhihu_id: "513562991"
zhihu_title: "yiduobo的每日leetcode 2058.找出临界点之间的最小和最大距离"
question_id: "2058"
question: "找出临界点之间的最小和最大距离"
problem_url: "https://leetcode.cn/problems/find-the-minimum-and-maximum-number-of-nodes-between-critical-points/"
difficulty: "Medium"
created: "2022-05-12T23:52:08+08:00"
updated: "2022-05-12T23:52:09+08:00"
upvotes: 0
comments: 0
---

# 2058. 找出临界点之间的最小和最大距离

> **[yiduobo的每日leetcode 2058.找出临界点之间的最小和最大距离](https://zhuanlan.zhihu.com/p/513562991) · 知乎 · 2022-05-12 · 赞同 0**
> 力扣：[2058. 找出临界点之间的最小和最大距离](https://leetcode.cn/problems/find-the-minimum-and-maximum-number-of-nodes-between-critical-points/) · Medium · 灵茶山艾府：[记录临界点的位置（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2058.找出临界点之间的最小和最大距离

[力扣](https://leetcode.cn/problems/find-the-minimum-and-maximum-number-of-nodes-between-critical-points/)

首先，题目关于局部极小值和局部极大值都涉及到某个节点的前驱和后继节点，在单链表中，找到某个节点的后继节点是很容易的，但是没有办法直接找到某个节点的前驱节点，因此需要使用一个遍历last记录当前节点的上一个节点。

接下来就只需要一趟遍历，对于当前遍历到的节点now，对比last、now、now.next三者的值来判断now是否是一个极值点。判断完now之后，将last更新为now，将now更新为now.next然后继续向后求解。这样一来，就可以通过一趟遍历找出链表中的所有极值点。

题目要求的是两个极值点之间的最小距离和最大距离。很明显，这里的最小距离必然出现在两个相邻的极值点之间，而最大距离则必然就是第一个极值点和最后一个极值点之间的距离，因此在求解极值点的过程中，还需要使用三个变量pos、first_pos和last_pos，分别表示当前节点now是链表中的第几个点、第一个极值点下标以及最后一个极值点的下标。

若当前节点now是一个极值点，那么就使用pos - first_pos和pos - last_pos分别更新最大距离和最小距离，然后将last_pos更新为pos。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def nodesBetweenCriticalPoints(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: List[int]
        """

        first_pos = last_pos = None

        last = head
        now = head.next
        pos = 1

        res = [100000, -1]
        while now.next:
            if (now.val > last.val and now.val > now.next.val) or (now.val < last.val and now.val < now.next.val):
                if first_pos is None:
                    first_pos = pos
                else:
                    res[0] = min(res[0], pos - last_pos)
                    res[1] = max(res[1], pos - first_pos)

                last_pos = pos

            last, now = now, now.next
            pos += 1

        if res[0] == 100000:
            res[0] = -1
        
        return res
```
