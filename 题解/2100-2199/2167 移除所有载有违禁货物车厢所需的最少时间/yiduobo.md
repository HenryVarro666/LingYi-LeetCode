---
title: "2167. 移除所有载有违禁货物车厢所需的最少时间"
aliases: ["yiduobo的每日leetcode 2167.移除所有载有违禁货物车厢所需的最少时间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/string", "leetcode/dynamic-programming", "leetcode/dp", "leetcode/dp-2", "题单/动态规划", "题单/动态规划/七-其他线性-DP", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/533492044"
zhihu_id: "533492044"
zhihu_title: "yiduobo的每日leetcode 2167.移除所有载有违禁货物车厢所需的最少时间"
question_id: "2167"
question: "移除所有载有违禁货物车厢所需的最少时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-remove-all-cars-containing-illegal-goods/"
difficulty: "Hard"
rating: 2219
created: "2022-06-25T00:43:12+08:00"
updated: "2022-06-25T00:43:12+08:00"
upvotes: 0
comments: 0
---

# 2167. 移除所有载有违禁货物车厢所需的最少时间

> **[yiduobo的每日leetcode 2167.移除所有载有违禁货物车厢所需的最少时间](https://zhuanlan.zhihu.com/p/533492044) · 知乎 · 2022-06-25 · 赞同 0**
> 力扣：[2167. 移除所有载有违禁货物车厢所需的最少时间](https://leetcode.cn/problems/minimum-time-to-remove-all-cars-containing-illegal-goods/) · Hard · 灵茶山艾府：[前后缀分解 + DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2167.移除所有载有违禁货物车厢所需的最少时间

[力扣](https://leetcode.cn/problems/minimum-time-to-remove-all-cars-containing-illegal-goods/)

题目中移除前缀和后缀车厢时每节车厢的代价是1，而直接移除中部车厢的代价则为2，那么最终答案必然是由移除前缀0到i - 1之间的车厢、移除后缀j + 1到n - 1的车厢，以及以代价2直接移除i到j之间的车厢三部分组成。

对于这3个部分，前缀和后缀的代价是很容易计算的，而对于中间部分则需要直到区间i到j之间有多少节违禁车厢。这是一个典型的区间和问题，还是老样子，转化成前缀和来进行求解。设sum[i]表示第0到i节车厢中违禁车厢的总数，那么区间i到j之间违禁车厢的数目就是sum[j] - sum[i - 1]。

由于题目中n的规模并不小，直接枚举i和j的O(n^2)的做法显然是行不通的，必须进行优化。

不妨从代价之和入手进行考虑。根据上面的结论，对于任意一组i和j，总的代价为

cost \= ((i - 1) - 0 + 1) + ((n - 1) - (j + 1) + 1) + 2 \* (sum[j] - sum[i - 1])

整理一下这个式子可以得到

cost \= n - 1 + (i - 2 \* sum[i - 1]) + (2 \* sum[j] - j)

对于构成cost的三个部分，n - 1为常量不需要考虑，而对于i和j组成的两个部分，则可以先将其中一个部分固定下来，然后想办法在O(1)或者O(logn)的时间内求出另一个部分的最小值，从高效的求出最终的答案。

在这里我选择的是枚举j的位置，将j固定下来后，i的取值范围就是0到j之间。令f[j]表示当i的取值在0到j之间时，i - 2 \* sum[i - 1]的最小值，那么对于f[j]就有

f[j] \= min(0，1 - 2 \* sum[0], 2 - 2 \* sum[1] , ..., p - 2 \* sum[p - 1])

另一方面，f[p - 1]为

f[j - 1] \= min(0, 1 - 2 \* sum[0], 2 - 2 \* sum[1], ..., p - 1 - 2 \* sum[j - 2])

可以发现，在这里f[p]可以通过f[j] \= min(f[j - 1], j - 2 \* sum[j - 1])来进行求解。

换言之，在随着j的向后遍历，每一轮的f[j]就可以在O(1)的时间内通过f[j - 1]以及sum[j - 1]求解出来。这样一来，确定移除第j + 1到n - 1节车厢的最小代价就是f[j] + 2 \* sum[j] - j + n - 1。一趟遍历，求解出所有j对应的f[j]并更新答案即可。

需要注意的是，这种算法在遇到j \= n - 1且对应的最优的i \= 0时，会出现将所有火车车厢都当做中部车厢移除的情况，这个显然是有问题的。对于移除全部车厢的情况，最终的代价应该是n，因此在这里可以使用n来初始化答案，避免这种有问题的情况发生。

另外，注意到f的每一轮只与上一轮有关，因此可以使用变量滚动替换掉f数组。同样的，sum[j - 1]在参与完f[j]的计算后，sum[j]将马上参与答案的计算，因此在这里同样可以使用变量滚动替换掉sum数组。具体实现时先使用这个遍历更新f，然后将其累加上s[j]，再用累加后的结果更新答案。

最后附上python代码：

```python
class Solution(object):
    def minimumTime(self, s):
        """
        :type s: str
        :rtype: int
        """

        n = len(s)
        res = n
        now = 0
        left = n

        for index, char in enumerate(s):
            left = min(left, index - now - now)
            now += int(char)
            res = min(res, left + now + now - index + n - 1)
        
        return res
```
