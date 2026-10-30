---
title: "3180. 执行操作可获得的最大总奖励I & 3181. 执行操作可获得的最大总奖励II"
aliases: ["yiduobo的每日leetcode 3180.执行操作可获得的最大总奖励I && 3181.执行操作可获得的最大总奖励II", "3180. 执行操作可获得的最大总奖励I", "3181. 执行操作可获得的最大总奖励II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bit-manipulation", "leetcode/dynamic-programming", "leetcode/sorting", "题单/动态规划", "题单/动态规划/三-背包", "leetcode/hard", "leetcode/hash-table", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/706066936"
zhihu_id: "706066936"
zhihu_title: "yiduobo的每日leetcode 3180.执行操作可获得的最大总奖励I && 3181.执行操作可获得的最大总奖励II"
question_id: ["3180", "3181"]
question: ["执行操作可获得的最大总奖励 I", "执行操作可获得的最大总奖励 II"]
problem_url: ["https://leetcode.cn/problems/maximum-total-reward-using-operations-i/", "https://leetcode.cn/problems/maximum-total-reward-using-operations-ii/"]
difficulty: ["Medium", "Hard"]
rating: ["1849", "2688"]
created: "2024-06-29T03:27:21+08:00"
updated: "2024-06-29T03:27:21+08:00"
upvotes: 0
comments: 0
---

# 3180. 执行操作可获得的最大总奖励I & 3181. 执行操作可获得的最大总奖励II

> **[yiduobo的每日leetcode 3180.执行操作可获得的最大总奖励I && 3181.执行操作可获得的最大总奖励II](https://zhuanlan.zhihu.com/p/706066936) · 知乎 · 2024-06-29 · 赞同 0**
> 力扣：[3180. 执行操作可获得的最大总奖励 I](https://leetcode.cn/problems/maximum-total-reward-using-operations-i/) · Medium · 灵茶山艾府：[bitset/bigint 优化 0-1 背包（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3181. 执行操作可获得的最大总奖励 II](https://leetcode.cn/problems/maximum-total-reward-using-operations-ii/) · Hard · 灵茶山艾府：[bitset/bigint 优化 0-1 背包 + 两数之和优化（Python/Java/C++/Go）](../3181%20执行操作可获得的最大总奖励%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3180.执行操作可获得的最大总奖励I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-total-reward-using-operations-i/description/)

3181.执行操作可获得的最大总奖励II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-total-reward-using-operations-ii/description/)

题目给出一个长度为n的整数数组rewardValues，另外令x表示获取的总奖励值，初始状态下，x等于0。接下来每一轮，都可以从rewardValues中选出一个未选择过的元素，若其大于x，那么就可以将其累加到x中，问最终可以获得的最大x是多少。

两题的题设相同，第一题的数据规模较小，rewardValues的长度和元素大小均不超过2000；第二题的数据规模较大，rewardValues的长度和元素大小都可以达到50000。

首先根据选择元素值必须大于x这个条件，最终的选择方案中必然不可能出现两个相同的值，因此可以先将rewardValues去重。

接下来，rewardValues中的最大值ma是必然会被选择的，因为如果没有选择ma，那么对于当前的选择方案，使用ma去替代已选择的最大值必然是可行的，同时总奖励值也会更优。根据这一点，就可以将ma从rewardValues中剔除，然后问题就变成了给出一个元素互不相同且都小于ma的数组rewardValues，问通过其中的元素可以构成的不超过ma - 1的最大和是多少。

这是一个非常标准的背包问题。令f\[i\]\[j\]表示是否存在从rewardValues中的前i个元素选出若干个元素使得这些元素的和为j，那么对于f\[i\]\[j\]，如果不选择rewardValues\[i\]，就有f\[i\]\[j\] \= f\[i\]\[j\] or f\[i - 1\]\[j\]，如果选择rewardValues\[i\]，就有f\[i\]\[j\] \= f\[i\]\[j\] or f\[i - 1\]\[j - rewardValues\[i\]\]，当然前提是j > rewardValues\[i\]且j - rewardValues\[i\] \< rewardValues\[i\]。

初始状态下f[0][0] \= true，计算完成后令j从ma - 1到0遍历，找到第一个为true的f[-1][j]，此时的j就是rewardValues中的元素可以组成的不超过ma的最大和，此时的答案就是ma + j。

上面的算法是O(n \* ma)的，这个复杂度处理3180题是足够的，但是对于3181题就比较勉强的。

我在这里没有想出很严谨的优化方法，只好将上面的动态规划写成记忆化搜索的方式，然后在中途进行剪枝。剪枝主要有两个部分：

1、由于需要满足选择的元素大于当前的和，因此可以将rewardValues先从小到大进行排序，接下来对于f[i][j]，可以从i到0倒序遍历rewardValues，若出现某个rewardValues[index] \* 2 \<\= j，即小于当前和的一半，那么就直接停止计算，因为接下来rewardValues中的所有元素都不会超过j的一半。

另外，对于递归计算的子问题，其下一个元素选择的起始下标也必须从当前选择下标的上一个位置开始。

2、在rewardValues排序的前提下，若存在某个i使得f[i][j]为true，那么对于所有满足k >\= i的k，都有f[k][j]为true；反之，若存在某个i使得f[i][j]为false，那么对于满足k \<\= i的k，都有f[k][j]为false。

根据这一点，就可以重新定义f\[v\]为当前计算过程中已知的可以得到和为v的最小前缀，即f\[v\]为可以通过rewardValues\[0\]到rewardValues\[f\[v\]\]构成v的最小下标，而g\[v\]则为当前计算过程中已知的无法得到和为v的最大前缀，即g\[v\]为无法通过rewardValues\[0\]到rewardValues\[g\[v\]\]构成v的最大下标。

那么对于通过前i个元素构造j这一查询，若i >\= f\[j\]，由于通过rewardValues\[0\]到rewardValues\[f\[j\]\]已经可以构成j了，因此通过rewardValues\[0\]到rewardValues\[i\]也必然可以，此时就一定可以构造；同理，若i \<\= g\[j\]，则说明无法构造。

若两种情况都不满足，则只能依然按照上面的处理方法枚举当前选择的元素rewardValues[index]来计算，然后通过计算结果反过来更新f[j]以及g[j]。

这样一来可以省去原来二维的f数组的空间，同时强化之前的记忆化搜索。

以上两个剪枝加上后本题就可以通过了，但是严谨的时间复杂度不知道应该怎么分析。从直观上来看，每次计算时j会衰减一半，但是同一个j可能面对很多个i，而i这一侧则通过f和g起到了一定的优化作用，不过这个优化应该与数据的构造关系很大，不好分析。

最后附上python代码：

```python
class Solution(object):
    def maxTotalReward(self, rewardValues):
        """
        :type rewardValues: List[int]
        :rtype: int
        """

        nums = sorted(list(set(rewardValues)))
        
        ma = nums[-1]
        nums.pop()
        f = [len(nums)] * ma
        f[0] = -1
        g = [-1] * ma

        def calc(v, p):
            if f[v] <= p:
                return True
            if g[v] >= p:
                return False

            while p >= 0 and nums[p] > v:
                p -= 1

            res = False
            for index in range(p, -1, -1):
                if nums[index] * 2 <= v:
                    break
                
                if calc(v - nums[index], index - 1):
                    res = True
                    break

            if res:
                f[v] = min(f[v], p)
            else:
                g[v] = max(g[v], p)
        
            return res
        
        for v in range(ma - 1, -1, -1):
            if calc(v, len(nums) - 1):
                return v + ma
```
