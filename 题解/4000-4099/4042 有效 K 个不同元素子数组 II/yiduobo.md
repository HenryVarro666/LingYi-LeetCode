---
title: "4042. 有效K个不同元素子数组II"
aliases: ["yiduobo的每日leetcode 4042.有效K个不同元素子数组II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/hash-table", "leetcode/random", "leetcode/sliding-window", "leetcode/randomized"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2079338774132176112"
zhihu_id: "2079338774132176112"
zhihu_title: "yiduobo的每日leetcode 4042.有效K个不同元素子数组II"
question_id: "4042"
question: "有效 K 个不同元素子数组 II"
problem_url: "https://leetcode.cn/problems/valid-k-unique-subarrays-ii/"
difficulty: "Hard"
created: "2026-09-04T22:54:48+08:00"
updated: "2026-09-04T22:55:05+08:00"
upvotes: 0
comments: 0
---

# 4042. 有效K个不同元素子数组II

> **[yiduobo的每日leetcode 4042.有效K个不同元素子数组II](https://zhuanlan.zhihu.com/p/2079338774132176112) · 知乎 · 2026-09-04 · 赞同 0**
> 力扣：[4042. 有效 K 个不同元素子数组 II](https://leetcode.cn/problems/valid-k-unique-subarrays-ii/) · Hard · 灵茶山艾府：[滑动窗口 + 异或哈希（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4042.有效K个不同元素子数组II

<https://leetcode.cn/problems/valid-k-unique-subarrays-ii/>

题目给出一个整数数组nums，以及一个整数k。其中nums的长度以及元素大小都不超过5 \* 10^5。

另外给出两个整数l0以及r0，定义了首个查询，以及一个整数q，表示需要处理的总查询数量。

对于一个子数组，若这个子数组中恰好包含k个不同的数字，且这些数字出现的次数都是偶数，那么就认为这个子数组是有效的。

对于查询0，需要计算nums[l0]到nums[r0]这一段子数组是否为有效的。接下来，对于每个index > 0：

- 若前一个查询的结果为true，那么令g[index - 1] \= l[index - 1] + r[index - 1]，否则令g[index - 1] \= r[index - 1] - l[index - 1]
- 计算l[index] \= (l[index] XOR g[index - 1]) % n, 以及r[index] \= (r[index - 1] XOR g[index - 1]) % n，其中XOR表示异或操作
- 若l[index] > r[index]，则交换二者

要求计算出这q个结果的答案。

之前4033题的加强版，不过本题的查询改成了强制在线，且数据规模较大。

[yiduobo的每日leetcode 4033.有效K个不同元素子数组I](https://zhuanlan.zhihu.com/p/2077905933565424935)

从复杂度角度而言，直接沿用之前的可持久化树的哈希方法应该是可以直接处理的，不过基于python中tuple的内存组织方式，可能出现超内存的情况。

在一般的认识中，一个整数占用的空位4字节，因此一个长度一百万的数组大小在4M左右。而对于tuple而言，如果将其大小理解成其中元素的数量乘以4，那么空间方面应该不会有问题，但是实际上，tuple除了其中所有元素的指针之外，还有头机构以及一些其他的内容。测试发现，一个两个元素的tuple大小远不止8字节，同时一个四元素的tuple大小也远小于两个元素的tuple的大小的两倍。

基于这一点，将原来的二叉树压缩成八叉树，即每个节点记录一个长度为8的tuple并进行哈希就是一种可行的平衡方案。这样一来，单个节点哈希的计算复杂度在理论上将变为原来的4倍，但是树中节点的数量则被压缩到了log8n，可以节省大量的空间。

最后附上python代码：

```python
class Solution(object):
    def validSubarrays(self, nums, k, l0, r0, q):
        """
        :type nums: List[int]
        :type k: int
        :type l0: int
        :type r0: int
        :type q: int
        :rtype: List[bool]
        """
        
        n = len(nums)

        freq1 = {}
        freq2 = {}
        hit_k = []
        p1 = 0
        p2 = 0
        for index, v in enumerate(nums):
            if p1 < index:
                p1 = index
            while p1 < len(nums) and len(freq1) < k:
                freq1[nums[p1]] = freq1.get(nums[p1], 0) + 1
                p1 += 1
            
            if len(freq1) < k:
                hit_k.append([-1, -1])
                continue

            if p2 < index:
                p2 = index
            while p2 < len(nums) and len(freq2) < k + 1:
                freq2[nums[p2]] = freq2.get(nums[p2], 0) + 1
                p2 += 1

            hit_k.append([p1, p2 - 1])

            freq1[v] -= 1
            if freq1[v] == 0:
                freq1.pop(v)
            freq2[v] -= 1
            if freq2[v] == 0:
                freq2.pop(v)

        vid = {}
        m = 0
        for v in nums:
            if v not in vid:
                vid[v] = m
                m += 1

        p = 1
        while p < m:
            p <<= 1

        f = [0] * (p << 1)
        length = p
        nxt_id = p << 1
        node_dict = {}
        root_flag = False
        pre_length = None
        while length:
            for index in range(length, length << 1):
                if length >= p:
                    f[index] = (index - length) << 1
                elif index == 1 and pre_length < 8:
                    if pre_length == 2:
                        key = (f[2], f[3])
                    elif pre_length == 4:
                        key = (f[4], f[5], f[6], f[7])
                    node_dict[key] = nxt_id
                    f[index] = nxt_id
                    nxt_id += 1
                else:
                    key = tuple([f[index << 3 | offset] for offset in range(8)])
                    node_dict[key] = nxt_id
                    f[index] = nxt_id
                    nxt_id += 1
            
            if length == 1:
                break

            pre_length = length
            if length >= 8:
                length >>= 3
            else:
                length = 1

        prefix_id = [f[1]]
        cnt = 0
        for v in nums:
            index = vid[v] + p
            f[index] ^= 1
            while index > 1:
                if index >= 8:
                    target = index >> 3
                    key = tuple(sorted([f[target << 3 | offset] for offset in range(8)]))
                else:
                    target = 1
                    if index >= 4:
                        key = tuple(sorted([f[4], f[5], f[6], f[7]]))
                    else:
                        key = tuple(sorted([f[2], f[3]]))
                
                if key not in node_dict:
                    node_dict[key] = nxt_id
                    nxt_id += 1
                
                f[target] = node_dict[key]
                index = target
            
            prefix_id.append(f[1])

        left, right = l0, r0
        res = []
        for _ in range(q):
            res.append(hit_k[left][0] <= right <= hit_k[left][1] and prefix_id[left] == prefix_id[right + 1])
            if res[-1]:
                g = left + right
            else:
                g = right - left
            
            left, right = (left ^ g) % n, (right ^ g) % n
            if left > right:
                left, right = right, left
        
        return res
```
