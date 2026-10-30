---
title: "3636. 查询超过阈值频率最高元素"
aliases: ["yiduobo的每日leetcode 3636.查询超过阈值频率最高元素"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/binary-search", "leetcode/sorting", "leetcode/bao-li", "题单/常用数据结构", "题单/常用数据结构/十一-根号算法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1947061655025460091"
zhihu_id: "1947061655025460091"
zhihu_title: "yiduobo的每日leetcode 3636.查询超过阈值频率最高元素"
question_id: "3636"
question: "查询超过阈值频率最高元素"
problem_url: "https://leetcode.cn/problems/threshold-majority-queries/"
difficulty: "Hard"
rating: 2451
created: "2025-09-05T00:56:16+08:00"
updated: "2025-09-05T00:56:16+08:00"
upvotes: 1
comments: 0
---

# 3636. 查询超过阈值频率最高元素

> **[yiduobo的每日leetcode 3636.查询超过阈值频率最高元素](https://zhuanlan.zhihu.com/p/1947061655025460091) · 知乎 · 2025-09-05 · 赞同 1**
> 力扣：[3636. 查询超过阈值频率最高元素](https://leetcode.cn/problems/threshold-majority-queries/) · Hard · 灵茶山艾府：[莫队算法（回滚莫队）Python/Java/C++/Go](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3636.查询超过阈值频率最高元素

[3636. 查询超过阈值频率最高元素 - 力扣（LeetCode）](https://leetcode.cn/problems/threshold-majority-queries/description/)

题目给出一个长度为n的整数数组nums和一个查询数组queries，其中queries\[index\] \= \[left\[index\], right\[index\], threshold\[index\]\]。nums的长度不超过10000，queries的长度不超过50000。

要求返回一个整数数组ans，其中ans\[index\]等于子数组nums\[left\[index\] ... right\[index\]\]中，出现至少threshold\[index\]次的元素，选择频率最高的元素，如果频率相同，则选择最小的元素。若不存在，则返回-1。

题目可以理解成给出若干区间，问这些区间的众数是什么。对于这个问题，常规的最值形区间数据结构就不太好用了，因为对于一个大区间而言，要想知道这个区间的众数，就不能丢失任何小区间的信息。更具体的说，如果小区间不记录每种元素出现的次数，就无法得到大区间中每种元素出现的次数，也就无法知道众数是什么了。

对于这类多个区间求解的问题，另一种思路就是使用之前3590题中用过的莫队算法进行求解。

[yiduobo的每日leetcode 3590.第K小的路径异或和](https://zhuanlan.zhihu.com/p/1939489676860823544)

对于本题，同样是将所有的查询区间按照大小b \= sqrt(n)进行分块，接下来将这些区间按照所在块数为第一关键字，区间右边界为第二关键字进行排序。

到了这里，如果按照常规的莫队算法，就是设置一个nowx和nowy，然后遍历所有区间，让nowx和nowy逐步向当前遍历到的区间靠拢，并在这个过程中更新区间的众数。对于区间众数，如果只需要知道任意出现次数最多的数中的任意一个，那么就可以利用类似lfu cache的数据结构，在O(1)的时间内完成增删，同时更新区间众数。但是本题在此基础上还需要知道众数中数值最小的那一个，需要保序，那么在这里就必须使用懒更新的堆这类数据结构，时间复杂度来到了O(logn)。再结合莫队算法遍历区间的复杂度，整体的时间复杂度是比较紧张的。

除此之外，另一种处理方法就是回滚莫队了。回滚莫队是指的对于同一块中的区间，由于右边界有序，那么按照顺序遍历时可以正常扩展右边界，而左边界间的差异不会超过块的大小，因此可以每次从块的末尾往回，完整的扩展到当前的左边界，计算完当前区间后再回滚回去，消除掉左边界这一段元素的影响。需要注意的是，为了能有效进行左边界的扩展，需要保证有右边界都在块的分界线后面，而对于右边界在块的分界线前面的区间，则可以直接暴力计算。

更形式化的说，对于一个区间(x, y)，其所属的块应该是x // b，而这个块包含的区间，其左边界都必然位于块的起点(x // b - 1) \* b以及块的终点x // b \* b - 1之间。如果区间右边界在位于其中，那么直接暴力计算。对于这类区间，暴力计算的复杂度不超过块的大小，也就是O(B)。反之，如果区间右边界在块的终点右侧，那么对于右边界就可以正常进行扩展。由于右边界是有序的，因此在O(n)的时间内就可以完成当前块中所有区间右边界的扩展，一共是B个块，因此总的时间复杂度不超过O(nB)。而对于这些区间的左边界x，则需要每次都从终点x // b \* b - 1开始，向前一步一步扩展到x，计算完成后，再一步步缩回到块的终点，消除这些元素的影响。由于块中区间的左边界与块终点的距离不超过B，因此单词扩展并缩回的事件复杂度也是O(B)。这样一来，就可以在O((n + q)B)的时间内完成所有运算了。

到了这里，还剩下最后一个问题：在区间左边界缩回的过程中如何维护众数。对于众数的计算，在遍历的语境下通常是使用哈希表记录每种元素出现的次数，然后当某个元素的次数获得增加，并且当前出现的次数变得大于当前的众数时，就将其众数更新为这个元素。对于这个操作，在区间扩展时是没有任何问题的，但是当区间缩回时，若当前众数的出现次数因为缩回操作变少时，要确定新的众数就不容易了。

不过好在本题有一个特殊的前提，就是右边界的扩展在块中一直有效，而左边界的扩展和收缩都是基于块终点计算的，那么在这里就可以使用两个变量记录当前区间仅扩展完右边界时的众数以及出现的次数，接下来在左边界扩展前先记录一个副本，然后照常扩展左边界并更新当前区间的答案，扩展完成后在收缩时，就只需要更新记录每种元素出现次数的哈希表，而最终收缩完后的众数以及出现的次数，就可以直接通过扩展前记录的副本得到了，这样一来，就避开了收缩时众数产生变化的问题。

另外需要特别注意的是，若当前询问的左边界不再属于上一个块，那么就需要重新确定当前块的边界，同时之前块中通过右边界扩展出来的结果，包括记录每种元素出现次数的哈希表都不能再用了，必须重新计算。

最后附上python代码：

```python
class Solution(object):
    def subarrayMajority(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        cnt = {}
        ma = 0
        mi = 0

        b = int(len(nums) ** 0.5)
        if b == 0:
            b = 1
        q = sorted([[x, y, threshold, index] for index, (x, y, threshold) in enumerate(queries)], key=lambda d: (d[0] // b, d[1]))
        res = [-1] * len(q)
        
        nowb = -1
        nowy = -1
        for x, y, threshold, index in q:
            if nowb != x // b:
                block_end = (x // b + 1) * b - 1
                if y <= block_end:
                    cnt = {}
                    ma, mi = 0, 0
                    for v in nums[x : y + 1]:
                        cnt[v] = cnt.get(v, 0) + 1
                        if cnt[v] > ma or (cnt[v] == ma and v < mi):
                            ma, mi = cnt[v], v

                    if ma >= threshold:
                        res[index] = mi
                    continue
                
                nowb = x // b
                nowy = block_end
                cnt = {}
                ma, mi = 0, 0

            for v in nums[nowy + 1: y + 1]:
                cnt[v] = cnt.get(v, 0) + 1
                if cnt[v] > ma or (cnt[v] == ma and v < mi):
                    ma, mi = cnt[v], v
            nowy = y

            ori_ma, ori_mi = ma, mi
            for v in nums[x : block_end + 1]:
                cnt[v] = cnt.get(v, 0) + 1
                if cnt[v] > ma or (cnt[v] == ma and v < mi):
                    ma, mi = cnt[v], v

            if ma >= threshold:
                res[index] = mi
            for v in nums[x : block_end + 1]:
                cnt[v] -= 1
            ma, mi = ori_ma, ori_mi
        
        return res
```
