---
title: "3929. 最小分割分数II"
aliases: ["yiduobo的每日leetcode 3929.最小分割分数II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2042013002682159313"
zhihu_id: "2042013002682159313"
zhihu_title: "yiduobo的每日leetcode 3929.最小分割分数II"
question_id: "3929"
question: "最小分割分数II"
problem_url: "https://leetcode.cn/problems/minimum-partition-score-ii/"
created: "2026-05-24T23:54:32+08:00"
updated: "2026-05-24T23:54:39+08:00"
upvotes: 1
comments: 3
---

# 3929. 最小分割分数II

> **[yiduobo的每日leetcode 3929.最小分割分数II](https://zhuanlan.zhihu.com/p/2042013002682159313) · 知乎 · 2026-05-24 · 赞同 1**
> 力扣：[3929. 最小分割分数II](https://leetcode.cn/problems/minimum-partition-score-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3929.最小分割分数II

<https://leetcode.cn/problems/minimum-partition-score-ii/description/>

题目给出一个正整数数组nums以及一个整数k。nums的长度不超过50000，k不超过nums的长度。

现在要求将nums分割成恰好k个子数组，并返回所有有效分割方案中的最小可能分数。

一个分割方案的分数指的是其所有子数组值的总和。

子数组的值定义为sumArr \* (sumArr + 1) / 2，其中sumArr是该子数组元素的总和。

写了好几年的leetcode，这一题应该是遇到过的最难的了，不过也因此学习到了新的技巧。

本题与之前3826题的题设相同，不过数据规模大了很多。

[yiduobo的每日leetcode 3826.最小分割分数](https://zhuanlan.zhihu.com/p/2001442836256679054)

以本题的数据规模，之前的nklogn的算法也不行，必须想办法进一步优化。

关于这个复杂度，仅仅优化掉logn无济于事，而不可能不对nums进行至少一次遍历，因此n这一项也不可能被优化掉，也就是说，这里优化的目标就是把k优化掉。换言之，就是将分割成k个子数组的分割次数限制给去掉。

对于这个问题，有一种处理方法叫做wqs二分，其思路来自于拉格朗日乘数法，通过引入一个惩罚函数叠加在无限制的代价函数上，从而将有次数限制的最优化问题转化为无次数限制的最优化问题。接下来通过调整惩罚函数的惩罚系数大小，使得这个无次数限制的最优化问题的极值落在k这一点，然后通过无次数限制的函数在k这一点的极值，减去惩罚函数值，得到原函数在k这一点的极值，也就是次数限制为k时的最优解。

上述的说明比较难懂，在这里结合本题的题设，给出比较简单的理解。

首先，对于原题，很容易写出带次数限制的动态规划的状态表示，即f[i][j]表示将前i个元素划分为j个子数组的最小可能分数。方便起见，让nums调整为下标1开始计算，然后定义cost(i, j)为(nums[i] + nums[i + 1] + ... + nums[j]) \* (nums[i] + nums[i + 1] + ... + nums[j] + 1) / 2，那么对于f[i][j]，有

f[i][j] \= min(f[p][j - 1] + cost(p + 1, i))

接下来，令g[j] \= f[n][j]，也就是划分j次可以得到的最优解。

首先，这里的g必然是单调递减的，因为根据cost的计算方式，一个和为a + b的子数组的代价为((a + b) ^ 2 + (a + b)) // 2，而拆分成a和b之后，代价为(a^2 + a) // 2 + (b^2 + b) // 2，相比之前少了一项ab，显然是更优的。

另一方面，g是边际效益递减的，也就是说每一次的分割相比上一次，其带来的收益更小。这个也好理解，如果后一次的收益更大，就应该在之前的那一轮就执行这次分割，这样g才会更小。

基于以上两点，g在二维平面上的函数图像，就必然是一条单调递减，且下凸的折线，这条折线的极值在j \= n这一点。

接下来，考虑在这条折线上叠加一条直线y \= λj，这里的λ >\= 0，得到带惩罚的函数h(j) \= g[j] + λj。

想象一个这个叠加的过程，就相当于拿着g在n的这一头，将g往上扭转，变为一个类似y \= x^2的下凸折线的过程。随着λ的增大，这个下凸折线的极值点将从n逐渐向左滑动，而这个滑动的过程是连续的。也就是说，在这里可以通过二分这个λ，然后计算当前h的极值，找出使得满足h在j \= k这一点取得最小值的最大的λ，然后通过当前的h(j)减去λj，得到对应的g[j]，即最小的g[k]，也就是原题需要计算的答案。

关于h(j)，在这里则需要修改原来f的定义，并将λj化入到原来的转移方程。令f[i]表示划分前i个元素的最小可能分数，那么对于f[i]，有f[i] \= min(f[p] + cost(p + 1, i) + λ)，也就是相当于在前一次划分的基础上，需要计算本次划分的代价，并叠加一次划分的惩罚λ。需要注意这里的j已经被消去。

接下来的问题就是如何计算f的极值。在这里可以采用斜率优化进行计算。

对于这个转移方程，可以计算前缀和s，然后把除以2去掉方便计算，得到

f[i] \= min(f[p] + (s[i] - s[p]) \* (s[i] - s[p] + 1) + λ)

接下来拆开括号，可以得到

f[i] \= min(f[p] + s[i]^2 + s[p]^2 - 2 \* s[i] \* s[p] + s[i] - s[p] + λ)

观察这些项，可以分为三类：

1、与决策点p无关的项：s[i]^2 + s[i] + λ

2、仅与决策点p有关的项：f[p] + s[p]^2 - s[p]

3、与两边都有关的项：-2 \* s[i] \* s[p]

接下来，在这里令X(p) \= s[p]，令Y(p) \= f[p] + s[p]^2 - s[p]，那么对于平面上的点(X(p), Y(p))，一条经过这个点，斜率为2 \* s[i]的直线，其截距b恰好就是Y(p) - 2 \* s[i] \* X(p)，也就是上面转移方程中与p有关的所有项

f[p] + s[p]^2 - s[p] + (-2 \* s[i] \* s[p])

为了使得最终的f[i]最小，在这里就应该让上面的f[p] + s[p]^2 - s[p] + (-2 \* s[i] \* s[p])最小，也就是说，对于f[i]选取最优决策点p的过程，实际上可以理解成使用一条斜率为2 \* s[index]的直线，沿着y轴从下往上扫，直到遇到第一个(X(p), Y(p))为止的过程，此时的p就是最优的决策点。

另一方面，前缀和s在这里是单调递增的，也就是说这条用来扫的直线，其斜率2 \* s[i]也是越来越斜的。如果将这些决策点连起来，那么得到的就必然是一个凸的曲线，因此在这里只需通过维护一个凸包来储存这些可能的决策点，就可以将转移的复杂度优化到均摊O(1)。

这里的维护包含两个部分。

第一个部分是对于凸包上的两点(X(p), Y(p))以及和(X(q), Y(q))，若X(p) \< X(q)，且在当前斜率2 \* s[i]的情境下，满足Y(p) - 2 \* s[i] \* X(p) >\= Y(q) - 2 \* s[i] \* X(q)，那么就没有必要再保留p这个决策点了，因为对于后续的f，其对应的s会越来越大，因此上面这个不等式必然成立，也就是说此时q这个决策点必然由于p这个决策点，因此没有再保留p的必要。

换言之，凸包上的点必须满足某种单调性。在这里就可以通过当前的斜率，对比凸包上最老以及第二老的决策点，来决定是否要淘汰掉最老的决策点，并重复此过程直到不需要继续淘汰为止。

第二个部分则是对于当前i，计算完f[i]之后，需要将(X(i), Y(i))加入到凸包中，此时则可以判断凸包中的最新两个点，再加上新加入的(X(i), Y(i))，是否依然是凸的，如果不满足，那么就可以淘汰掉凸包上最新的点，并重复此过程直到不需要继续淘汰为止。

以及以上的讨论，在这里就可以利用一个双端队列来维护这个凸包，而对于每个f[i]，其对应的p就是更新后的凸包上最老的决策点。这样一来，就可以在均摊O(1)的时间内完成状态转移了。

到了这里，就得到了完整的算法：

二分惩罚系数λ，对于当前二分到的λ，计算f[i] \= min(f[p] + (s[i] - s[p]) \* (s[i] - s[p] + 1) + λ)的最优解，这里的s为nums的前缀和。在计算过程中，使用一个数组cnt记录当f[i]取到最值时对应的最大分割次数，cnt遵从cnt[i] \= cnt[p] + 1，也就是f[i]从f[p]转移过来的同时，划分次数cnt[i]在cnt[p]的基础上加上1次。。

计算完成得到f和cnt后，若cnt[n]小于k，说明目前的惩罚系数太大，此时需要调整二分下界为λ - 1，否则调整二分上界为λ即可。

二分结束后，使用二分结果λ再次计算f，反过来计算出最终答案(f[n] - k \* λ) // 2。

需要特别注意的是，在使用斜率优化维护凸包时，如果最老的决策点与次老的决策点关于2 \* s[i]在y轴上的截距相同，那么说明使用这两个决策点的代价是相同的。按照常规的维护方式，在这里将直接放弃掉最老的决策点，但是对于本题，除了f之外，还需要让cnt最大，因此对于这种情况，可以使用最老决策点的cnt来更新次老决策点的cnt，从而保证最终状态转移时，在取到最优决策点的前提下，其对应的cnt也是最多的。

另外再吐槽一句，这种难度的题目放在leetcode确实不太合适。

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

        p2 = []
        for v in s:
            p2.append(v * v)
        
        if k == 1:
            return s[-1] * (s[-1] + 1) // 2

        def calc(lamb):
            f = [0] * (n + 1)
            cnt = [0] * (n + 1)
            # f[index] = min(f[p] + (s[indx] - s[p]) * (s[index] - s[p] + 1) + lam)
            # -> f[p] + s[index]^2 + s[p]^2 - 2 * s[index] * s[p] + s[index] - s[p] + lam
            # -> (s[index]^2 + s[index] + lam) + (f[p] + s[p]^2 - s[p]) + (-2 * s[index] * s[p])

            q = [0] * (n + 1)
            head, tail = 0, 1

            for index in range(1, n + 1):
                while tail - 1 > head:
                    p0 = q[head]
                    p1 = q[head + 1]

                    b0 = f[p0] + p2[p0]
                    b0 -= s[p0]
                    kx = 2 * s[index]
                    kx *= s[p0]
                    b0 -= kx

                    b1 = f[p1] + p2[p1]
                    b1 -= s[p1]
                    kx = 2 * s[index]
                    kx *= s[p1]
                    b1 -= kx

                    if b1 <= b0:
                        #截距相同时，需要使用最老决策点的cnt更新次老决策点的cnt
                        if b1 == b0 and cnt[p0] > cnt[p1]:
                            cnt[p1] = cnt[p0]
                        head += 1
                    else:
                        break

                p = q[head]
                d = s[index] - s[p]
                d *= (d + 1)
                f[index] = f[p] + d
                f[index] += lamb
                cnt[index] = cnt[p] + 1

                while tail - 1 > head:
                    x_index = s[index]
                    y_index = f[index] + p2[index]
                    y_index -= s[index]

                    p_tail1 = q[tail - 1]
                    x_last_1 = s[p_tail1]
                    y_last_1 = f[p_tail1] + p2[p_tail1]
                    y_last_1 -= s[p_tail1]

                    p_tail2 = q[tail - 2]
                    x_last_2 = s[p_tail2]
                    y_last_2 = f[p_tail2] + p2[p_tail2]
                    y_last_2 -= s[p_tail2]

                    x1 = x_index - x_last_2
                    y1 = y_index - y_last_2

                    x2 = x_last_1 - x_last_2
                    y2 = y_last_1 - y_last_2

                    cross = x1 * y2 - x2 * y1
                    if cross > 0:
                        tail -= 1
                    else:
                        break

                q[tail] = index
                tail += 1
            
            return f[-1], cnt[-1]

        left = 0
        right = 10 ** 18
        while left < right:
            mid = (left + right + 1) // 2
            _, cnt = calc(mid)
            if cnt < k:
                right = mid - 1
            else:
                left = mid

        res, _ = calc(left)
        return (res - k * left) // 2
```
