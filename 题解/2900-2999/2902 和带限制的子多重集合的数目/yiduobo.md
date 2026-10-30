---
title: "2902. 和带限制的子多重集合的数目"
aliases: ["yiduobo的每日leetcode 2902.和带限制的子多重集合的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/动态规划", "题单/动态规划/三-背包", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/663784087"
zhihu_id: "663784087"
zhihu_title: "yiduobo的每日leetcode 2902.和带限制的子多重集合的数目"
question_id: "2902"
question: "和带限制的子多重集合的数目"
problem_url: "https://leetcode.cn/problems/count-of-sub-multisets-with-bounded-sum/"
difficulty: "Hard"
rating: 2759
created: "2023-10-28T02:55:28+08:00"
updated: "2023-10-28T02:55:28+08:00"
upvotes: 0
comments: 0
---

# 2902. 和带限制的子多重集合的数目

> **[yiduobo的每日leetcode 2902.和带限制的子多重集合的数目](https://zhuanlan.zhihu.com/p/663784087) · 知乎 · 2023-10-28 · 赞同 0**
> 力扣：[2902. 和带限制的子多重集合的数目](https://leetcode.cn/problems/count-of-sub-multisets-with-bounded-sum/) · Hard · 灵茶山艾府：[多重背包方案数：从朴素 DP 到优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2902.和带限制的子多重集合的数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-of-sub-multisets-with-bounded-sum/)

题目要求从集合中选出一个子集，使得这个子集的和落在l到r之间，问存在多少个不重复的子集。

最直观的思路自然是计算子集等于l、等于l + 1、等于l + 2、...、等于r的方案数，然后将这些方案数相加。那么对于单个问题，就是要求从一个集合中找出一个子集，使得子集和等于指定数值，与背包问题相似。不过这里有去重问题存在，因此这是一个多重背包问题，也就是说有若干种不同的物品，每种物品可能有若干件，要求每种物品选若干个使得和等于指定重量和。

处理方法依然是动态规划，令f[i][j]表示前i种物品满足和为j的方案数，那么对于f[i][j]，设第i种物品的重量为v，一共有cnt[v]个，那么就有

f[i][j] \= f[i - 1][j] + f[i - 1][j - v] + f[i - 1][j - 2 \* v] + ... + f[i - 1][j - cnt[v] \* v]

其中第一项表示不选择任何物品i，而后面的每一项则对应选择一件、两件、...、cnt[v]件物品i。

这种做法的时间复杂度肯定是偏高的，需要想办法进行优化。

状态表示方面，虽然可以用滚动数组优化掉i这一维，但是对最终的时间复杂度并没有帮助，因为即使优化掉了i这一维，依然要枚举每种物品，在时间方面并没有优化掉i这一维。而对于重量和这一维则是状态表示的核心，也无法进行优化，因此优化的重点只能放在优化状态转移方程上。

再次观察转移方程

f[i][j] \= f[i - 1][j] + f[i - 1][j - v] + f[i - 1][j - 2 \* v] + ... + f[i - 1][j - cnt[v] \* v]

对于f[i][j - v]，就有

f[i][j - v] \= f[i - 1][j - v] + f[i - 1][j - 2 \* v] + f[i - 1][j - 3 \* v] + ... + f[i - 1][j - (cnt[v] +1) \* v]

可以发现，其中f[i - 1][j - v]到f[i - 1][j - cnt[v] \* v]这一段是重复的，更进一步的，就有

f[i][j] \= f[i - 1][v] + f[i][j - 1] - f[i - 1][j - (cnt[v] + 1) \* v]

这样一来，就将状态转移的复杂度优化到了O(1)。

需要特别注意的是，这里的j可能不够大。对于j - 2 \* v到j - cnt[v] \* v这些项，若j不够大，那么在f[i][j]和f[i][j - v]里面都不会进行计算，因此无需处理。唯一需要特殊处理的是j - (cnt[v] + 1) \* v这一项，若这里的j不够大，那么在上面的转移方程里面就不需要f[i - 1][j - (cnt[v] + 1) \* v]这一项。

除此之外，在使用滚动数组时需要注意，不能再使用经典的单数组倒序遍历，因为在这里每一项不仅取决于上一轮的项，也取决于本轮新计算出来的j更小的项，因此不能使用单个数组迭代。

最后还有一点是关于0的使用。设0一共有cnt[0]个，那么对于每种可行的方案，都可以额外添加0到cnt[0]个0进去，也就是说最终答案应该乘以(cnt[0] + 1)。

另外再补充一下关于时间复杂度的计算。本题保证了nums之和不超过r的上限2 \* 10^4，那么在极限情况下，nums中最多也就只有sqrt(2 \* 10^4)个不同的数字，因此时间复杂度就是O(r \* sqrt(s))，其中s是nums之和。

最后附上python代码：

```python
class Solution(object):
    def countSubMultisets(self, nums, l, r):
        """
        :type nums: List[int]
        :type l: int
        :type r: int
        :rtype: int
        """

        cnt = {}
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
        
        f = [0] * (r + 1)
        f[0] = 1
        mod = 10 ** 9 + 7

        for v in cnt:
            if v == 0:
                continue
            
            g = f[:]
            for index in range(v, r + 1):
                g[index] += g[index - v]
                if g[index] >= mod:
                    g[index] -= mod
                if index >= (cnt[v] + 1) * v:
                    g[index] -= f[index - (cnt[v] + 1) * v]
                    if g[index] < 0:
                        g[index] += mod
            
            f = g[:]
        
        res = 0
        for index in range(l, r + 1):
            res += f[index]
            if res >= mod:
                res -= mod
        
        return res * (cnt.get(0, 0) + 1) % mod
```
