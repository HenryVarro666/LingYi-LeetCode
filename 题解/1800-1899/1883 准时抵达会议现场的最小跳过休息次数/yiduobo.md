---
title: "1883. 准时抵达会议现场的最小跳过休息次数"
aliases: ["yiduobo的每日leetcode 1883.准时抵达会议现场的最小跳过休息次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/477321784"
zhihu_id: "477321784"
zhihu_title: "yiduobo的每日leetcode 1883.准时抵达会议现场的最小跳过休息次数"
question_id: "1883"
question: "准时抵达会议现场的最小跳过休息次数"
problem_url: "https://leetcode.cn/problems/minimum-skips-to-arrive-at-meeting-on-time/"
difficulty: "Hard"
rating: 2588
created: "2022-03-07T23:16:39+08:00"
updated: "2022-03-07T23:16:40+08:00"
upvotes: 1
comments: 0
---

# 1883. 准时抵达会议现场的最小跳过休息次数

> **[yiduobo的每日leetcode 1883.准时抵达会议现场的最小跳过休息次数](https://zhuanlan.zhihu.com/p/477321784) · 知乎 · 2022-03-07 · 赞同 1**
> 力扣：[1883. 准时抵达会议现场的最小跳过休息次数](https://leetcode.cn/problems/minimum-skips-to-arrive-at-meeting-on-time/) · Hard · 灵茶山艾府：[教你一步步思考动态规划：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1883.准时抵达会议现场的最小跳过休息次数

[力扣](https://leetcode-cn.com/problems/minimum-skips-to-arrive-at-meeting-on-time/)

题目问的是抵达会议所需的最小跳过次数，直接求解起来比较困难，因为不知道要如何安排在什么地方跳过，那么不妨转换思路，考虑跳过若干次之后最早什么时候可以抵达会议现场。一共n段道路，最多跳过n - 1次，那么不妨计算出对于每种跳过次数，最早能到达会议现场的时间，其中到达时间小于等于规定时间的最少跳过次数就是最终答案。

对于这个转化后的问题，则是一个经典的动态规划套路。令f[i][j]表示通过第0到i条道路，跳过了其中j次休息时所需的最少时间。很明显，对于这种状态表示方法，必须要满足j \< i + 1。那么对于f[i][j]：

1、当i \= 0时，没得跳过这种说法，因此就有f[i][j] \= dist[0] / speed

2、对于其他情况：

首先可以选择不跳过最后这次休息，那么就相当于第0到第i - 1段道路中跳过了j次休息，然后在走过第i - 1段道路之后进行了休息，最后再走过第i段道路。走过第0到i - 1段道路跳过了j次休息所需的时间是f[i - 1][j]，之后进行了休息，因此就是ceil(f[i - 1][j])，这里ceil表示向上取整。最后还需要走过第i段道路，所需时间为dist[i] / speed，因此综合起来就是

f[i][j] \= ceil(f[i - 1][j]) + dist[i] / speed

当然，也可以选择跳过最后这次休息，那么就相当于第0到第i - 1段道路中跳过了j - 1次休息，然后在走过第i - 1段道路后里面走第i段道路。前者所需时间是f[i - 1][j - 1]，后者同样是dist[i] / speed，因此综合起来就是

f[i][j] \= min(f[i][j], f[i - 1][j - 1] + dist[i] / speed)

需要注意的是，这种情况默认了跳过最后这次休息，因此必须要j > 0时才成立

注意到这里每一轮的状态只与上一轮有关，因此可以使用滚动数组优化掉i这一维。另外，在这里由于是实数计算，可能会丢失精度，但是这里除法的分母全都是speed，因此可以使用分数而不是实数来表示状态的结果，避免丢精度的问题。

最后附上python代码：

```python
class Solution(object):
    def minSkips(self, dist, speed, hoursBefore):
        """
        :type dist: List[int]
        :type speed: int
        :type hoursBefore: int
        :rtype: int
        """

        f = [dist[0]]

        for i in range(1, len(dist)):
            g = f[:]
            f = []
            for j in range(i):
                if g[j] % speed == 0:
                    t = g[j]
                else:
                    t = (g[j] / speed + 1) * speed
                
                f.append(t + dist[i])
                
                if j > 0:
                    f[-1] = min(f[-1], g[j - 1] + dist[i])
            
            f.append(g[-1] + dist[i])
        
        if f[-1] > speed * hoursBefore:
            return -1
        
        res = 0
        while f[res] > speed * hoursBefore:
            res += 1
        return res
```
