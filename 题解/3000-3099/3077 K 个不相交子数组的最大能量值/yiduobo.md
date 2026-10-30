---
title: "3077. K个不相交子数组的最大能量值"
aliases: ["yiduobo的每日leetcode 3077.K个不相交子数组的最大能量值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/动态规划", "题单/动态规划/五-划分型-DP", "题单/动态规划/六-状态机-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/697992616"
zhihu_id: "697992616"
zhihu_title: "yiduobo的每日leetcode 3077.K个不相交子数组的最大能量值"
question_id: "3077"
question: "K 个不相交子数组的最大能量值"
problem_url: "https://leetcode.cn/problems/maximum-strength-of-k-disjoint-subarrays/"
difficulty: "Hard"
rating: 2557
created: "2024-05-15T23:02:00+08:00"
updated: "2024-05-15T23:02:00+08:00"
upvotes: 1
comments: 0
---

# 3077. K个不相交子数组的最大能量值

> **[yiduobo的每日leetcode 3077.K个不相交子数组的最大能量值](https://zhuanlan.zhihu.com/p/697992616) · 知乎 · 2024-05-15 · 赞同 1**
> 力扣：[3077. K 个不相交子数组的最大能量值](https://leetcode.cn/problems/maximum-strength-of-k-disjoint-subarrays/) · Hard · 灵茶山艾府：[前缀和+划分型DP+式子变形（附题单！）Python/Java/C++/Go](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3077.K个不相交子数组的最大能量值

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-strength-of-k-disjoint-subarrays/description/)

朴素的动态规划算法是很容易想到的。令f[i][j]表示从nums[0]到nums[i]中选取j个不相交子数组可以得到的最大能量值，那么对于f[i][j]，首先初始化f[i][0] \= 0，表示一个子数组都不选的话能量值自然就是0，另外需要初始化其他的f值为空。接下来对于f[i][j]：

1、可以放弃掉nums[i]，于是就有f[i][j] \= f[i - 1][j]

2、如果要选择nums[i]，那么就需要枚举最后这个子数组的起点start，于是就有f[i][j] \= max(f[i][j], f[start - 1][j - 1] + (nums[start] + nums[start + 1] + ... + nums[i]) \* (k - j +1) \* (-1)^(j + 1))

朴素的动态规划的状态表示是O(nk)的，转移时需要枚举最后这一段的起点，最终的时间复杂度为O(n^2 \* k)，必须进行优化。

枚举状态的二重循环是没有优化空间的，这也就意味着只能想办法优化转移方程。

对于f[start - 1][j - 1] + (nums[start] + nums[start + 1] + ... + nums[i]) \* (k - j +1) \* (-1)^(j + 1)这个式子，其中存在一段区间和，那么就可以先将其转化为前缀和之差。

令s[i]表示nums[0] + nums[1] + ... + nums[i]，转移方程就可以写成

f[i][j] \= max(f[i - 1][j], f[start - 1][j - 1] + (s[i] - s[start - 1]) \* (k - j + 1) \* (-1)^(j + 1))

方便起见，令p \= start - 1，那么就是

f[i][j] \= max(f[i - 1][j], f[p][j - 1] + (s[i] - s[p]) \* (k - j + 1) \* (-1)^(j + 1))

接下来，将括号拆开，就有

s[i] \* (k - j + 1) \* (-1)^(j + 1) + (f[p][j - 1] - s[p] \* (k - j + 1) \* (-1)^(j + 1))

可以发现，式子的前半部分是定值，因此此时的目标就是找出最好的p使得后半部分的值最大，于是可以使用一个数组g记录最优的p，即g[j - 1]表示之前计算得到的最大的f[p][j - 1] - s[p] \* (k - j + 1) \* (-1)^(j + 1)。

此时就只需要一边通过g[j - 1]来计算f[i][j]，然后使用f[i][j]来更新g[j]。即

f[i][j] \= max(f[i - 1][j], s[i] \* (k - j + 1) \* (-1)^(j + 1) + g[j - 1])

g[j] \= max(g[j], f[i][j] + s[i] \* (k - j) \* (-1)^(j + 1)）

需要注意g这边的两个细节。

首先是乘法的系数为(k - j)而不是(k - j + 1)，因为这里的g[j]是用来更新后续f中的f[x][j + 1]，转移方程应该是f[p][j] + (s[x] - s[p]) \* (k - (j + 1) + 1) \* (-1)^(j + 2)，中间乘数项k - (j + 1) + 1就是k - j。

另外的就是最后的-1的幂次应该是j + 2次，我在这里选择还是将其写成j + 1次，然后将前面的减号改为加号。

到了这里，转移的复杂度就优化到了O(1)，此时的时间复杂度就是O(nk)。

另外可以发现的是，此时的转移方程中每一轮都只与g以及上一轮有关，因此可以省略掉状态中的i这一维，然后改为倒序遍历防止重复计算。

最后附上python代码：

```python
class Solution(object):
    def maximumStrength(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        n = len(nums)
        f = [None] * (k + 1)
        f[0] = 0
        g = [None] * (k + 1)
        g[0] = 0

        s = [nums[0]]
        for v in nums[1:]:
            s.append(s[-1] + v)
        
        for i in range(n):
            for j in range(min(i + 1, k), 0, -1):
                if j % 2 == 1:
                    sign = 1
                else:
                    sign = -1
                mul = k - j + 1
                p = s[i] * sign * mul
                q = s[i] * sign * (mul - 1)

                v = g[j - 1] + p
                if f[j] is None or f[j] < v:
                    f[j] = v
                if g[j] is None or g[j] < f[j] + q:
                    g[j] = f[j] + q

            g[0] = max(g[0], -s[i] * mul)

        return f[-1]
```
