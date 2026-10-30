---
title: "1388. 3n块披萨"
aliases: ["yiduobo的每日leetcode 1388.3n块披萨"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/403219384"
zhihu_id: "403219384"
zhihu_title: "yiduobo的每日leetcode 1388.3n块披萨"
question_id: "1388"
question: "3n块披萨"
problem_url: "https://leetcode.cn/problems/pizza-with-3n-slices/"
created: "2021-08-24T22:55:24+08:00"
updated: "2021-08-24T22:55:24+08:00"
upvotes: 0
comments: 0
---

# 1388. 3n块披萨

> **[yiduobo的每日leetcode 1388.3n块披萨](https://zhuanlan.zhihu.com/p/403219384) · 知乎 · 2021-08-24 · 赞同 0**
> 力扣：[1388. 3n块披萨](https://leetcode.cn/problems/pizza-with-3n-slices/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1388.3n块披萨

[力扣](https://leetcode-cn.com/problems/pizza-with-3n-slices/)

从样例2来看，简单的贪心法应该是行不通的，那么老老实实用动态规划来做。

令f[i][j]表示前i块披萨，从中间选择了j块能得到的最大和，那么对于f[i][j]：

1、若我们没有选择第i块披萨，那么就有f[i][j] \= f[i - 1][j]

2、当然我们也可以选择第i块披萨，这里的前提是我们不能选择第i - 1块披萨，那么就有

f[i][j] \= max(f[i][j], f[i - 2][j - 1]) + slices[i]

另外，需要注意这里的披萨是一个圆，也就是说我们是不能同时选择第一块和最后一块披萨的，一个简单的处理方法是我们强制不选择最后一块，即只对前n - 1块披萨执行动态规划，计算出第一种结果，然后强制不选择第一块，即只对后n - 1块披萨执行动态规划，计算出第二种结果，然后取二者的较大值作为答案。

另外，也有贪心法发挥的地方。对于样例2中的情况，可以抽象成

slices[0]，slices[1]，...，slices[k]，slices[k + 1]，slices[k + 2]，...，slices[n - 1]

其中slices[k + 1]是所有数中最大的，同时slices[k] + sliecs[k + 2] > slices[k + 1]

那么此时应该有两种选法，第一种是选择slices[k + 1]，这样一来不能选择相邻两块slices[k]以及slices[k + 2]。

第二种是选择slices[k]以及slices[k + 2]。这里有一个结论是我们不会单独选择其中一个，下面给出简单的证明：

由于两侧可以认为是对称的，不妨设选择了slices[k]没有选择slices[k + 2]，当然此时也不能选择slices[k + 1]。这种情况下，slices[k]会影响到slices[k - 1]的选择，而在slices[k - 2]之前以及slices[k + 2]之后的披萨选择则完全不受影响，

再考察我们选择slices[k + 1]时的情况。此时我们不能选择slices[k]以及slices[k + 2]，也就是说slices[k - 1]之前的选择不受影响，而slikces[k + 2]之后的披萨选择也不受影响。

对比两种情况，仅选择slices[k]不仅大小相比选择slices[k + 1]较差，同时还会额外影响到slices[k - 1]这块披萨，也就是说仅选择slices[k]是一定不如选择slices[k + 1]的，也就得出了结论，要么选择slices[k + 1]，要么同时选择slices[k]以及slices[k + 2]。

但是仅有上面的结论还不够，因为也有一种情况是我们不选择slices[k]、slices[k + 1]以及slices[k + 2]中的任意一个，因此还无法得出一个可证明的贪心做法。

当然，按上面动态规划做法生成的选择结果来看，是可以使用贪心法的，即slices[k + 1]以及slices[k] + slices[k + 2]这两种情况中必然会选择一种，但由于给不出证明，这里就不继续往下探究了。

最后附上python代码：

```python
class Solution(object):
    def maxSizeSlices(self, slices):
        """
        :type slices: List[int]
        :rtype: int
        """

        n = len(slices)

        f = [[0] * (n / 3 + 1) for _ in range(n)]
        f[0][1] = slices[0]
        f[1][1] = max(slices[0], slices[1])
        for i in range(2, n - 1):
            for j in range(1, n / 3 + 1):
                f[i][j] = f[i - 1][j]
                if j == 1:
                    f[i][j] = max(f[i][j], slices[i])
                elif f[i - 2][j - 1] is not None:
                    f[i][j] = max(f[i][j], f[i - 2][j - 1] + slices[i])
        res = f[n - 2][n / 3]

        f = [[0] * (n / 3 + 1) for _ in range(n)]
        f[1][1] = slices[1]
        f[2][1] = max(slices[1], slices[2])
        for i in range(3, n):
            for j in range(1, n / 3 + 1):
                f[i][j] = f[i - 1][j]
                if j == 1:
                    f[i][j] = max(f[i][j], slices[i])
                elif f[i - 2][j - 1] is not None:
                    f[i][j] = max(f[i][j], f[i - 2][j - 1] + slices[i])
        
        res = max(res, f[n - 1][n / 3])

        return res
```
