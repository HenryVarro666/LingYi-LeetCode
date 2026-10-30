---
title: "3811. 交替按位异或分割的数目"
aliases: ["yiduobo的每日leetcode 3811.交替按位异或分割的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/动态规划", "题单/动态规划/六-状态机-DP", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1996640222381891632"
zhihu_id: "1996640222381891632"
zhihu_title: "yiduobo的每日leetcode 3811.交替按位异或分割的数目"
question_id: "3811"
question: "交替按位异或分割的数目"
problem_url: "https://leetcode.cn/problems/number-of-alternating-xor-partitions/"
difficulty: "Medium"
rating: 2006
created: "2026-01-19T20:07:33+08:00"
updated: "2026-01-19T20:07:38+08:00"
upvotes: 1
comments: 0
---

# 3811. 交替按位异或分割的数目

> **[yiduobo的每日leetcode 3811.交替按位异或分割的数目](https://zhuanlan.zhihu.com/p/1996640222381891632) · 知乎 · 2026-01-19 · 赞同 1**
> 力扣：[3811. 交替按位异或分割的数目](https://leetcode.cn/problems/number-of-alternating-xor-partitions/) · Medium · 灵茶山艾府：[合法子序列 DP + 状态机 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3811.交替按位异或分割的数目

<https://leetcode.cn/problems/number-of-alternating-xor-partitions/description/>

题目给出一个整数数组nums以及两个互不相同的整数target1和target2。

现在要求将nums分割成一个或多个连续的块，每一块非空，且这些快的按位异或值按target1、target2交替出现，即对于划分出来的块b1、b2、b3、...，有

XOR(b1) \= target1

XOR(b2) \= target2（若b2存在）

XOR(b3) \= target1（若b3存在）

以此类推。

问有多少种可行的划分方案。

在进行划分后将得到若干个区间异或，看到区间问题自然就会联想到能否转化为前缀问题求解，恰好异或操作也是满足这个转化的，那么对于所有合法划分的前缀异或，都需要满足：

- 第一段的异或值为target1
- 第二段的异或值为target2，因此到第二段为止的前缀异或为target1 ^ target2
- 第三段的异或值为target1，因此到第三段为止的前缀异或为target1 ^ target2 ^ target1 \= target2
- 第四段的异或值为target2，因此到第四段为止的前缀异或为target1 ^ target2 ^ target1 ^ target2 \= 0
- 第五段的异或值为target1，因此到第五段为止的前缀异或为target1 ^ target2 ^ target1 ^ target2 ^ target1 \= target1
- 以此类推

此时问题就转化成了计算存在多少个合法的下标序列p，满足

prefix_xor\[p\[0\]\] \= target1

prefix_xor\[p\[1\]\] \= target1 ^ target2

prefix_xor\[p\[2\]\] \= target2

prefix_xor\[p\[3\]\] \= 0

prefix_xor\[p\[4\]\] \= target1

...

以此类推

这是非常经典的动态规划问题，令t1[index]表示所有结尾小于等于index且前缀异或值恰好等于target1的所有前缀的合法划分方案数，xor[index]、t2[index]、zero[index]则表示前缀异或值恰好等于target1 ^ target2、target2、0的合法划分方案数，那么：

1、根据定义，如果不考虑nums[index]，那么就有

t1[index] \= t1[index - 1]

xor[index] \= xor[index - 1]

t2[index] \= t2[index - 1]

zero[index] \= zero[index - 1]

2、如果要考虑nums[index]，需要先计算当前的前缀异或值x：

若x \= target1，那么就有t1[index] +\= zero[index - 1]，表示在之前所有前缀异或为0的前缀的划分方案的基础上，添加上最后到index的这一段。

需要注意，这里只能这样做状态转移，因为前缀异或为target1，意味着最后一段必须是target1，因此到上一段结尾位置的前缀异或必须为0。

同样的

若x \= target1 ^ target2，那么就有xor[index] +\= t1[index - 1]

若x \= target2，那么就有t2[index] +\= xor[index - 1]

若x \= 0，那么就有zero[index] +\= t2[index - 1]

另外需要特别注意的是，计算完成后，答案并不是t1[-1] + xor[-1] + t2[-1] + zero[-1]。

以t1为例，按照状态表示，t1[-1]记录的是所有异或值为target1的前缀的合法划分方案，但是题目问的是整个字符串的划分方案，因此只有最后这个前缀才作数。

更进一步的，记整个数组的异或值为x，那么只有当x等于target1时，需要将t1[-1] - t1[-2]，也就是zero[-2]累加到答案中。

同理，当x为target1 ^ target2时，需要将t1[-2]累加到答案中。当x为target2时，需要将xor[-2]累加到答案中。当x为0时，需要将t2[-2]累加到答案中。

注意到状态转移只与上一轮有关，因此可以使用四个变量迭代，省去四个数组的开销。

最后附上python代码：

```python
class Solution(object):
    def alternatingXOR(self, nums, target1, target2):
        """
        :type nums: List[int]
        :type target1: int
        :type target2: int
        :rtype: int
        """
        
        t1, xor, t2, zero = 0, 0, 0, 1
        x = 0
        mod = 10 ** 9 + 7
        for v in nums:
            x ^= v
            pre_t1, pre_xor, pre_t2, pre_zero = t1, xor, t2, zero

            if x == target1:
                t1 += pre_zero
                if t1 >= mod:
                    t1 -= mod

            if x == target1 ^ target2:
                xor += pre_t1
                if xor >= mod:
                    xor -= mod

            if x == target2:
                t2 += pre_xor
                if t2 >= mod:
                    t2 -= mod

            if x == 0:
                zero += pre_t2
                if zero >= mod:
                    zero -= mod

        res = 0
        if x == target1:
            res += pre_zero
        if x == target1 ^ target2:
            res += pre_t1
        if x == target2:
            res += pre_xor
        if x == 0:
            res += pre_t2
        return res % mod
```
