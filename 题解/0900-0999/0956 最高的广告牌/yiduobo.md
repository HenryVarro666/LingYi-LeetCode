---
title: "956. 最高的广告牌"
aliases: ["yiduobo的每日leetcode 956.最高的广告牌"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/360356357"
zhihu_id: "360356357"
zhihu_title: "yiduobo的每日leetcode 956.最高的广告牌"
question_id: "956"
question: "最高的广告牌"
problem_url: "https://leetcode.cn/problems/tallest-billboard/"
created: "2021-03-27T16:52:42+08:00"
updated: "2021-03-27T16:52:42+08:00"
upvotes: 1
comments: 0
---

# 956. 最高的广告牌

> **[yiduobo的每日leetcode 956.最高的广告牌](https://zhuanlan.zhihu.com/p/360356357) · 知乎 · 2021-03-27 · 赞同 1**
> 力扣：[956. 最高的广告牌](https://leetcode.cn/problems/tallest-billboard/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

956.最高的广告牌

[力扣](https://leetcode-cn.com/problems/tallest-billboard/)

虽然题目最多只有20根钢筋，但是如果直接使用dfs的话，那么会有3^20种可能的状态，不加以剪枝的话肯定是不行的。

另外，注意到这里钢筋长度之和最多为5000，那么使用类似背包问题的冬天规划也是很容易想到的。令状态f[i][j][k]表示前i根钢筋，是否能搭建左侧高度为j，右侧高度为k的支架。不过这种状态表示法的时间复杂度依然很高，需要想办法进行优化。

注意到对于f[i][j][k]这个状态，我们最终想要的是j等于k，且j和k尽可能大。这个状态表示是01的，可以认为是浪费掉了一个维度。换言之，我们关注的是j和k绝对值之差，以及j和k的绝对值大小，其中绝对值之差是限制条件，而j和k的绝对值大小是优化目标。由于最终合法答案下的绝对值之差必然为0，因此j和k的绝对值大小也可以转换为j + k之和，这个和越大j和k就越大。

因此可以将状态改造成f[i][d]表示前i根钢筋，构造出两侧绝对值之差为d的支架时，两侧高度之和是多少。

那么对于f[i][d]而言，第i + 1根钢筋对应的是rods[i]：

1、可以不选择第i根钢筋，就有f[i + 1][d] \= f[i][d]

2、也可以将第i根焊接到当前较高的那一侧，那么此时两侧的差值就是d + rods[i]，于是有

f\[i + 1\]\[d + rods\[i\]\] \= max(f\[i + 1\]\[d + rods\[i\]\], f\[i\]\[d\] + rods\[i\])

3、当然也可以将第i根焊接到当前较矮的那一侧，那么此时若d > rods[i]，那么差值就是d - rods[i]，否则就是rods[i] - d，也就是abs(d - rods[i])，于是有

f[i + 1][abs(d - rods[i])] \= max(f[i + 1][abs(d - rods[i])], f[i][d] + rods[i])

处理完成后，最终f[len(rods) + 1][0]表示的就是所有钢筋达成高度相等的两侧时的最大高度之和，除以2就可以得到最终答案了。

最后附上python代码：

```python
class Solution(object):
    def tallestBillboard(self, rods):
        """
        :type rods: List[int]
        :rtype: int
        """

        s = sum(rods)
        max_len = s / 2
        f = [[None] * (max_len + 1) for _ in range(len(rods) + 1)]
        f[0][0] = 0

        for i, rod in enumerate(rods):
            for j in range(0, max_len + 1):
                if f[i][j] is not None:
                    if f[i + 1][j] is None or f[i + 1][j] < f[i][j]:
                        f[i + 1][j] = f[i][j]

                    if j + rod <= max_len:
                        if f[i + 1][j + rod] is None or f[i + 1][j + rod] < f[i][j] + rod:
                            f[i + 1][j + rod] = f[i][j] + rod
                    
                    if abs(j - rod) <= max_len:
                        if f[i + 1][abs(j - rod)] is None or f[i + 1][abs(j - rod)] < f[i][j] + rod:
                            f[i + 1][abs(j - rod)] = f[i][j] + rod
        
        return f[-1][0] / 2
```
