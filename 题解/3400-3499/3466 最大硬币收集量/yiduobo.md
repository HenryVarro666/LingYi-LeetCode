---
title: "3466. 最大硬币收集量"
aliases: ["yiduobo的每日leetcode 3466.最大硬币收集量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1895595512058589849"
zhihu_id: "1895595512058589849"
zhihu_title: "yiduobo的每日leetcode 3466.最大硬币收集量"
question_id: "3466"
question: "最大硬币收集量"
problem_url: "https://leetcode.cn/problems/maximum-coin-collection/"
created: "2025-04-15T22:06:26+08:00"
updated: "2025-04-15T22:06:26+08:00"
upvotes: 0
comments: 0
---

# 3466. 最大硬币收集量

> **[yiduobo的每日leetcode 3466.最大硬币收集量](https://zhuanlan.zhihu.com/p/1895595512058589849) · 知乎 · 2025-04-15 · 赞同 0**
> 力扣：[3466. 最大硬币收集量](https://leetcode.cn/problems/maximum-coin-collection/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3466.最大硬币收集量

[3466. 最大硬币收集量 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-coin-collection/description/)

马里奥在双车道的高速公路上行驶，其中每英里上都有硬币。给出两个整数数组lane1和lane2，若马里奥在车道1上处于第index英里处，且lane1[index] > 0，那么马里奥获得lane1[index]枚硬币；反之若lane1[index] \< 0，马里奥则失去lane1[index]枚硬币，这个规则同样适用于lane2。

马里奥可以在任何地方进入高速，并在行驶至少一英里后退出。马里奥只能从1号车道进入高速，且可以变换车道最多两次，切换车道可以在进入高速或者离开高速前立即执行。

问马里奥可以收集到的最多硬币数量。

经典的子段和问题，不过在这里有两个数组且可以进行切换，那么在这里使用动态规划会更直观点。为了覆盖住这两次变道的机会，可以令f[index]、g[index]、h[index]分别表示在变道了0、1、2次，且当前位于第index英里时可以收集到的最大硬币数量，那么：

1、对于f[index]，其可以从第1车道的index - 1处走来，也可以是在index处才上高速，因此有

f[index] \= max(f[index - 1], 0) + lane1[index]

2、对于g[index]，其可以从第1车道的index - 1处变道过来，也可以是从第2车道的index - 1处走来，还可以是在index处上高速然后立即变道，因此有

g[index] \= max(f[index - 1], g[index - 1], 0) + lane2[index]

这里加上lane2[index]是因为g表示的是经过一次变道后的状态，此时必然位于第2车道上

3、对于h[index]，其可以从第1车道的index - 1走来，也可以是从第2车道的index - 1处变道过来，因此有

h[index] \= max(h[index - 1], g[index - 1]) + lane1[index]

而最终答案就是f、g、h中的最大值。另外注意到f、g、h都只依赖于上一轮的结果，那么在这里只需按照h、g、f的顺序来进行更新，就可以通过三个变量迭代来省去数组的空间了。

最后附上python代码：

```python
class Solution(object):
    def maxCoins(self, lane1, lane2):
        """
        :type lane1: List[int]
        :type lane2: List[int]
        :rtype: int
        """
        
        f, g, h = 0, 0, 0
        res = None

        for x, y in zip(lane1, lane2):
            h = max(g, h) + x
            g = max(f, g, 0) + y
            f = max(f, 0) + x
            max_v = max(f, g, h)
            if res is None or res < max_v:
                res = max_v
        
        return res
```
