---
title: "983. 最低票价"
aliases: ["yiduobo的每日leetcode 983.最低票价"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/two-pointers", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/363595922"
zhihu_id: "363595922"
zhihu_title: "yiduobo的每日leetcode 983.最低票价"
question_id: "983"
question: "最低票价"
problem_url: "https://leetcode.cn/problems/minimum-cost-for-tickets/"
difficulty: "Medium"
rating: 1786
created: "2021-04-09T18:31:39+08:00"
updated: "2021-04-09T18:31:39+08:00"
upvotes: 0
comments: 0
---

# 983. 最低票价

> **[yiduobo的每日leetcode 983.最低票价](https://zhuanlan.zhihu.com/p/363595922) · 知乎 · 2021-04-09 · 赞同 0**
> 力扣：[983. 最低票价](https://leetcode.cn/problems/minimum-cost-for-tickets/) · Medium · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到三指针优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

983.最低票价

[力扣](https://leetcode-cn.com/problems/minimum-cost-for-tickets/)

动态规划的题目，令f[i]表示满足前days[i - 1]天的最低票价是多少，那么首先可以初始化法法f[0]为0，f[1]为min(cost)，接下来枚举2到n。对于f[i]：

1、可以只买单日票，那么就可以初始化f[i]为f[i] \= f[i - 1] + cost[0]

2、可以在之前的某天买七日票。在当下f[i]的定义下，为了使得这个七日票发挥最大的价值，其必然是从之前某天开始计算，涵盖从之前某天开始直到days[i - 1]。设这个某天在days中对应的下标为w，那么就有f[i] \= min(f[i], f[w - 1] + cost[1])

3、还可以在之前的某天买月票，与情况2类似，月票涵盖了从之前某天开始知道days[i - 1]，设其对应的下标为m，那么就有f[i] \= min(f[i], f[m - 1] + cost[2])

对于w和m的求解，由于days是单调递增的，那么随着i的增大，w和m也必然是随之增大的，因此可以使用两个变量随着i一起向后递推。

最后附上python代码：

```python
class Solution(object):
    def mincostTickets(self, days, costs):
        """
        :type days: List[int]
        :type costs: List[int]
        :rtype: int
        """

        f = [0, min(costs)]
        pos_w = pos_m = 0
        for index in range(1, len(days)):
            f.append(f[-1] + costs[0])
            while days[pos_w] + 6 < days[index]:
                pos_w += 1
            f[-1] = min(f[-1], f[pos_w] + costs[1])
            while days[pos_m] + 29 < days[index]:
                pos_m += 1
            f[-1] = min(f[-1], f[pos_m] + costs[2])

        return f[-1]
```
