---
title: "3826. 最小分割分数"
aliases: ["yiduobo的每日leetcode 3826.最小分割分数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/queue", "leetcode/geometry", "leetcode/math", "leetcode/dynamic-programming", "leetcode/prefix-sum", "leetcode/monotonic-queue", "题单/动态规划", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2001442836256679054"
zhihu_id: "2001442836256679054"
zhihu_title: "yiduobo的每日leetcode 3826.最小分割分数"
question_id: "3826"
question: "最小分割分数"
problem_url: "https://leetcode.cn/problems/minimum-partition-score/"
difficulty: "Hard"
rating: 2345
created: "2026-02-03T22:10:31+08:00"
updated: "2026-05-24T22:48:06+08:00"
upvotes: 0
comments: 0
---

# 3826. 最小分割分数

> **[yiduobo的每日leetcode 3826.最小分割分数](https://zhuanlan.zhihu.com/p/2001442836256679054) · 知乎 · 2026-02-03 · 赞同 0**
> 力扣：[3826. 最小分割分数](https://leetcode.cn/problems/minimum-partition-score/) · Hard · 灵茶山艾府：[划分型 DP + 斜率优化（凸包优化）Python/Java/C++/Go](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3826.最小分割分数

<https://leetcode.cn/problems/minimum-partition-score/description/>

题目给出一个正整数数组nums以及一个整数k。nums的长度不超过10000，同时k不超过nums的长度。

现在要求将nums分割成恰好k个子数组，并返回所有有效分割方案中的最小可能分数。

一个分割方案的分数指的是其所有子数组值的总和。

子数组的值定义为sumArr \* (sumArr + 1) / 2，其中sumArr是该子数组元素的总和。

标准的划分形动态规划，令f[i][j]表示将前i个元素划分为j个子数组的最小可能分数。方便起见，让nums调整为下标1开始计算，然后定义cost(i, j)为(nums[i] + nums[i + 1] + ... + nums[j]) \* (nums[i] + nums[i + 1] + ... + nums[j] + 1) / 2，那么对于f[i][j]，有

f[i][j] \= min(f[p][j - 1] + cost(p + 1, i))

即对于f[i][j]，可以枚举最后这一段的起点p + 1，然后使用f[p][j - 1]加上最后这一段的分数来更新f[i][j]。

对于cost的计算，由于其与子数组和有关，也就是与区间和有关，因此在这里可以先计算nums的前缀和s，那么cost(i, j)就可以写作(s[j] - s[i - 1]) \* (s[j] - s[i - 1] + 1) / 2。

加入前缀和的优化之后，以上算法的时间复杂度为O(n^2 \* k)，还需要继续进行优化。

---

对于动态规划的优化，无非就是从状态表示和转移方程两方面来想办法。对于状态表示，虽然可以利用滚动数组优化掉j这一维，但是实际上依然需要遍历O(nk)的状态，省去任意一维都无法继续计算，因此只能从转移方程上来想办法。

对于上面的转移方程，实际上是要找一个最优的决策点，因此首先想到使用单调性进行优化。

对于f[p][j - 1]以及cost(p + 1, i)这两个部分，随着p的增加，f[p][j - 1]是单调递增的，而cost(p + 1, i)是单调递减的，因此简单的单调性优化在这里是无法使用的。

---

简单的单调性优化无法使用，接下来可以试试决策点优化。

所谓决策点优化，指的是对于上面这种形式的转移方程，可能满足对于f[i][j]对应的最优的p，f[i + 1][j]对应的最优的p'必然大于等于p。

当然，这个优化的前提不一定成立，还需要给出证明：

不妨设f[i][j]对应的最优决策点为p，而f[i + 1][j]对应的最优决策点p'小于p，那么就有

f[p'][j - 1] + cost(p' + 1, i + 1) \< f[p][j - 1] + cost(p + 1, i + 1)

即

f[p'][j - 1] - f[p][j - 1] \< cost(p + 1, i + 1) - cost(p' + 1, i + 1)

将后面cost相减拆开，可以得到

(s[i + 1] - s[p]) \* (s[i + 1] - s[p] + 1) - (s[i + 1] - s[p']) \* (s[i + 1] - s[p'] + 1)

将s[i + 1]写作s[i] + nums[i + 1]，减号左侧就可以写成

left \= (nums[i + 1] + s[i] - s[p]) \* (nums[i + 1] + s[i] - s[p] + 1)

而减号右侧则为

right \= (nums[i + 1] + s[i] - s[p']) \* (nums[i + 1] + s[i] - s[p'] + 1)

提出其中nums[i + 1]有关的项，就有

left \= nums[i + 1]^2 + (s[i] \* 2 - s[p] \* 2 + 1) \* nums[i + 1] + cost(p + 1, i)

right \= nums[i + 1]^2 + (s[i] \* 2 - s[p'] \* 2 + 1) \* nums[i + 1] + cost(p' + 1, i)

还原到left - right，就有

cost(p + 1, i + 1) - cost(p' + 1, i + 1) \= nums[i + 1] \* (s[p'] - s[p]) \* 2 + cost(p + 1, i) - cost(p' + 1, i)

由于p' \< p且nums是正整数数组，因此s[p'] \< s[p]，即nums[i + 1] \* (s[p'] - s[p]) \* 2这一项小于0，因此就有

cost(p + 1, i + 1) - cost(p' + 1, i + 1) \< cost(p + 1, i) - cost(p' + 1, i)

代入回上面的f[p'][j - 1] - f[p][j - 1] \< cost(p + 1, i + 1) - cost(p' + 1, i + 1)，就有

f[p'][j - 1] - f[p][j - 1] \< cost(p + 1, i) - cost(p' + 1, i)

即

f[p'][j - 1] + cost(p' + 1, i) \< f[p][j - 1] + cost(p + 1, i)

可以发现，小于号左侧表示的是f[i][j]从f[p'][j - 1]转移过来的代价，而右侧表示的则是f[i][j]从f[p][j - 1]转移过来的代价。

也就是说，对于f[i][j]，通过p'转移过来的代价比通过p转移过来的代价更优，与p是f[i][j]对应的最优决策点矛盾了，因此对于f[i + 1][j]，其对应的最优决策点p'必然大于等于f[i][j]的最优决策点p。

基于上面的结论，对于某个特定的j，如果想计算对应的f[1][j]到f[n][j]，就可以令mid \= (1+ n) // 2，然后可以枚举出f[mid][j]对应的最优决策点p。

更进一步的，f[1][j]到f[mid - 1][j]对应的最优决策点必然都小于等于p，而f[mid + 1][j]到f[n][j]的最优决策点必然都大于等于p，也就是说对于[1, mid - 1]，决策点区间被缩减到了[0, p]，而对于[mid + 1, n]，决策点区间被缩减到了[p, n - 1]。接下来只需递归计算这两个区间就行了，总的时间复杂度优化到了O(nklogn)。

最后附上python代码：

```python
class Solution(object):
    def minPartitionScore(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        n = len(nums)
        s = [0]
        for v in nums:
            s.append(s[-1] + v)
        
        def calc(x, y, left, right):
            mid = (x + y) // 2
            mi = None
            mi_p = None
            for p in range(left, right + 1):
                if g[p] is not None:
                    cost = g[p] + (s[mid] - s[p]) * (s[mid] - s[p] + 1) // 2
                    if mi is None or mi > cost:
                        mi = cost
                        mi_p = p
            
            f[mid] = mi
            if x < mid:
                calc(x, mid - 1, left, mi_p)
            if mid < y:
                calc(mid + 1, y, mi_p, right)

        f = [None] * (n + 1)
        f[0] = 0
        for _ in range(k):
            g = f[:]
            f = [-1] * (n + 1)

            calc(1, n, 0, n - 1)
        
        return f[-1]
```
