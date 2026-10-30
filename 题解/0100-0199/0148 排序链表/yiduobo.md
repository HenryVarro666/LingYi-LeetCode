---
title: "148. 排序链表"
aliases: ["yiduobo的每日leetcode 148.排序链表"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/divide-and-conquer", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/一-链表", "题单/LeetCode-热题-100/链表", "题单/面试经典-150-题/分治"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/142921084"
zhihu_id: "142921084"
zhihu_title: "yiduobo的每日leetcode 148.排序链表"
question_id: "148"
question: "排序链表"
problem_url: "https://leetcode.cn/problems/sort-list/"
difficulty: "Medium"
created: "2020-05-22T22:40:25+08:00"
updated: "2020-05-22T22:40:25+08:00"
upvotes: 0
comments: 0
---

# 148. 排序链表

> **[yiduobo的每日leetcode 148.排序链表](https://zhuanlan.zhihu.com/p/142921084) · 知乎 · 2020-05-22 · 赞同 0**
> 力扣：[148. 排序链表](https://leetcode.cn/problems/sort-list/) · Medium · 灵茶山艾府：[两种方法：分治/迭代，模块化设计，代码可读性高（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

148.排序链表<https://leetcode-cn.com/problems/sort-list/>

题目要求O(nlogn)的时间复杂度与O(1)的空间复杂度，那么需要递归的，例如快排、归并，或者需要额外空间的，例如堆排都不能达成要求。在这里，可以运用倍增的思想，逐步归并排序。其主要思路为设置步长step，每次从头开始划分出两个长度为step的部分进行归并，然后倍增step直到step大于等于链表长度。

以样例为例子说明：

样例一中，初始状态为

4 2 1 3

此时step为1，那么此时的划分为4与2归并，1与3，得到

2 4

1 3

接下来倍增step\=2，那么此时的划分为[2, 4]与[1, 3]归并，得到

1 2 3 4

即为最后的答案

样例二中，初始状态为

-1 5 3 4 0

此时step为1，那么此时的划分为-1与5归并，3与4归并，剩下0不进行操作，得到

-1 5

3 4

0

接下来倍增step\=2，那么此时的划分为[-1, 5]与[3, 4]归并，剩下0依然不进行操作，得到

-1 3 4 5

0

最后倍增step\=4，那么此时的划分为[-1, 3, 4, 5]与[0]归并，得到

-1 0 3 4 5

即为最后答案

每一次操作，链表中的所有数字都需要执行一次归并，于是一趟的时间复杂度为O(n)。

step在logn的次数内就能增长到n，于是只需要执行logn次操作，因此最终的时间复杂度为O(nlogn)。

过程中只需要链表操作的空间，因此空间复杂度为O(1)。

具体实现中，也还是先加入一个假头p_head方便计算。

接下来设已经完成排序的部分的最后一个节点为last_node，那么last_node的初始值为p_head。那么每次归并的第一个部分的头部part1一定就是last_node.next。

设now等于last_node，那么将now往后移动step位之后，now.next就是第二部分的头部part2。

接下来从part1与part2开始执行长度为step的归并排序，同时调整last_node的位置。

在完成这一次排序后，如果last_node后面还有节点，那么继续上面的操作，否则就倍增step，然后将last_node指回到p_head开始下一轮的操作。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def sortList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """

        if not head:
            return head

        p_head = ListNode(0)
        p_head.next = head

        now = head
        l = 0
        while now:
            l += 1
            now = now.next

        step = 1
        while step < l:
            last_node = p_head
            while last_node.next:
                part1 = last_node.next
                now = last_node
                l1 = 0
                while l1 < step and now.next:
                    l1 += 1
                    now = now.next
                if not now.next:
                    break

                part2 = now.next
                l2 = 0
                while l2 < step and now.next:
                    l2 += 1
                    now = now.next
                    
                next_part = now.next

                cnt1 = cnt2 = 0
                while cnt1 < l1 or cnt2 < l2:
                    choose_one = True
                    if cnt1 == l1 or ((cnt2 != l2) and (part1.val > part2.val)):
                        choose_one = False

                    if choose_one:
                        last_node.next = part1
                        last_node = part1
                        part1 = part1.next
                        cnt1 += 1
                    else:
                        last_node.next = part2
                        last_node = part2
                        part2 = part2.next
                        cnt2 += 1

                last_node.next = next_part

            step += step

        return p_head.next
```
