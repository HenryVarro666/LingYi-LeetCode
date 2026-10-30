---
title: "2188. 完成比赛的最少时间"
aliases: ["yiduobo的每日leetcode 2188.完成比赛的最少时间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/536728172"
zhihu_id: "536728172"
zhihu_title: "yiduobo的每日leetcode 2188.完成比赛的最少时间"
question_id: "2188"
question: "完成比赛的最少时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-finish-the-race/"
difficulty: "Hard"
rating: 2315
created: "2022-07-02T16:07:08+08:00"
updated: "2022-07-02T16:07:08+08:00"
upvotes: 0
comments: 0
---

# 2188. 完成比赛的最少时间

> **[yiduobo的每日leetcode 2188.完成比赛的最少时间](https://zhuanlan.zhihu.com/p/536728172) · 知乎 · 2022-07-02 · 赞同 0**
> 力扣：[2188. 完成比赛的最少时间](https://leetcode.cn/problems/minimum-time-to-finish-the-race/) · Hard · 灵茶山艾府：[结合性质巧妙 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2188.完成比赛的最少时间

[力扣](https://leetcode.cn/problems/minimum-time-to-finish-the-race/)

经典的背包形式的动态规划问题，状态g[i][j]表示用前j种轮胎跑完i圈需要的最少时间。不过对于本题，由于轮胎的数目非常多，因此这种状态表示是行不通的，需要另想办法。

注意到题目中每次更换轮胎的时间消耗是一样的，那么可以放弃前j种轮胎的状态表示，改为g[i]表示跑完i圈需要的时间，那么对于g[i]：

1、直接用单种轮胎跑完全程，那么就有g[i] \= min(h[j][i])，这里的h[j][i]表示第j中轮胎跑完i圈需要的最少时间

2、中途换胎，可以枚举换胎前跑了多少圈，那么就有g[i] \= min(g[k] + g[i - k] + changeTime)，其中k的取值范围在1到i - 1之间，表示换胎前跑了k圈

对于第二种情况，状态转移的复杂度为O(n)，是可以满足条件的。但是对于第一种情况，依然涉及到枚举每种轮胎跑完每种圈数，复杂度太高需要优化。

注意到轮胎的消耗是按指数级增长的，因此可以猜测单个轮胎一直跑的时间不会太久。

对于第j种轮胎，不换胎跑x圈的时间消耗为

r_time[j][x] \= h[j][x] \= f[j] + f[j] \* r[j] + f[j] \* r[j]^2 + ... + f[j] \* r[j]^(x - 1)

而如果中间出现一次换胎，那么显然应该在正中间的时刻进行更换，换胎前的时间消耗为

h[j][x / 2] \= f[j] + f[j] \* r[j] + f[j] \* r[j]^2 + ... + f[j] \* r[j]^(x/2 - 1)

换胎后的时间消耗为

h[j][(x + 1) / 2] \= f[j] + f[j] \* r[j] + f[j] \* r[j]^2 + ... + f[j] \* r[j]^((x + 1)/2 - 1)

总的时间消耗就是

c_time[j][x] \= h[j][x / 2] + h[j][(x + 1) / 2] + changeTime

那么在这里只需要从小到大枚举x，找出第一个满足c_time[j][x] \<\= r_time[j][x]的x，就能知道对于第j中轮胎而言，其最多不换胎一直跑x - 1圈，那么只需要在动态规划执行前，先提前预处理出第j种轮胎不换胎跑1到x - 1圈的所有时间消耗，然后用这个时间消耗分别更新g[1]到g[x - 1]即可。

最后附上python代码：

```python
class Solution(object):
    def minimumFinishTime(self, tires, changeTime, numLaps):
        """
        :type tires: List[List[int]]
        :type changeTime: int
        :type numLaps: int
        :rtype: int
        """

        g = [None] * (numLaps + 1)
        for f, r in tires:
            h = [0, f]
            if g[1] is None or g[1] > f:
                g[1] = f
            x = 2
            while x <= numLaps:
                r_time = (h[-1] - h[-2]) * r + h[-1]
                c_time = h[x / 2] + h[(x + 1) / 2] + changeTime
                if r_time >= c_time:
                    break
                h.append(r_time)
                if g[x] is None or g[x] > r_time:
                    g[x] = r_time
                x += 1

        for i in range(2, numLaps + 1):
            for k in range(1, i):
                if g[i] is None or g[i] > g[k] + g[i - k] + changeTime:
                    g[i] = g[k] + g[i - k] + changeTime
        
        return g[-1]
```
