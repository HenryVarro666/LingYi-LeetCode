---
title: "3845. 最大子数组异或值"
aliases: ["yiduobo的每日leetcode 3845.最大子数组异或值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/trie", "leetcode/hash-table", "leetcode/prefix-sum", "leetcode/sliding-window", "leetcode/monotonic-queue", "题单/常用数据结构", "题单/位运算", "题单/常用数据结构/六-字典树-trie", "题单/位运算/五-试填法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2011475734871446659"
zhihu_id: "2011475734871446659"
zhihu_title: "yiduobo的每日leetcode 3845.最大子数组异或值"
question_id: "3845"
question: "最大子数组异或值"
problem_url: "https://leetcode.cn/problems/maximum-subarray-xor-with-bounded-range/"
difficulty: "Hard"
created: "2026-03-01T16:41:21+08:00"
updated: "2026-03-01T16:41:24+08:00"
upvotes: 0
comments: 0
---

# 3845. 最大子数组异或值

> **[yiduobo的每日leetcode 3845.最大子数组异或值](https://zhuanlan.zhihu.com/p/2011475734871446659) · 知乎 · 2026-03-01 · 赞同 0**
> 力扣：[3845. 最大子数组异或值](https://leetcode.cn/problems/maximum-subarray-xor-with-bounded-range/) · Hard · 灵茶山艾府：[两种方法：0-1 字典树 / 试填法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3845.最大子数组异或值

<https://leetcode.cn/problems/maximum-subarray-xor-with-bounded-range/description/>

题目给出一个非负整数数组nums以及一个整数k。

现在要求从nums中找出一个子数组，这个子数组中的最大值与最小值之间的差不超过k，且这个子数组中各元素异或的结果最大。

问最大可能得到的异或值是多少。

首先，对于一个固定了左边界的子数组而言，其右边界p越大，其中的最大值就越大，最小值就越小，也就是说p越大，最大值和最小值之间的差值越大，就越有可能超过k。

反过来，以p为右边界，index为左边界的子数组中的最大值，必然大于等于以index + 1为左边界的子数组中的最大值，最小值也一样，因此若以index为左边界的子数组的最大合法右边界为p，那么p也必然是以index + 1为左边界的子数组的一个合法右边界，从而得到以index + 1为左边界的最大合法右边界必然大于等于p。

基于上面的结论，就可以利用滑动窗口，配合堆或者单调栈，计算出对于每个左边界的最大合法右边界。

接下来，问题就变成了对于每个左边界index，若其最大合法右边界为p，那么就需要找出index到p之间的最优右边界q，使得index到q这一段的异或值最大。

注意到index到q这一段的异或是区间异或，那么一种常见的思路就是将其转化为前缀异或再想办法处理。方便起见，记pre_xor[0]为0，而pre_xor[index + 1]为nums[0] ^ nums[1] ^ ... ^ nums[index]，那么index到q这一段的异或值，就可以写成pre_xor[index] ^ pre_xor[q + 1]。

其中pre_xor[index]是固定的，因此目标就是从pre_xor[index + 1]到pre_xor[p + 1]中选出最优的那个pre_xor[q + 1]。

对于这个问题，则可以先将pre_xor[index + 1]到pre_xor[p + 1]做成01的trie树，接下来按二进制位从高到低进行遍历，尽量让异或结果的高位为1。

更具体的，对于当前遍历到的位d，若pre_xor[index + 1]在d这一位上为1，为了使得异或结果的这一位为1，此时就应该尽量往trie树中当前节点的孩子0方向走，反之则应该尽量往孩子1方向走，当然，这里的前提是trie树中有对应的孩子。

到了这里，就得到了一种可行的做法。

先对nums进行一趟遍历，预处理出pre_xor数组。

接下来再一趟遍历，对于每个左边界index，利用单调队列计算出index对应的最大合法的右边界p，并将本轮中右边界新扩展的位置对应的pre_xor加入到trie树中。接下来，通过trie树计算与pre_xor[index + 1]异或可能得到的最大结果并更新答案，然后将pre_xor[index + 1]从trie树中移除然后继续向后遍历即可。

最后附上python代码：

```python
class Solution(object):
    def maxXor(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        def update(v, delta):
            now = root
            for d in range(14, -1, -1):
                if (v & (1 << d)) == (1 << d):
                    c = 1
                else:
                    c = 0
                
                if c not in now:
                    now[c] = [{}, 0]
                now[c][1] += delta
                now = now[c][0]

        def find(other):
            now = root
            v = 0
            for d in range(14, -1, -1):
                p2 = 1 << d
                if (other & p2) == p2:
                    c = 0
                else:
                    c = 1
                
                if c in now and now[c][1] > 0:
                    v |= p2
                    now = now[c][0]
                else:
                    now = now[c ^ 1][0]
            
            return v

        pre_xor = [0]
        for v in nums:
            pre_xor.append(pre_xor[-1] ^ v)
        
        ma = deque()
        mi = deque()

        p = 0
        n = len(nums)
        root = {}
        res = 0
        for index, v in enumerate(nums):
            while p < n:
                ma_v, mi_v = nums[p], nums[p]
                if ma:
                    ma_v = max(ma_v, nums[ma[0]])
                if mi:
                    mi_v = min(mi_v, nums[mi[0]])
                if ma_v - mi_v <= k:
                    while ma and nums[ma[-1]] <= nums[p]:
                        ma.pop()
                    ma.append(p)

                    while mi and nums[mi[-1]] >= nums[p]:
                        mi.pop()
                    mi.append(p)

                    update(pre_xor[p + 1], 1)
                    p += 1
                else:
                    break
            
            res = max(res, find(pre_xor[index]))
            if ma and ma[0] == index:
                ma.popleft()
            if mi and mi[0] == index:
                mi.popleft()
            update(pre_xor[index + 1], -1)

        return res
```
