---
title: "LCP 14. 切分数组"
aliases: ["yiduobo的每日leetcode LCP14.切分数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/571333165"
zhihu_id: "571333165"
zhihu_title: "yiduobo的每日leetcode LCP14.切分数组"
question_id: "LCP 14"
question: "切分数组"
problem_url: "https://leetcode.cn/problems/qie-fen-shu-zu/"
created: "2022-10-08T00:19:28+08:00"
updated: "2022-10-08T00:19:28+08:00"
upvotes: 0
comments: 0
---

# LCP 14. 切分数组

> **[yiduobo的每日leetcode LCP14.切分数组](https://zhuanlan.zhihu.com/p/571333165) · 知乎 · 2022-10-08 · 赞同 0**
> 力扣：[LCP 14. 切分数组](https://leetcode.cn/problems/qie-fen-shu-zu/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP14.切分数组

[力扣](https://leetcode.cn/problems/qie-fen-shu-zu/)

又是经典的动态规划问题。令f[i]表示第0到第i个数，这一共i + 1个数最少需要切分出多少个数组，那么对于f[i]，可以枚举0到i之间的每一个数nums[j]，若nums[j]与nums[i]的最大公约数不为1，那么就可以通过f[j - 1] + 1来更新f[i]，那么就有f[i] \= min(f[j - 1] + 1)，其中j为0到i中满足nums[j]与nums[i]不互质的所有下标。

O(n)的状态表示，O(n)的转移，这是一个非常典型的O(n^2)的算法，但是对于本题，由于n的数据规模较大，需要进行优化。

看上去状态表示已经没有什么可优化的了，那么需要从优化状态转移入手。

题目中的切分规则与最大公约数有关，那么对于f[i]，不妨设0到i之间有两个位置j和k，满足nums[j]、nums[k]以及nums[i]都有某个大于1的约数p。在这里可以发现，f[i]显然是由f[j - 1]和f[k - 1]中较小的那一个转移过来的，而对于f[i]后续的所有状态而言，如果是通过公因子p进行的状态转移，那么一定是从具有这个公因子的数nums[x]对应的f[x - 1]转移过来的，这里的f[x - 1]是现有具有公因子p的值对应的f中最小的那个。根据这个结论，很自然想到使用一个数组best来维护当前具有某个因子的数对应的f值的最小值，即best[p]表示当前一直的具有因此p的nums[x]中，f[x - 1]的最小值是多少。更进一步的，对于后续具有因子p的数nums[i]而言，就可以枚举nums[i]的所有质因子p，直接通过best[p]来更新f[i]。

于是现在的做法就变成了枚举nums中的每个数，对于当前枚举到的nums[index]：

1、首先考虑边界情况。当index \= 0时，有f[index] \= 1。同时对于nums[index]的所有质因子p，有best[p] \= 0

2、当index > 0时，可以先初始化f[index]为f[index - 1] + 1。接下来对于nums[index]的所有质因子p，首先使用f[index - 1]来更新best[p]，然后再使用best[p] + 1来更新f[index]

动态规划完成后，f[-1]就是最终答案了。

另外，还有一个问题是如何高效枚举nums[index]的所有质因子p。在这里可以先做一次筛法，找出2到sqrt(max(nums))中的所有素数，并在筛法执行的过程中标记2到max(nums)中每个数最大的质因子。接下来枚举nums中的每个数，通过标记的质因子执行分解质因数的操作，并使用一个哈希表prime_set_map记录每个数拥有哪些质因子。所有数都分解完毕之后，prime_set_map就可以在动态规划执行的过程中来用枚举质因子了。

最后附上python代码：

```python
class Solution(object):
    def splitArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        max_num = max(nums)
        prime = range(max_num + 1)
        now = 2
        while now * now <= max_num:
            if prime[now] == now:
                tmp = now + now
                while tmp <= max_num:
                    prime[tmp] = now
                    tmp += now
            now += 1

        prime_set_map = {}
        for num in nums:
            if num not in prime_set_map:
                prime_set_map[num] = set()
                now = num
                while now != 1:
                    prime_set_map[num].add(prime[now])
                    now /= prime[now]
        
        best = {}
        f = []
        for index in range(len(nums)):
            if index == 0:
                f.append(1)
            else:
                f.append(f[-1] + 1)

            for p in prime_set_map[nums[index]]:
                if index == 0:
                    best[p] = 0
                else:
                    if p not in best or best[p] > f[index - 1]:
                        best[p] = f[index - 1]
                    f[-1] = min(f[-1], best[p] + 1)
        
        return f[-1]
```
