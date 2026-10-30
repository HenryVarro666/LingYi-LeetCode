---
title: "3063. 链表频率"
aliases: ["yiduobo的每日leetcode 3063.链表频率"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/696676581"
zhihu_id: "696676581"
zhihu_title: "yiduobo的每日leetcode 3063.链表频率"
question_id: "3063"
question: "链表频率"
problem_url: "https://leetcode.cn/problems/linked-list-frequency/"
created: "2024-05-09T03:01:45+08:00"
updated: "2024-05-09T03:01:45+08:00"
upvotes: 1
comments: 0
---

# 3063. 链表频率

> **[yiduobo的每日leetcode 3063.链表频率](https://zhuanlan.zhihu.com/p/696676581) · 知乎 · 2024-05-09 · 赞同 1**
> 力扣：[3063. 链表频率](https://leetcode.cn/problems/linked-list-frequency/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3063.链表频率

[. - 力扣（LeetCode）](https://leetcode.cn/problems/linked-list-frequency/)

先对链表进行一趟遍历，使用哈希表统计链表中每种数出现的频率，接下来再对这些频率进行一趟遍历，构造出答案链表即可。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def frequenciesOfElements(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """

        freq = Counter()
        now = head
        while now:
            freq[now.val] += 1
            now = now.next
        
        res = ListNode()
        now = res
        for f in freq.values():
            now.next = ListNode(f)
            now = now.next
        
        return res.next
```
