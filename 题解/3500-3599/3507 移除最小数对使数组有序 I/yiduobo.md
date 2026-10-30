---
title: "3507. 移除最小数对使数组有序I & 3510. 移除最小数对使数组有序II"
aliases: ["yiduobo的每日leetcode 3507.移除最小数对使数组有序I && 3510.移除最小数对使数组有序II", "3507. 移除最小数对使数组有序I", "3510. 移除最小数对使数组有序II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/ordered-set", "leetcode/simulation", "leetcode/heap-priority-queue", "leetcode/hard", "leetcode/linked-list", "leetcode/doubly-linked-list", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1902165511070019822"
zhihu_id: "1902165511070019822"
zhihu_title: "yiduobo的每日leetcode 3507.移除最小数对使数组有序I && 3510.移除最小数对使数组有序II"
question_id: ["3507", "3510"]
question: ["移除最小数对使数组有序 I", "移除最小数对使数组有序 II"]
problem_url: ["https://leetcode.cn/problems/minimum-pair-removal-to-sort-array-i/", "https://leetcode.cn/problems/minimum-pair-removal-to-sort-array-ii/"]
difficulty: ["Easy", "Hard"]
rating: 2608
created: "2025-05-04T01:22:42+08:00"
updated: "2025-05-04T01:22:59+08:00"
upvotes: 0
comments: 0
---

# 3507. 移除最小数对使数组有序I & 3510. 移除最小数对使数组有序II

> **[yiduobo的每日leetcode 3507.移除最小数对使数组有序I && 3510.移除最小数对使数组有序II](https://zhuanlan.zhihu.com/p/1902165511070019822) · 知乎 · 2025-05-04 · 赞同 0**
> 力扣：[3507. 移除最小数对使数组有序 I](https://leetcode.cn/problems/minimum-pair-removal-to-sort-array-i/) · Easy · 灵茶山艾府：[O(nlogn) 非暴力做法（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3510. 移除最小数对使数组有序 II](https://leetcode.cn/problems/minimum-pair-removal-to-sort-array-ii/) · Hard · 灵茶山艾府：[两种方法：两个有序集合 / 懒删除堆+数组模拟双向链表（Python/Java/C++/Go）](../3510%20移除最小数对使数组有序%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3507.移除最小数对使数组有序I

[3507. 移除最小数对使数组有序 I - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-pair-removal-to-sort-array-i/description/)

3510.移除最小数对使数组有序II

[3510. 移除最小数对使数组有序 II - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-pair-removal-to-sort-array-ii/description/)

题目给出一个数组nums，现在要求对其执行若干次操作，直到数组变为非递减。

每次操作中，需要从nums中选出一对和最小的相邻数对，如果存在多对则选择下标最小的那一对，然后用这两个数的和替换掉这对元素。

问需要执行多少次操作。

两题的题设一致，第二题的数据规模较大，nums的长度可达10^5。

由于每次操作都会使得数组的长度减1，因此总的操作次数不会超过数组的长度n，可以考虑直接模拟整个操作过程。对nums进行一趟遍历，统计其中的逆序对数目desc。若desc大于0，则不断执行操作，直到desc等于0为止。每轮操作可以分为两步，分别是找出和最小的相邻数对的下标，以及使用数对之和替换这两个元素。

对于找最小和这一步，这是一个动态全局最小值问题，可以使用堆来处理。具体来说，对于所有在0到n - 2之间的下标index，可以使用一个堆来储存数对和以及下标形成的二元组(nums[index] + nums[index + 1], index)。接下来的每轮操作，只需取出堆顶的二元组然后执行操作就行了。需要注意的是，中途存在数对和替换相邻元素的操作，那么在修改后一方面需要删去与被合并元素有关的二元组，一方面还需要将新的二元组加入到堆中。对于删除操作依然可以使用懒删除的处理方法，若堆顶的二元组与当前剩下的nums不符，那么说明堆顶的二元素已经失效，无需处理。而对于添加新的二元组，则需要知道当前nums中的元素是如何排布的。

另一方面，对于使用数对和替换相邻元素对的操作，则可以认为是将后面这个元素值累积到前面这个元素中，然后将后面这个元素从数组中删去。在删除操作执行后，元素间的相对位置会产生变化，但是变化的跨度不大，因此在这里可以使用两个数组pre和nxt分别记录每个元素在当前数组中的前一个元素和后一个元素在原始nums中的下标。具体来说，pre\[index\]表示在原始数组中下标为index的元素，在当前数组中的前一个元素在原始nums中的下标，nxt\[index\]则表示后一个元素在原始nums中的下标，那么对于在原始下标为index处的元素执行的合并操作，只需将nums\[nxt\[index\]\]累加到nums\[index\]，然后通过修改pre和nxt数组，将index\<->nxt\[index\]\<->nxt\[nxt\[index\]\]的链接修改为index\<->nxt\[nxt\[index\]\]即可，类似于在链表中删除nxt\[index\]这个节点。这样一来，不仅处理了替换操作，也可以很方便地将新的元素和添加到堆中。

另外在每次合并操作时，不要忘了通过nums\[pre\[index\]\]、nums\[index\]、nums\[nxt\[index\]\]、nums\[nxt\[nxt\[index\]\]\]这三组相邻元素对的大小关系，以及nums\[pre\[index\]\]、nums\[index\] + nums\[nxt\[index\]\]、nums\[nxt\[nxt\[index\]\]这两组相邻元素的大小关系来更新desc。

最后附上python代码：

```python
class Solution(object):
    def minimumPairRemoval(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        heap = []
        n = len(nums)
        pre = [None] * n
        nxt = [None] * n
        s = [0] * n

        desc = 0
        for index in range(n):
            if index > 0:
                pre[index] = index - 1
            if index < n - 1:
                nxt[index] = index + 1
                heapq.heappush(heap, (nums[index] + nums[index + 1], index))
                if nums[index] > nums[index + 1]:
                    desc += 1
        
        res = 0
        while desc > 0:
            v, index = heapq.heappop(heap)
            if nums[index] is not None and nxt[index] is not None and nums[index] + nums[nxt[index]] == v:
                res += 1
                if nums[index] > nums[nxt[index]]:
                    desc -= 1
                
                if nxt[nxt[index]] is not None and nums[nxt[index]] > nums[nxt[nxt[index]]]:
                    desc -= 1
                
                if pre[index] is not None and nums[pre[index]] > nums[index]:
                    desc -= 1

                nums[index] += nums[nxt[index]]
                nums[nxt[index]] = None

                if nxt[nxt[index]] is not None:
                    pre[nxt[nxt[index]]] = index
                    nxt[index] = nxt[nxt[index]]

                    if nums[index] > nums[nxt[index]]:
                        desc += 1
                    
                    heapq.heappush(heap, (nums[index] + nums[nxt[index]], index))
                else:
                    nxt[index] = None

                if pre[index] is not None:
                    if nums[pre[index]] > nums[index]:
                        desc += 1
                    
                    heapq.heappush(heap, (nums[pre[index]] + nums[index], pre[index]))

        return res
```
