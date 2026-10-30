---
title: "3250. 单调数组对的数目I & 3251. 单调数组对的数目II"
aliases: ["yiduobo的每日leetcode 3250.单调数组对的数目I && 3251.单调数组对的数目II", "3250. 单调数组对的数目I", "3251. 单调数组对的数目II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "leetcode/prefix-sum", "题单/动态规划", "题单/动态规划/七-其他线性-DP", "题单/数学算法", "题单/动态规划/十一-优化-DP", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/721703913"
zhihu_id: "721703913"
zhihu_title: "yiduobo的每日leetcode 3250.单调数组对的数目I && 3251.单调数组对的数目II"
question_id: ["3250", "3251"]
question: ["单调数组对的数目 I", "单调数组对的数目 II"]
problem_url: ["https://leetcode.cn/problems/find-the-count-of-monotonic-pairs-i/", "https://leetcode.cn/problems/find-the-count-of-monotonic-pairs-ii/"]
difficulty: "Hard"
rating: ["1898", "2323"]
created: "2024-09-23T23:21:00+08:00"
updated: "2024-09-23T23:21:00+08:00"
upvotes: 2
comments: 0
---

# 3250. 单调数组对的数目I & 3251. 单调数组对的数目II

> **[yiduobo的每日leetcode 3250.单调数组对的数目I && 3251.单调数组对的数目II](https://zhuanlan.zhihu.com/p/721703913) · 知乎 · 2024-09-23 · 赞同 2**
> 力扣：[3250. 单调数组对的数目 I](https://leetcode.cn/problems/find-the-count-of-monotonic-pairs-i/) · Hard · 灵茶山艾府：[两种方法：前缀和优化 DP / 组合数学（Python/Java/C++/Go）](../3250%20单调数组对的数目%20I/灵茶山艾府.md)
> 力扣：[3251. 单调数组对的数目 II](https://leetcode.cn/problems/find-the-count-of-monotonic-pairs-ii/) · Hard · 灵茶山艾府：[两种方法：前缀和优化 DP / 组合数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3250.单调数组对的数目I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-count-of-monotonic-pairs-i/description/)

3251.单调数组对的数目II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-count-of-monotonic-pairs-ii/description/)

题目给出一个大小为n的正整数数组nums，要求构造出两个由非负整数构成的数组arr1和arr2，这两个数组满足arr1单调不减，arr2单调不增，且对于任意的下标i，都满足arr1[i] + arr2[i] \= nums[i]。问一共有多少种可行的构造方案。

两题的题设一样，第二题的数据规模较大。

常规的动态规划是比较容易想到的，令f[index][v]表示构造了arr1和arr2的第0到第index项，其中arr1[index]为v时可行的构造方案。由于题目要求arr1[i] + arr2[i] \= nums[i]，因此这里arr1[index]为v实际上就规定了arr2[index]为nums[i] - v。

接下来对于f[index][v]：

1、首先考虑边界情况：

当index \= 0时，v的可行取值范围在0到nums[0]之间，这些f[index][v]都等于1，而其他的f[index][v]则都等于0

2、接下来对于index > 1的情况：

此时可以枚举所有可行的f[index - 1][pre_v]，对于pre_v的取值：

由于arr1[index - 1]必须小于等于arr1[index]，因此必须满足pre_v \<\= v

由于arr2[index - 1]必须大于等于arr2[index]，因此必须满足nums[index - 1] - pre_v >\= nums[index] - v

最后pre_v自身的取值范围也必须在0到nums[index - 1]之间

综合以上三点，就有

0 \<\= pre_v \<\= min(v, nums[index - 1], nums[index - 1] + v - nums[index])

注意到这里的v必然是小于等于nums[index]，因此上面min里面的最后一项必然小于等于nums[index- 1]，可以省去nums[index - 1]这一项，那么就有0 \<\= pre_v \<\= min(v, nums[index - 1] + v - nums[index])。此时就有

f[index][v] \= f[index - 1][0] + f[index - 1][1] + ... + f[index - 1][min(v, nums[index - 1] + v - nums[index])]

如果直接枚举所有可行的pre_v，上面算法的时间复杂度就是O(nm^2)，其中m表示nums中的最大值。

注意到状态转移方程是一个标准的前缀和形式，因此可以令

s[index][v] \= f[index][0] + f[index][1] + ... + f[index][v]

那么就有

f[index][v] \= s[index - 1][min(v, nums[index - 1] + v - nums[index])]

在计算完f[index]所有可行的v之后，再利用f[index][v]来更新s[index]就行了，这样一来整体的时间复杂度就被优化到了O(nm)。

另外注意到这里的s和f都只与上一轮有关，因此可以通过二者相互更新来省去index这一维。

最后附上python代码：

```python
class Solution(object):
    def countOfPairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        ma = max(nums)

        f = [0] * (ma + 1)
        s = [0] * (ma + 1)

        mod = 10 ** 9 + 7
        for v in range(nums[0] + 1):
            f[v] = 1
            if v == 0:
                s[v] = f[v]
            else:
                s[v] = s[v - 1] + f[v]

        pre = nums[0]
        for x in nums[1:]:
            f = [0] * (ma + 1)
            for v in range(0, x + 1):
                threshold = min(v, pre + v - x)
                if threshold >= 0:
                    f[v] = s[threshold]

            s = [0] * (ma + 1)
            for v in range(0, x + 1):
                if v == 0:
                    s[v] = f[v]
                else:
                    s[v] = s[v - 1] + f[v]
                    if s[v] >= mod:
                        s[v] -= mod
        
            pre = x
        return s[nums[-1]]
```
