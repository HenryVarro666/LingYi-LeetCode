---
title: "1253. 重构2行二进制矩阵"
aliases: ["yiduobo的每日leetcode 1253.重构2行二进制矩阵"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/386158267"
zhihu_id: "386158267"
zhihu_title: "yiduobo的每日leetcode 1253.重构2行二进制矩阵"
question_id: "1253"
question: "重构2行二进制矩阵"
problem_url: "https://leetcode.cn/problems/reconstruct-a-2-row-binary-matrix/"
created: "2021-07-02T21:35:37+08:00"
updated: "2021-07-02T21:35:37+08:00"
upvotes: 0
comments: 0
---

# 1253. 重构2行二进制矩阵

> **[yiduobo的每日leetcode 1253.重构2行二进制矩阵](https://zhuanlan.zhihu.com/p/386158267) · 知乎 · 2021-07-02 · 赞同 0**
> 力扣：[1253. 重构2行二进制矩阵](https://leetcode.cn/problems/reconstruct-a-2-row-binary-matrix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1253.重构2行二进制矩阵

[力扣](https://leetcode-cn.com/problems/reconstruct-a-2-row-binary-matrix/)

我们可以从头开始向后扫描，对于第i列，其元素之和为colsum[i]，那么有三种情况：

1、若colsum[i]为0，说明这一列的两个数都为0，没有什么操作的空间。

2、若colsum[i]为2，说明这一列的两个数都为1，同样没有操作的空间。

3、若colsum[i]为1，说明这一列中有一个0和一个1，可以灵活调配。为了适配upper和lower，若当前upper > lower，那么我们将1安排在第0行，将0安排在第1行，并将upper减去1。反过来，我们将1安排在第1行，将0安排在第0行，并将lower减去1。

扫描完成后，若upper和lower都为0，说明得到了一种合法的答案，否则返回空。

最后附上python代码：

```python
class Solution(object):
    def reconstructMatrix(self, upper, lower, colsum):
        """
        :type upper: int
        :type lower: int
        :type colsum: List[int]
        :rtype: List[List[int]]
        """

        res = [[], []]
        for s in colsum:
            if s == 0:
                res[0].append(0)
                res[1].append(0)
            elif s == 2:
                if upper == 0 or lower == 0:
                    return []
                res[0].append(1)
                res[1].append(1)
                upper -= 1
                lower -= 1
            elif upper == 0 and lower == 0:
                return []
            else:
                if upper > lower:
                    res[0].append(1)
                    res[1].append(0)
                    upper -= 1
                else:
                    res[0].append(0)
                    res[1].append(1)
                    lower -= 1
        
        if upper > 0 or lower > 0:
            return []
        return res
```
