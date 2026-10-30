---
title: "3500. 将数组分割为子数组的最小代价"
aliases: ["yiduobo的每日leetcode 3500.将数组分割为子数组的最小代价"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/geometry", "leetcode/math", "leetcode/two-pointers", "leetcode/dynamic-programming", "leetcode/prefix-sum", "leetcode/monotonic-queue", "题单/动态规划", "题单/动态规划/五-划分型-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1901104249473066059"
zhihu_id: "1901104249473066059"
zhihu_title: "yiduobo的每日leetcode 3500.将数组分割为子数组的最小代价"
question_id: "3500"
question: "将数组分割为子数组的最小代价"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-divide-array-into-subarrays/"
difficulty: "Hard"
rating: 2569
created: "2025-05-01T04:59:37+08:00"
updated: "2025-05-01T04:59:37+08:00"
upvotes: 0
comments: 0
---

# 3500. 将数组分割为子数组的最小代价

> **[yiduobo的每日leetcode 3500.将数组分割为子数组的最小代价](https://zhuanlan.zhihu.com/p/1901104249473066059) · 知乎 · 2025-05-01 · 赞同 0**
> 力扣：[3500. 将数组分割为子数组的最小代价](https://leetcode.cn/problems/minimum-cost-to-divide-array-into-subarrays/) · Hard · 灵茶山艾府：[两种方法：Abel 求和 + 划分型 DP / O(n) 斜率优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3500.将数组分割为子数组的最小代价

[3500. 将数组分割为子数组的最小代价 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-cost-to-divide-array-into-subarrays/)

题目给出两个长度相等的整数数组nums和cost，长度都不超过1000，另外给出一个整数k。

现在可以将nums分割成若干个子数组，对于第index个子数组，若其的起点和终点分别为left和right，那么其代价为(nums[0] + nums[1] + ... + nums[right] + k \* index) \* (cost[left] + cost[left + 1] + ... + cost[right])。在这里index从1开始计数。

问划分数组的最小总代价。

很有意思的题目。对于数组划分类的题目，一般是往贪心或者动态规划上去靠，本题使用动态规划应该是比较合适的。另一方面，考虑到题目给出的数据规模，最后大概率是使用O(n^2)或者O(n^2 \* logn)的算法。

在这里不妨先写出朴素的动态规划，再看看时间复杂度如何，应该如何优化。

令f[right][index]表示将nums[0]到nums[right]划分为index个子数组时的最小代价，那么对于f[right][index]：

1、若index \= 1，说明并没有进行划分，此时就有

f[right][index] \= (nums[0] + nums[1] + ... + nums[right] + k) \* (cost[0] + cost[1] + ... + cost[right])

注意到其中有一组前缀和以及一组区间和，那么统一都转化为前缀和来进行求解。

令ps_n[index]表示nums中前index项的前缀和，ps_c[index]表示cost中前index项的前缀和，那么上面的式子就可以写成

f[right][index] \= (ps_n[right + 1] + k) \* ps_c[right + 1]

2、若index > 1，则可以枚举最后这一段的左边界left，那么就有

f[right][index] \= min(f[right][index], f[left - 1][index - 1] + (ps_n[right + 1] + k \* index) \* (ps_c[right + 1] - ps_c[left])

到了这里，就到了一种O(n^3)的算法，需要想办法进行优化。

---

一般来说，对于这类划分问题，应该先从转移方程上入手，因为大部分情况下问题都可以转化为某种区间最小值，也许还具备某种单调性，也就是说可能有办法利用单调队列、堆、线段树之类的数据结构优化转移方程。对于本题，考察两个不同的分割点left1和left2，二者的代价分别为

f[left1 - 1][index - 1] + (ps_n[right + 1] + k \* index) \* (ps_c[right + 1] - ps_c[left1])

f[left2 - 1][index - 1] + (ps_n[right + 1] + k \* index) \* (ps_c[right + 1] - ps_c[left2])

消去其中相同的项，剩下的就是

f[left1 - 1][index - 1] - (ps_n[right + 1] + k \* index) \* ps_c[left1]

f[left2 - 1][index - 1] - (ps_n[right + 1] + k \* index) \* ps_c[left2]

一般来说，到了这里就可以找到优化的方法了，但是观察上面的式子可以发现，更新的时机应该是在计算得到f[left1 - 1][index - 1]以及f[left2 - 1][index - 1]的这一刻，然而可能影响到的区间却包含了left1或者left2之后的所有位置，最致命的是这个式子里面还有一项right没消掉，也就是说无法使用区间赋值的方法一次性更新。

到了这里，感觉就没有继续优化转移方程的思路了。

---

另一种做法就是优化状态表示。对于f[right][index]，直接去掉其中一维感觉都不太合适，那么在这里还是从代价计算的方式入手，看看能有哪些变化。

不妨设最终将数组划分成了m段，分割点分别为p[1]、p[2]、...、p[m - 1]，那么总的代价为

(ps_n\[p\[1\]\] + k) \* ps_c\[p\[1\]\] +

(ps_n\[p\[2\]\] + 2 \* k) \* (ps_c\[p\[2\]\] - ps_c\[p\[1\]\]) +

...

(ps_n\[p\[m - 1\]\] + (m - 1) \* k) \* (ps_c\[p\[m - 1\]\] - ps_c\[p\[m - 2\]\]) +

(ps_n\[-1\] + m \* k) \* (ps_c\[-1\] - ps_c\[p\[m - 1\]\])

由于每一项的右侧括号中都是区间和，而这些区间和拼起来恰好是整个区间，那么在这里不妨将这些区间合并试试，具体来说，即

k \* ps_c\[p\[1\]\] + 2 \* k \* (ps_c\[p\[2\]\] - ps_c\[p\[1\]\]) + ... + (m - 1) \* k \* (ps_c\[p\[m - 1\]\] - ps_c\[p\[m - 2\]\]) + m \* k \* (ps_c\[-1\] - ps_c\[p\[m - 1\]\])

先从每一项中都提取一个k出来，即

k \* (ps_c\[p\[1\]\] + (ps_c\[p\[2\]\] - ps_c\[p\[1\]\]) + ... + (ps_c\[p\[m - 1\]\] - ps_c\[p\[m - 2\]\]) + (ps_c\[-1\] - ps_c\[p\[m - 1\]\])) \= k \* ps_c\[-1\]

那么剩下的项为

k \* (ps_c\[p\[2\]\] - ps_c\[p\[1\]\]) + ... + (m - 2) \* k \* (ps_c\[p\[m - 1\]\] - ps_c\[p\[m - 2\]\]) + (m - 1) \* k \* (ps_c\[-1\] - ps_c\[p\[m - 1\]\])

此时式子改写成了

k \* ps_c[-1] +

k \* (ps_c\[p\[2\]\] - ps_c\[p\[1\]\]) + ... + (m - 2) \* k \* (ps_c\[p\[m - 1\]\] - ps_c\[p\[m - 2\]\]) + (m - 1) \* k \* (ps_c\[-1\] - ps_c\[p\[m - 1\]\])

继续提取一个k出来，即

k \* (ps_c\[p\[2\]\] - ps_c\[p\[1\]\]) + ... + k \* (ps_c\[p\[m - 1\]\] - ps_c\[p\[m - 2\]\]) + k \* (ps_c\[-1\] - ps_c\[p\[m - 1\]\]) \= k \* (ps_c\[-1\] - ps_c\[p\[1\]\])

那么剩下的项为

k \* (ps_c\[p\[3\]\] - ps_c\[p\[2\]\]) + ... + (m - 3) \* k \* (ps_c\[p\[m - 1\]\] - ps_c\[p\[m - 2\]\]) + (m - 2) \* k \* (ps_c\[-1\] - ps_c\[p\[m - 1\]\])

此时式子改写成了

k \* ps_c[-1] +

k \* (ps_c\[-1\] - ps_c\[p\[1\]\]) +

k \* (ps_c\[p\[3\]\] - ps_c\[p\[2\]\]) + ... + (m - 3) \* k \* (ps_c\[p\[m - 1\]\] - ps_c\[p\[m - 2\]\]) + (m - 2) \* k \* (ps_c\[-1\] - ps_c\[p\[m - 1\]\])

重复此过程，每一轮都从最后这些项中提取一个k，最后就能得到

k \* ps_c[-1] +

k \* (ps_c\[-1\] - ps_c\[p\[1\]\]) +

... +

k \* (ps_c\[-1\] - ps_c\[p\[m - 2\]\]) +

k \* (ps_c\[-1\] - ps_c\[p\[m - 1\]\])

可以发现，划分次数在这里就已经被消去的，而每进行一次划分，都相当于在最终答案中加上k乘以区间和，因此在这里可以尝试去掉状态表示中的index，不过在这里f的含义也需要修改，其中f[right]表示最后的划分点为right时的最小总代价，那么对于f[right]：

1、如果之前没进行过任何划分：

f[right] \= ps_n[right + 1] \* ps_c[right + 1] + ps_n[-1] \* (ps_c[-1] - ps_c[right + 1]) + k \* ps_c[-1] + k \* (ps_c[-1] - ps_c[right + 1])

其中前两项分别是

(nums[0] + nums[1] + ... + nums[right]) \* (cost[0] + cost[1] + ... + cost[right])

(nums[0] + nums[1] + ... + nums[-1]) \* (cost[right + 1] + cost[right + 2] + ... + cost[-1])

后面两项则是关于k \* index的项在化简后的形式

2、如果之前进行过划分，那么可以枚举之前的最后划分点left。此时最后这段从left + 1到数组末尾的区间，将被重新划分成了left到right以及right + 1到数组末尾这两段。需要特别注意的是，这次重新划分需要重新计算最后这个区间关于前缀和的项。

具体来说，在f[left]中，最后这个区间与前缀和有关的项为

ps_n[-1] \* (ps_c[-1] - ps_c[left + 1])

而在新增分割点right之后，最后这两个区间与前缀和有关的项则分别为

ps_n[right + 1] \* (ps_c[right + 1] - ps_c[left + 1]) + ps_n[-1] \* (ps_c[-1] - ps_c[right + 1])

换言之，在使用f[left]更新f[right]时，需要先把之前的影响消除掉，即

f[right] \= min(f[right], f[left] - ps_n[-1] \* (ps_c[-1] - ps_c[left + 1]) + ps_n[right + 1] \* (ps_c[right + 1] - ps_c[left + 1]) + ps_n[-1] \* (ps_c[-1] - ps_c[right + 1]) + k \* (ps_c[-1] - ps_c[right + 1]))

其中

第一项，减去ps_n[-1] \* (ps_c[-1] - ps_c[left + 1])，表示消除left + 1到末尾的这个区间中前缀和相关式子的影响

第二项和第三项，加上ps_n[right + 1] \* (ps_c[right + 1] - ps_c[left + 1])以及ps_n[-1] \* (ps_c[-1] - ps_c[right + 1])，表示新增分割点right之后，需要添加区间left到right以及区间right + 1到末尾的这两个区间中前缀和相关式子的影响

最后这一项，k \* (ps_c[-1] - ps_c[right + 1])，则是关于k \* index的项在化简后的形式

这样一来，就成功消去了index，整体的时间复杂度优化到了O(n^2)。

---

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, nums, cost, k):
        """
        :type nums: List[int]
        :type cost: List[int]
        :type k: int
        :rtype: int
        """
        
        ps_n = [0]
        for v in nums:
            ps_n.append(ps_n[-1] + v)
        
        ps_c = [0]
        for v in cost:
            ps_c.append(ps_c[-1] + v)

        res = (ps_n[-1] + k) * ps_c[-1]

        if len(nums) > 1:
            f = []
            for right in range(len(nums) - 1):
                f.append(ps_n[right + 1] * ps_c[right + 1] + ps_n[-1] * (ps_c[-1] - ps_c[right + 1]) + k * ps_c[-1] + k * (ps_c[-1] - ps_c[right + 1]))
                for left in range(right):
                    f[-1] = min(f[-1], f[left] - ps_n[-1] * (ps_c[-1] - ps_c[left + 1]) + ps_n[right + 1] * (ps_c[right + 1] - ps_c[left + 1]) + ps_n[-1] * (ps_c[-1] - ps_c[right + 1]) + k * (ps_c[-1] - ps_c[right + 1]))
                res = min(res, f[-1])

        return res
```
