---
title: "1019. 链表中的下一个更大节点"
aliases: ["yiduobo的每日leetcode 1019.链表中的下一个更大节点"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/linked-list", "leetcode/monotonic-stack", "题单/链表-二叉树与回溯", "题单/单调栈", "题单/链表-二叉树与回溯/一-链表", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/368361503"
zhihu_id: "368361503"
zhihu_title: "yiduobo的每日leetcode 1019.链表中的下一个更大节点"
question_id: "1019"
question: "链表中的下一个更大节点"
problem_url: "https://leetcode.cn/problems/next-greater-node-in-linked-list/"
difficulty: "Medium"
rating: 1571
created: "2021-04-27T21:46:37+08:00"
updated: "2021-04-27T21:46:37+08:00"
upvotes: 0
comments: 0
---

# 1019. 链表中的下一个更大节点

> **[yiduobo的每日leetcode 1019.链表中的下一个更大节点](https://zhuanlan.zhihu.com/p/368361503) · 知乎 · 2021-04-27 · 赞同 0**
> 力扣：[1019. 链表中的下一个更大节点](https://leetcode.cn/problems/next-greater-node-in-linked-list/) · Medium · 灵茶山艾府：[【图解单调栈】两种方法，两张图秒懂！附题单（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1019.链表中的下一个更大节点

[力扣](https://leetcode-cn.com/problems/next-greater-node-in-linked-list/)

对于链表这种数据结构而言，比较方便的遍历方式只有从头开始向后遍历，那么我们应该以这个为前提来设计算法。

假设我们现在处理的是一个数组，然后从头开始向后遍历。对于当前的num[index]，其可能是之前num[0]到num[index - 1]的下一个更大节点，而num[index]本身的下一个更大节点则需要继续向后遍历才能知道，因此很自然想到使用某种数据结构将还没有找到答案的位置给保存下来。

由于是从头向后扫描，那么保存下来的还没找到答案的这些位置上的数必然是单调不增的，即对于位置i和j而言，若i \< j且位置i上的数还没找到答案，那么必然有num[i] >\= num[j]，否则num[i]的答案就是num[j]了。

这样一来，很自然就想到使用单调栈来维护这些没有找到答案的位置。于是现在的做法就是对于当前的num[index]，若当前栈非空且栈顶元素小于num[index]，那么就将栈顶元素对应的答案就是num[index]，同时将栈顶元素弹出。重复该过程直到栈为空或者栈顶元素大于等于num[index]。接下来将num[index]压入栈中然后继续向后处理num[index+ 1]即可。

遍历完成后，栈中剩下的元素都是找不到答案的，那么将对应的位置上设为0即可。

回到本题，除了遍历的方式从数组的遍历变成了链表的遍历之外，其他做法与上面的做法完全一致。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def nextLargerNodes(self, head):
        """
        :type head: ListNode
        :rtype: List[int]
        """
        
        stack = []
        res = []

        now = head
        l = 0
        while now:
            res.append(0)
            while stack and stack[-1][0] < now.val:
                res[stack[-1][1]] = now.val
                stack.pop()
            stack.append([now.val, l])
            now = now.next
            l += 1

        return res
```
