---
title: "3263. 将双链表转换为数组I & 3294. 将双链表转换为数组II"
aliases: ["yiduobo的每日leetcode 3263.将双链表转换为数组I && 3294.将双链表转换为数组II", "3263. 将双链表转换为数组I", "3294. 将双链表转换为数组II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/739114712"
zhihu_id: "739114712"
zhihu_title: "yiduobo的每日leetcode 3263.将双链表转换为数组I && 3294.将双链表转换为数组II"
question_id: ["3263", "3294"]
question: ["将双链表转换为数组I", "将双链表转换为数组II"]
problem_url: ["https://leetcode.cn/problems/convert-doubly-linked-list-to-array-i/", "https://leetcode.cn/problems/convert-doubly-linked-list-to-array-ii/"]
created: "2024-09-27T21:23:01+08:00"
updated: "2024-09-27T21:23:01+08:00"
upvotes: 2
comments: 0
---

# 3263. 将双链表转换为数组I & 3294. 将双链表转换为数组II

> **[yiduobo的每日leetcode 3263.将双链表转换为数组I && 3294.将双链表转换为数组II](https://zhuanlan.zhihu.com/p/739114712) · 知乎 · 2024-09-27 · 赞同 2**
> 力扣：[3263. 将双链表转换为数组I](https://leetcode.cn/problems/convert-doubly-linked-list-to-array-i/)
> 力扣：[3294. 将双链表转换为数组II](https://leetcode.cn/problems/convert-doubly-linked-list-to-array-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3263.将双链表转换为数组I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/convert-doubly-linked-list-to-array-i/description/)

3294.将双链表转换为数组II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/convert-doubly-linked-list-to-array-ii/description/)

3263题是给出一个双链表的头结点head，要求将链表中的元素按顺序填充到答案数组中。

3294题则是给出双链表中的任意节点node，同样是要求将链表中的元素按顺序填充到答案数组中。

对于3263题，只需从头结点开始不断向后迭代，若当前head非空，那么就将其对于的元素加入到答案数组中。

对于3294题，则只需要先将node往前迭代到链表的头节点，然后再按3263题的方法处理就行了。

最后附上python代码：

3263:

```python
"""
# Definition for a Node.
class Node:
    def __init__(self, val, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next
"""

class Solution:
    def toArray(self, head):
        """
        :type head: Node
        :rtype: List[int]
        """

        res = []
        while head:
            res.append(head.val)
            head = head.next
        
        return res
```

3294:

```
"""
# Definition for a Node.
class Node:
    def __init__(self, val, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next
"""

class Solution:
    def toArray(self, node):
        """
        :type head: Node
        :rtype: List[int]
        """

        now = node
        while now.prev:
            now = now.prev
        
        res = []
        while now:
            res.append(now.val)
            now = now.next
        
        return res
```
