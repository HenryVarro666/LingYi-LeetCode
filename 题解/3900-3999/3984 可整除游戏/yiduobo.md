---
title: "3984. 可整除游戏"
aliases: ["yiduobo的每日leetcode 3984.可整除游戏"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/segment-tree", "leetcode/hash-table", "leetcode/math", "leetcode/dynamic-programming", "leetcode/number-theory", "leetcode/prefix-sum", "题单/动态规划", "题单/数学算法", "题单/动态规划/一-入门-DP", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2057227210667381385"
zhihu_id: "2057227210667381385"
zhihu_title: "yiduobo的每日leetcode 3984.可整除游戏"
question_id: "3984"
question: "可整除游戏"
problem_url: "https://leetcode.cn/problems/divisible-game/"
difficulty: "Medium"
rating: 1944
created: "2026-07-08T21:45:05+08:00"
updated: "2026-07-08T21:45:05+08:00"
upvotes: 0
comments: 0
---

# 3984. 可整除游戏

> **[yiduobo的每日leetcode 3984.可整除游戏](https://zhuanlan.zhihu.com/p/2057227210667381385) · 知乎 · 2026-07-08 · 赞同 0**
> 力扣：[3984. 可整除游戏](https://leetcode.cn/problems/divisible-game/) · Medium · 灵茶山艾府：[三种方法计算最大子数组和：枚举/线段树/前缀和（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3984.可整除游戏

<https://leetcode.cn/problems/divisible-game/description/>

题目给出一个长度为n的正整数数组nums，其长度不超过1000，其中元素大小不超过10^6。

alice和bob正在玩一个游戏。

游戏开始前，alice需要选择一个大于1的整数k以及两个在0到n - 1之间的整数l和r，同时l \<\= r。

在一开始，alice和bob分数都为0，接下来，对于l到r之间的每个下标index，若nums[index]是k的倍数，那么alice的分数增加nums[index]，否则bob的分数增加nums[index]。

最后，定义分数差为alice的分数减去bob的分数。alice希望让分数差最大，若有多个k可以使得分数差最大，那么alice会选择其中最小的那个k。

问最大的分数差与k的乘积是多少。

首先可以明确的是，除了nums全为1这种特殊情况之外，alice选择的k必然是l到r之间某个元素的质因子。理由如下：

- 如果k不是某个元素的因子，那么相当于把区间内的分数都让给了bob，这显然是不优的。
- 而选择质因子，则是因为若k为合数，那么如果改为选择k的某个质因子，那么区间中是老k倍数的元素，必然也是新k的倍数，同时可能出现一些不是老k倍数但是是新k倍数的元素，有机会使得alice的得分更高，因此在这里选择新k显然是更好的选择。

基于这一点以及题目中元素的取值范围，就可以先通过筛法找出nums中所有元素的质因子集合，然后在其中枚举最终选择的k并计算对应的最大分数差。

至于最大分数差的计算，对于当前的k，可以将nums中为k倍数的元素保持不变，其他元素取相反数，问题就变成了经典的最大子段和问题，一趟遍历贪心求解即可。

在具体实现上，可以总是保留2这个质因子，这样就能顺便处理掉全1的情况，同时筛法可以从3开始以步长为2进行。

最后附上python代码：

```python
class Solution(object):
    def divisibleGame(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        best_score = None
        best_k = None

        hit = [2]
        nums_set = set(nums)
        ma = max(nums)

        f = [True] * (ma + 2)
        for x in range(3, ma + 1, 2):
            if f[x]:
                for v in range(x, ma + 1, x):
                    f[v] = False
                    if v in nums_set and hit[-1] != x:
                        hit.append(x)

        for p in hit:
            s = 0
            for v in nums:
                if v % p != 0:
                    v = -v
                
                if s < 0:
                    s = 0
                s += v
                if best_score is None or best_score < s:
                    best_score = s
                    best_k = p
        
        mod = 10 ** 9 + 7
        return best_score * best_k % mod
```
