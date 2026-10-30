---
title: "2572. 无平方子集计数"
aliases: ["yiduobo的每日leetcode 2572.无平方子集计数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/641520142"
zhihu_id: "641520142"
zhihu_title: "yiduobo的每日leetcode 2572.无平方子集计数"
question_id: "2572"
question: "无平方子集计数"
problem_url: "https://leetcode.cn/problems/count-the-number-of-square-free-subsets/"
difficulty: "Medium"
rating: 2420
created: "2023-07-05T00:22:01+08:00"
updated: "2023-07-05T00:22:01+08:00"
upvotes: 0
comments: 0
---

# 2572. 无平方子集计数

> **[yiduobo的每日leetcode 2572.无平方子集计数](https://zhuanlan.zhihu.com/p/641520142) · 知乎 · 2023-07-05 · 赞同 0**
> 力扣：[2572. 无平方子集计数](https://leetcode.cn/problems/count-the-number-of-square-free-subsets/) · Medium · 灵茶山艾府：[两种写法：01背包/子集状压DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2572.无平方子集计数

[力扣](https://leetcode.cn/problems/count-the-number-of-square-free-subsets/)

首先，1在本题中不会影响平方子集的判定，因此每个1都可以任意选择加入或者不加入某个子集。不妨设一共有one个1，另外由大于1的数构成的子集一共有res个，那么一共可以构成res \* (2^one) + (2^one) - 1个合法的子集。关于这个式子，前半部分表示的是这one个1可以任意选择加入或不加入到这res个子集中，而后半部分则表示这one个1单独形成的子集，最后的减一是因为需要去掉空集的情况。

排除了1的影响，接下来需要考虑如何计算大于1的数构成的合法子集数量。对于大于1的数，其必然可以写成若干个素数的幂相乘的形式，而一个合法子集要求的是将子集中每个数分解质因数，并按照底数分别累加指数后，最大的指数和不能大于等于2。

另外，注意到本题中的数字不超过30，期间只有2、3、5、7、11、13、17、19、23、29这一共10个质数，那么就可以使用一个10位的2进制数来表示一个合法的子集，其中第i位表示的是子集中的数分解质因数的结果是否已经包含第i个质数。到了这里，就可以使用状态压缩动态规划来求解合法子集的数量了。

令f[j][index]表示前j个大于1的数可以得到的状态为index的合法子集数量，接下来遍历nums中所有大于1的数并将其分解质因数。

若当前遍历到的数分解的结果本身就包含大于等于2的指数，那么就直接跳过这个数，同时对于所有的index都有f[j][index] \= f[j - 1][index]。否则就通过其质因数在质数中的下标计算其对应的state。接下来，枚举所有的状态index，若当前index中包含了state，也就是index & state \= state，那么就有f[j][index] +\= f[j - 1][index ^ state]，表示在状态表示为index ^ state的集合的基础上添加当前数得到状态表示为index的集合。

计算完成后，将所有index大于0的f[-1][index]累加起来即为大于1的数可以构成的合法子集数量。这里排除掉f[-1][0]的原因是index为0表示的是空集。

另外，由于f每一轮都只与上一轮有关，因此可以通过倒序遍历index来省去j这一维。

最后附上python代码：

```python
class Solution(object):
    def squareFreeSubsets(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        max_state = 1024

        f = [0] * max_state
        f[0] = 1
        mod = 10 ** 9 + 7
        one = 0

        for v in nums:
            if v == 1:
                one += 1
                continue

            state = 0
            flag = True
            for index, p in enumerate(prime):
                if v % p == 0:
                    if v / p % p == 0:
                        flag = False
                        break
                    
                    state |= (1 << index)
            
            if not flag:
                continue
            
            for index in range(max_state - 1, state - 1, -1):
                if index & state == state:
                    f[index] += f[index ^ state]
                    if f[index] >= mod:
                        f[index] -= mod

        res = 0

        for index in range(1, max_state):
            res += f[index]
            if res >= mod:
                res -= mod
        
        pow2 = 1
        for _ in range(one):
            res += res
            if res >= mod:
                res -= mod

            pow2 += pow2
            if pow2 >= mod:
                pow2 -= mod
        
        res = res + pow2 - 1
        if res < 0:
            res += mod
        if res >= mod:
            res -= mod

        return res
```
