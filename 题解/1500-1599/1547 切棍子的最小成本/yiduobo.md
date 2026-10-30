---
title: "1547. 切棍子的最小成本"
aliases: ["yiduobo的每日leetcode 1547.切棍子的最小成本"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/sorting", "题单/动态规划", "题单/动态规划/八-区间-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/425676281"
zhihu_id: "425676281"
zhihu_title: "yiduobo的每日leetcode 1547.切棍子的最小成本"
question_id: "1547"
question: "切棍子的最小成本"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-cut-a-stick/"
difficulty: "Hard"
rating: 2116
created: "2021-10-25T23:17:05+08:00"
updated: "2022-09-06T23:37:40+08:00"
upvotes: 0
comments: 2
---

# 1547. 切棍子的最小成本

> **[yiduobo的每日leetcode 1547.切棍子的最小成本](https://zhuanlan.zhihu.com/p/425676281) · 知乎 · 2021-10-25 · 赞同 0**
> 力扣：[1547. 切棍子的最小成本](https://leetcode.cn/problems/minimum-cost-to-cut-a-stick/) · Hard · 灵茶山艾府：[教你一步步思考区间 DP：从记忆化搜索到递推（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1547.切棍子的最小成本

[力扣](https://leetcode-cn.com/problems/minimum-cost-to-cut-a-stick/)

经典的动态规划问题。方便起见，可以先将cuts按从小到大的顺序进行排序。接下来，这里切割时除了cuts中的位置之外，还存在隐藏边界0和n，方便起见也将这两个数加入到cuts当中。

接下来令f[i][j]表示完成cuts[i]到cuts[j]这一段的切割所需的最小代价，那么对于f[i][j]：

1、若i >\= j - 1，说明cuts[i]到cuts[j]之间没有分割点，因此f[i][j] \= 0

2、若i \< j - 1，那么说明此时存在cuts[i + 1]、cuts[i + 2]、...、cuts[j - 1]这些分割点，那么可以枚举这个分割点cut_pos进行分割，此时分割的代价就是cuts[j] - cuts[i]。另外，此时将棍子分割成了cuts[i]到cuts[cut_pos]以及cuts[cut_pos]到cuts[j]这两个子段，因此就有

f[i][j] \= min(f[i][cut_pos] + f[cut_pos][j]) + cuts[j] - cuts[i]

其中i \< cut_pos \< j

动态规划完成后，f[0][len(cuts) - 1]即为最终答案。

在具体实现时，由于需要先计算子段的值，也就意味着需要优先计算下标跨度较小的f，于是可以先从小到大枚举下标跨度l，然后枚举左边界i，通过i + l - 1计算出右边界j。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, n, cuts):
        """
        :type n: int
        :type cuts: List[int]
        :rtype: int
        """

        cuts = [0] + sorted(cuts) + [n]
        m = len(cuts)
        f = [[None] * m for _ in range(m)]
        for l in range(1, m + 1):
            for i in range(m):
                j = i + l - 1
                if j >= m:
                    continue
                
                if l <= 2:
                    f[i][j] = 0
                else:
                    for cut_pos in range(i + 1, j):
                        if f[i][j] is None or f[i][j] > f[i][cut_pos] + f[cut_pos][j]:
                            f[i][j] = f[i][cut_pos] + f[cut_pos][j]

                    f[i][j] += cuts[j] - cuts[i]

        return f[0][m - 1]
```
