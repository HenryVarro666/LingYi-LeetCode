---
title: "23. 合并K个排序链表"
aliases: ["yiduobo的每日leetcode 23.合并K个排序链表"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/divide-and-conquer", "leetcode/heap-priority-queue", "leetcode/bian-li", "题单/常用数据结构", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/常用数据结构/五-堆-优先队列", "题单/链表-二叉树与回溯/一-链表", "题单/LeetCode-热题-100/链表", "题单/面试经典-150-题/分治"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/116101679"
zhihu_id: "116101679"
zhihu_title: "yiduobo的每日leetcode 23.合并K个排序链表"
question_id: "23"
question: "合并 K 个升序链表"
problem_url: "https://leetcode.cn/problems/merge-k-sorted-lists/"
difficulty: "Hard"
created: "2020-03-24T23:42:10+08:00"
updated: "2020-03-24T23:42:10+08:00"
upvotes: 0
comments: 0
---

# 23. 合并K个排序链表

> **[yiduobo的每日leetcode 23.合并K个排序链表](https://zhuanlan.zhihu.com/p/116101679) · 知乎 · 2020-03-24 · 赞同 0**
> 力扣：[23. 合并 K 个升序链表](https://leetcode.cn/problems/merge-k-sorted-lists/) · Hard · 灵茶山艾府：[三种方法：最小堆/分治/迭代（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

23.合并K个排序链表<https://leetcode-cn.com/problems/merge-k-sorted-lists/>

经典的数据结构题，考察对于“堆”的运用。堆是一种完全二叉树，且对于任意节点，其左儿子和右儿子都满足一定的条件。

在这里我们运用的是小根堆，即对于任意节点p，都满足左儿子p_left_son和右儿子p_right_son的值都大于p，那么就可以确定，以p为根的子树中，p一定是最小的那个节点，因此获取最小节点的复杂度是O(1)的。

由于这是一棵完全二叉树，因此对于一个有n个节点的堆，其高度为logn，所以堆的插入与删除操作复杂度都是O(logn)。

回到题目上来，K路的归并我们可以维护一个小根堆，堆中存放这K个链表的头部。

接下来我们从堆中取出最小的节点，将其加入答案。

再然后我们将这个节点从堆中删去，并将其所在链表的下一个节点加入到堆当中。重复这个过程直到没有节点为止。

以上这个过程可以保证，每次从堆中取出来的节点都是当前剩下的节点中最小的那个，因此能保证合并结果的正确。整个过程需要操作n次，n为总的节点数量，每次操作需要进行一次插入和删除操作，复杂度都是logK，因此最后总的时间复杂度为O(nlogK)。

另外这个问题还可以用后缀数组倍增的思路进行两两合并，这里就不再展开了。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

from Queue import PriorityQueue

class Solution(object):
    def mergeKLists(self, lists):
        """
        :type lists: List[ListNode]
        :rtype: ListNode
        """
         
        head = ListNode(0)
        now = head

        heap = PriorityQueue()
        for l in lists:
            if l is not None:
                heap.put((l.val, l))

        while not heap.empty():
            min_val, min_node = heap.get()
            now.next = min_node
            if min_node.next:
                heap.put((min_node.next.val, min_node.next))
            min_node.next = None
            now = min_node
            
        return head.next
```
