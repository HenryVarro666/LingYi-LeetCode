---
title: "1029. 两地调度"
aliases: ["yiduobo的每日leetcode 1029.两地调度"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/369458820"
zhihu_id: "369458820"
zhihu_title: "yiduobo的每日leetcode 1029.两地调度"
question_id: "1029"
question: "两地调度"
problem_url: "https://leetcode.cn/problems/two-city-scheduling/"
created: "2021-05-02T22:57:32+08:00"
updated: "2021-05-02T22:57:32+08:00"
upvotes: 2
comments: 0
---

# 1029. 两地调度

> **[yiduobo的每日leetcode 1029.两地调度](https://zhuanlan.zhihu.com/p/369458820) · 知乎 · 2021-05-02 · 赞同 2**
> 力扣：[1029. 两地调度](https://leetcode.cn/problems/two-city-scheduling/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1029.两地调度

[力扣](https://leetcode-cn.com/problems/two-city-scheduling/)

动态规划算法是很容易想到的，令f[i][j]表示前i个人，其中有j个去了A地的最小代价，那么对于f[i][j]，若此时的第i个人没有去A地，那么就是前i - 1个人中有j个去了A地，然后第i个人没有去A地。若此时的地i个人去了A地，那么就是前i - 1个人中有j - 1个去了A地，再加上地i个人去了A地凑够了j个去A地的人。综合起来，就有

f[i][j] \= min(f[i - 1][j] + cost[i - 1][1], f[i - 1][j - 1] + cost[i - 1][0])

对于j等于0的情况，所有人只能去B地，因此有f[i][0] \= f[i - 1][0] + cost[i - 1][1]

最初始的边界条件则是f[0][0] \= 0，而最终答案就是f[n][n / 2]，其中n为总人数。

以上动态规划的做法是O(n^2)的，但是这里存在更好的做法。

不妨先假设所有的人都去的A地，那么此时的总代价为sum(cost[i][0])。接下里，我们需要将其中n/2个人移动到B地，而对于第i个人，移动的代价为delta[i] \= cost[i][1] - cost[i][0]。为了使得总代价最低，我们就只需要找到最小的n / 2个delta[i]，然后移动对应的人去B地即可。于是一个自然的想法就是先计算出delta，然后从小到大排序之后选取前n / 2个，将这些delta求和之后叠加到答案上即可。

最后附上python代码：

```python
class Solution(object):
    def twoCitySchedCost(self, costs):
        """
        :type costs: List[List[int]]
        :rtype: int
        """

        delta = sorted([x[1] - x[0] for x in costs])
        res = sum(x[0] for x in costs) + sum(delta[:len(costs) / 2])
        return res
```
