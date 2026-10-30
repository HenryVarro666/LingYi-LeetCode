---
title: "661. 图片平滑器"
aliases: ["yiduobo的每日leetcode 661.图片平滑器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/286757780"
zhihu_id: "286757780"
zhihu_title: "yiduobo的每日leetcode 661.图片平滑器"
question_id: "661"
question: "图片平滑器"
problem_url: "https://leetcode.cn/problems/image-smoother/"
created: "2020-11-11T23:24:53+08:00"
updated: "2020-11-11T23:29:06+08:00"
upvotes: 0
comments: 0
---

# 661. 图片平滑器

> **[yiduobo的每日leetcode 661.图片平滑器](https://zhuanlan.zhihu.com/p/286757780) · 知乎 · 2020-11-11 · 赞同 0**
> 力扣：[661. 图片平滑器](https://leetcode.cn/problems/image-smoother/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

661.图片平滑器

[力扣](https://leetcode-cn.com/problems/image-smoother/)

比较基础的题目，按照题目要求遍历矩阵中每个点，将该点以及周围8个点的值累加到答案矩阵的对应位置上，累加过程中需要注意判断边和角上的特殊情况。累加完成后，最后只需要再除以周围格子总数即可。

最后附上python代码：

```python
class Solution(object):
    def imageSmoother(self, M):
        """
        :type M: List[List[int]]
        :rtype: List[List[int]]
        """

        m = len(M)
        n = len(M[0])

        res = [[0] * n for _ in range(m)]

        for i in range(m):
            for j in range(n):
                res[i][j] = M[i][j]
                cnt = 1

                if i > 0:
                    if j > 0:
                        res[i][j] += M[i - 1][j - 1]
                        cnt += 1
                    res[i][j] += M[i - 1][j]
                    cnt += 1
                    if j < n - 1:
                        res[i][j] += M[i - 1][j + 1]
                        cnt += 1
                
                if j > 0:
                    res[i][j] += M[i][j - 1]
                    cnt += 1
                if j < n - 1:
                    res[i][j] += M[i][j + 1]
                    cnt += 1
                
                if i < m - 1:
                    if j > 0:
                        res[i][j] += M[i + 1][j - 1]
                        cnt += 1
                    res[i][j] += M[i + 1][j]
                    cnt += 1
                    if j < n - 1:
                        res[i][j] += M[i + 1][j + 1]
                        cnt += 1

                res[i][j] /= cnt

        return res
```
