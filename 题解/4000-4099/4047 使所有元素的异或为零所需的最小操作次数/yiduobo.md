---
title: "4047. 使所有元素的异或为零所需的最小操作次数"
aliases: ["yiduobo的每日leetcode 4047.使所有元素的异或为零所需的最小操作次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2082996569377456864"
zhihu_id: "2082996569377456864"
zhihu_title: "yiduobo的每日leetcode 4047.使所有元素的异或为零所需的最小操作次数"
question_id: "4047"
question: "使所有元素的异或为零所需的最小操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-xor-of-all-elements-zero/"
created: "2026-09-15T02:48:48+08:00"
updated: "2026-09-15T02:48:48+08:00"
upvotes: 1
comments: 0
---

# 4047. 使所有元素的异或为零所需的最小操作次数

> **[yiduobo的每日leetcode 4047.使所有元素的异或为零所需的最小操作次数](https://zhuanlan.zhihu.com/p/2082996569377456864) · 知乎 · 2026-09-15 · 赞同 1**
> 力扣：[4047. 使所有元素的异或为零所需的最小操作次数](https://leetcode.cn/problems/minimum-operations-to-make-xor-of-all-elements-zero/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4047.使所有元素的异或为零所需的最小操作次数

<https://leetcode.cn/problems/minimum-operations-to-make-xor-of-all-elements-zero/description/>

题目给出一个由正整数组成的整数数组nums，其长度可达10^5，不过其中元素的大小不超过2000。

现在可以执行任意次操作，每次操作中，需要选择两个不同的下标i和j，满足nums[i]与nums[j]不同，然后将其中的一个替换为nums[i] ^ nums[j]，其中^表示按位异或。

问使得nums中所有元素的按位异或等于0所需的最少操作次数。若做不到，则返回-1。

首先考虑边界情况。

若一开始nums中所有元素的异或就是0，那么就无需操作，此时的答案就是0。

若所有元素的异或非0，且nums中所有元素都相同，那么就无法进行任何操作，此时的答案就是-1。

接下来考虑一般情况。

对于一组执行操作的nums[i]和nums[j]，在执行操作之前，二者的异或值nums[i] ^ nums[j]将被异或到最终数组的异或值中。而在执行操作之后，如果被替换的是nums[i]，即留下的是nums[i] ^ nums[j]以及nums[j]，那么被异或到最终数组的异或值中就只剩下了nums[i]，同理，如果被替换的是nums[j]，那么留下的就是nums[j]。

更进一步的，这种替换带来的删除是可以传递的，但是传递的前提条件是用过的元素不能再用。而一旦再用，相当于之前的异或操作就白干了。根据异或的特性，本题实际上就是要找出一个最小的子集，满足这个子集中元素的异或值恰好等于整个数组的元素的异或值，然后通过操作将这些元素对异或值的影响抹掉，剩下的元素的异或值就可以变为0了。

另一方面，由于多次异或相同的元素是没有意义的，因此问题从nums中所有元素中选取，简化为了从nums中所有不同元素中选取，也就就是说至多两千个元素中选取若干个，使得这些元素的异或值恰好等于整个数组的异或值。而对于这个问题，只需使用bfs从0开始不断扩展，直到组合出数组异或值为止，其中bfs的轮次使用的元素数量，即执行操作的次数。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        

        xor = 0
        for v in nums:
            xor ^= v
        
        if xor == 0:
            return 0

        if max(nums) == min(nums):
            return -1
        
        f = [-1] * 2048
        f[0] = 0
        q = [0]
        head, tail = 0, 1
        distinct_nums = list(set(nums))
        while head < tail:
            for x in q[head : tail]:
                for v in distinct_nums:
                    y = x ^ v
                    if f[y] == -1:
                        f[y] = f[x] + 1
                        q.append(y)

            head, tail = tail, len(q)
        
        if f[xor] == len(nums):
            return -1
        return f[xor]
```
