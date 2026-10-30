---
title: "2463. 最小移动总距离"
aliases: ["yiduobo的每日leetcode 2463.最小移动总距离"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/monotonic-queue", "题单/动态规划", "题单/图论算法", "题单/动态规划/五-划分型-DP", "题单/动态规划/十一-优化-DP", "题单/图论算法/八-网络流"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/587021969"
zhihu_id: "587021969"
zhihu_title: "yiduobo的每日leetcode 2463.最小移动总距离"
question_id: "2463"
question: "最小移动总距离"
problem_url: "https://leetcode.cn/problems/minimum-total-distance-traveled/"
difficulty: "Hard"
rating: 2454
created: "2022-11-27T03:27:44+08:00"
updated: "2022-11-27T03:27:44+08:00"
upvotes: 0
comments: 0
---

# 2463. 最小移动总距离

> **[yiduobo的每日leetcode 2463.最小移动总距离](https://zhuanlan.zhihu.com/p/587021969) · 知乎 · 2022-11-27 · 赞同 0**
> 力扣：[2463. 最小移动总距离](https://leetcode.cn/problems/minimum-total-distance-traveled/) · Hard · 灵茶山艾府：[三种方法：记忆化搜索 -> 递推 -> 单调队列优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2463.最小移动总距离

[力扣](https://leetcode.cn/problems/minimum-total-distance-traveled/description/)

首先，由于各个机器人除了初始位置之外并没有其他的差别，那么就断定最终的分配方案中，各个机器人之间不会在除了目的地之外的地方相遇。一个简单的证明是如果两个机器人出现了相遇的情况，那么在原题的描述中是各自继续往前走，但是也可以理解成两个机器人在相遇之后，目的地互换，然后各自掉头往回走，那么最终走到目的地的时候就必然存在一个掉头走的过程，这显然是一种浪费，因此在最终答案中，各个机器人不会出现除目的地之外的相遇情况。

有了这个前提，就可以使用动态规划来进行处理了。令f[i][j]表示前i个机器人送到前j个工厂修理的最小移动总距离，那么对于f[i][j]：

1、第j个工厂可能完全没有发挥作用，那么就有

f[i][j] \= f[i][j - 1]

2、可以安排若干个机器人到第j个工厂进行修理。由于机器人不会出现中途的相遇，因此只能安排前i个机器人中的最后几个到第j个工厂。设p \= factory[j - 1][0]，即p为第j个工厂的位置，那么就有

f[i][j] \= f[i - k][j - 1] + |robot[i - 1] - p| + |robot[i - 2] - p| + ... + |robot[i - k] - p|

表示将robot[i - k]到robot[i - 1]这一共k个机器人送到第j个工厂去修理。需要注意的是，这里的k必须满足1 \<\= k \<\= factory[j - 1][1]

上面这种做法，设机器人的数量为n，工厂的数量为m，那么状态表示的复杂度为O(mn)，转移时需要枚举送去最后一个工厂的机器人数量，同时还需要计算这些机器人到最后一个工厂的距离，因此为O(n^2)，综合起来就是O(mn^3)的复杂度。即使这里m和n的最大值都只有100这个复杂度也是比较勉强的。

在不进行大修改的前提下，状态表示应该是定死了，因此只能从转移上想办法进行优化。由于转移的复杂度主要出现在上面第二种情况中，那么肯定是想办法优化这个部分。

令p \= factory[j - 1][0]，然后将第二种情况的所有可能展开来，就有

f[i][j] \= min(

f[i][j - 1] + 0，

f[i - 1][j - 1] + |robot[i - 1] - p|，

f[i - 2][j - 1] + |robot[i - 1] - p| + |robot[i - 2] - p|，

f[i - 3][j - 1] + |robot[i - 1] - p| + |robot[i - 2] - p| + |robot[i - 3] - p|，

...)

可以发现，对于后面这些绝对值求和的操作，可以利用上一步的求和来进行优化，也就是对于将robot[i - 1]到robot[i - k]这些机器人送去第j个工厂的代价，可以在上一轮计算得到代价的基础上，也就是将robot[i - 1]到robot[i - k + 1]这些机器人送去工厂的代价的基础上，再加上|robot[i - k] - p|

这样一来，计算代价和的复杂度就从O(n)优化到了O(1)，此时O(mn^2)的算法就完全够用了。

当然，在这里状态转移也还有优化的空间，在这里就不展开了。

另外本题采用费用流也是可以处理的，在建图上进行一些优化可以得到非常稀疏的网格图，性能也是相当不错的。

最后附上python代码：

```python
class Solution(object):
    def minimumTotalDistance(self, robot, factory):
        """
        :type robot: List[int]
        :type factory: List[List[int]]
        :rtype: int
        """

        m = len(robot)
        n = len(factory)

        f = [[None] * (n + 1) for _ in range(m + 1)]
        for j in range(n + 1):
            f[0][j] = 0

        robot.sort()
        factory.sort(key=lambda d:d[0])

        s = [0]
        for pos, limit in factory:
            s.append(s[-1] + limit)
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s[j] < i:
                    continue
                
                if f[i][j - 1] is not None:
                    f[i][j] = f[i][j - 1]
                
                cost = 0
                for k in range(1, min(i, factory[j - 1][1]) + 1):
                    cost += abs(robot[i - k] - factory[j - 1][0])
                    if f[i - k][j - 1] is not None and (f[i][j] is None or f[i][j] > f[i - k][j - 1] + cost):
                        f[i][j] = f[i - k][j - 1] + cost
        
        return f[-1][-1]
```
