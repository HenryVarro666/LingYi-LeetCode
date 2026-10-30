---
title: "1039. 多边形三角剖分的最低得分"
aliases: ["yiduobo的每日leetcode 1039.多边形三角剖分的最低得分"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/八-区间-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/370508014"
zhihu_id: "370508014"
zhihu_title: "yiduobo的每日leetcode 1039.多边形三角剖分的最低得分"
question_id: "1039"
question: "多边形三角剖分的最低得分"
problem_url: "https://leetcode.cn/problems/minimum-score-triangulation-of-polygon/"
difficulty: "Medium"
rating: 2130
created: "2021-05-07T23:19:38+08:00"
updated: "2021-05-07T23:19:38+08:00"
upvotes: 0
comments: 0
---

# 1039. 多边形三角剖分的最低得分

> **[yiduobo的每日leetcode 1039.多边形三角剖分的最低得分](https://zhuanlan.zhihu.com/p/370508014) · 知乎 · 2021-05-07 · 赞同 0**
> 力扣：[1039. 多边形三角剖分的最低得分](https://leetcode.cn/problems/minimum-score-triangulation-of-polygon/) · Medium · 灵茶山艾府：[【视频】教你一步步思考动态规划，从记忆化搜索到递推（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1038题与之前做过的538题完全一致，在这里就略过了。

1039.多边形三角剖分的最低得分

[力扣](https://leetcode-cn.com/problems/minimum-score-triangulation-of-polygon/)

看题目中给出的图，一个多边形被分割成了一个三角形加上一到两个较小的多边形，那么应该是往动态规划的方向去想。

在这里必须要想办法维护住多边形的区间性质，即f[i][j]表示的点i到点j必须是连续的。因为这里如果没有保证区间性质的话，若此时的i到j之间如果已经被分割出去几个点，那么状态表示的复杂度就上升到指数级别了。这里的点最多有50个，显然是不行的。

因此在这里需要使用f[l][r]表示点l到点r的这一段连续的点，再加上边(i, j)形成的多边形的三角剖分的最低得分，那么进行分割的话只能是从i + 1到j - 1之间找一个点cut_pos，然后将i、j以及cut_pos视为分割出来的三角形，而剩下的的两个部分则是i到cut_pos以及cut_pos到j。

根据上面的结论就可以写出状态转移方程，f[i][j]的定义如上，那么对于f[i][j]，就有

f[i][j] \= min(f[i][cut_pos] + f[cut_pos][j] + values[i] \* values[j] \* values[cut_pos])

其中cut_pos的取值范围为i + 1到j - 1

具体实现时，采用记忆化搜索会比较方便一点。如果采用递推式的动态规划，那么就需要优先计算出区间长度较短的f[i][j]，因此需要优先枚举区间长度l，然后枚举i并通过i + l - 1计算出j，再进行f[i][j]的计算。

最后附上python代码：

```python
class Solution(object):
    def minScoreTriangulation(self, values):
        """
        :type values: List[int]
        :rtype: int
        """

        n = len(values)
        f = [[0] * n for _ in range(n)]
        for l in range(1, n):
            for i in range(n - l):
                j = i + l
                for cut_pos in range(i + 1, j):
                    if f[i][j] == 0 or f[i][j] > f[i][cut_pos] + f[cut_pos][j] + values[i] * values[j] * values[cut_pos]:
                        f[i][j] = f[i][cut_pos] + f[cut_pos][j] + values[i] * values[j] * values[cut_pos]
        
        return f[0][n - 1]
```
