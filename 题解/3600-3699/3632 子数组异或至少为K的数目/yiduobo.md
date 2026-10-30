---
title: "3632. 子数组异或至少为K的数目"
aliases: ["yiduobo的每日leetcode 3632.子数组异或至少为K的数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1946378424206747562"
zhihu_id: "1946378424206747562"
zhihu_title: "yiduobo的每日leetcode 3632.子数组异或至少为K的数目"
question_id: "3632"
question: "子数组异或至少为K的数目"
problem_url: "https://leetcode.cn/problems/subarrays-with-xor-at-least-k/"
created: "2025-09-03T01:25:55+08:00"
updated: "2025-09-03T01:25:59+08:00"
upvotes: 1
comments: 0
---

# 3632. 子数组异或至少为K的数目

> **[yiduobo的每日leetcode 3632.子数组异或至少为K的数目](https://zhuanlan.zhihu.com/p/1946378424206747562) · 知乎 · 2025-09-03 · 赞同 1**
> 力扣：[3632. 子数组异或至少为K的数目](https://leetcode.cn/problems/subarrays-with-xor-at-least-k/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3632.子数组异或至少为K的数目

[3632. 子数组异或至少为 K 的数目 - 力扣（LeetCode）](https://leetcode.cn/problems/subarrays-with-xor-at-least-k/description/)

题目给出一个长度为n的正整数属于nums和一个非负整数k，n不超过10^5，数组中的元素大小以及k不超过10^9。要求找出其中所有元素按位异或大于等于k的子数组的数目。

题目的长度很短，但是难度却不低。由于数据规模较大，直接使用暴力法显然是不行的。另一方面，由于是异或操作，因此常规的滑动窗口也是不行的，因为不具备单调性，必须另想办法。

注意到对同一个元素异或两次相当于无事发生，那么对于一个子数组，其异或值就可以将其转化为两个前缀数组的异或结果再进行异或，这样一来就有了个算法的雏形了：遍历数组，计算到当前下标为止的异或值，并计算有多少个前缀数组的异或值与当前的异或值异或后大于等于k。

由于异或是基于二进制位进行运算的，那么比较结果的大小基于二进制来进行也比较方便，这样一来可以考虑将所有的前缀异或值拉成01的串。又由于二进制大小的比较，只要高位分出胜负来低位就不用比了，也就是说在这里比的也是前缀，因此在这里可以考虑利用trie树来进行求解。使用trie树还有一个理由，就是这里是01串，所以形成的是一颗二叉树。在trie树中行走时，路径是非0即1的，而对于当前没走的那一侧，其中包含了多少个前缀中的异或值也可以在建树时通过记录每个节点的权重，在O(1)的时间内得到。

基于上面的分析，就得到了一种做法：

对于nums所有的前缀的异或值建立trie树，trie树一开始为空。接下来从头开始遍历nums数组，计算当前前缀的异或值xor，对于当前的xor，从二进制的最高位开始向下遍历，对于当前遍历到的位：

1、若k在这一位上为1：

为了使得xor与之前的某个前缀的异或结果大于等于k，那么这个异或结果在这一位上也必须是1。不妨设xor在这一位上为d，那么此时就必须往trie数中1 - d这个孩子节点走。若不存在，则说明没有可用的前缀，直接退出。

2、若k在这一位上为0：

若xor在这一位上为d，且配对的前缀在这一位上为1 - d，那么二者的异或结果在这一位上就为1，也就是说这个异或结果必然大于k，因此在1 - d这一侧的所有前缀都是合法的，此时可以将对应孩子节点的权重累加到答案中。接下来，依然正常走向trie树中d对应的这一侧孩子节点，计算在高位相等时有多少可以通过低位配对成功的前缀。同样的，若此时不存在d这一侧的孩子，也直接退出。

全部计算完成后，将当前xor加入到trie树中，然后继续向后遍历即可。

最后附上python代码：

```python
class Solution(object):
    def countXorSubarrays(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        c = [[None, None]]
        weight = [0]

        ma = max(max(nums), k)
        length = len(bin(ma)) - 2
        p2 = [1]
        while len(p2) < length:
            p2.append(p2[-1] + p2[-1])

        now = 0
        for index in range(length - 1, -1, -1):
            c[now][0] = len(weight)
            c.append([None, None])
            weight.append(1)
            now = c[now][0]

        digits_k = [0] * length
        p = 0
        while k:
            digits_k[p] = k % 2
            k //= 2
            p += 1

        xor = 0
        res = 0
        for v in nums:
            xor ^= v
            now = 0
            for index in range(length - 1, -1, -1):
                if xor & p2[index]:
                    d = 1
                else:
                    d = 0

                if digits_k[index] == 1:
                    now = c[now][1 - d]
                else:
                    if c[now][1 - d] is not None:
                        res += weight[c[now][1 - d]]
                    now = c[now][d]
                
                if now is None:
                    break

            if now is not None:
                res += weight[now]
        
            now = 0
            for index in range(length - 1, -1, -1):
                if xor & p2[index]:
                    d = 1
                else:
                    d = 0
                
                if c[now][d] is None:
                    c[now][d] = len(weight)
                    c.append([None, None])
                    weight.append(0)
                
                now = c[now][d]
                weight[now] += 1

        return res
```
