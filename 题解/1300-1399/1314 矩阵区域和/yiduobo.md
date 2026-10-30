---
title: "1314. 矩阵区域和"
aliases: ["yiduobo的每日leetcode 1314.矩阵区域和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/392848974"
zhihu_id: "392848974"
zhihu_title: "yiduobo的每日leetcode 1314.矩阵区域和"
question_id: "1314"
question: "矩阵区域和"
problem_url: "https://leetcode.cn/problems/matrix-block-sum/"
created: "2021-07-24T22:19:10+08:00"
updated: "2021-07-24T22:19:10+08:00"
upvotes: 1
comments: 0
---

# 1314. 矩阵区域和

> **[yiduobo的每日leetcode 1314.矩阵区域和](https://zhuanlan.zhihu.com/p/392848974) · 知乎 · 2021-07-24 · 赞同 1**
> 力扣：[1314. 矩阵区域和](https://leetcode.cn/problems/matrix-block-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1314.矩阵区域和

[力扣](https://leetcode-cn.com/problems/matrix-block-sum/)

矩阵区域和问题一般都会转化为二维前缀和来进行处理，之前1292题的题解中已经讲述了使用二维前缀和处理矩阵区域和的原理，传送门在这里

[yiduobo：yiduobo的每日leetcode 1292.元素和小于等于阈值的正方形的最大边长](https://zhuanlan.zhihu.com/p/390124624)

回到本题，我们可以先预处理出所有的二维前缀和，然后枚举每个格子，并计算以这个格子为中心的二维矩阵范围，然后利用前缀和求出矩阵和并加入到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def matrixBlockSum(self, mat, k):
        """
        :type mat: List[List[int]]
        :type k: int
        :rtype: List[List[int]]
        """

        m = len(mat)
        n = len(mat[0])
        s = [[0] * n for _ in range(m)]

        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        s[i][j] = mat[i][j]
                    else:
                        s[i][j] = s[i][j - 1] + mat[i][j]
                elif j == 0:
                    s[i][j] = s[i - 1][j] + mat[i][j]
                else:
                    s[i][j] = s[i - 1][j] + s[i][j - 1] - s[i - 1][j - 1] + mat[i][j]
        
        res = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                x1 = max(0, i - k)
                y1 = max(0, j - k)
                x2 = min(m - 1, i + k)
                y2 = min(n - 1, j + k)
                if x1 == 0:
                    if y1 == 0:
                        res[i][j] = s[x2][y2]
                    else:
                        res[i][j] = s[x2][y2] - s[x2][y1 - 1]
                elif y1 == 0:
                    res[i][j] = s[x2][y2] - s[x1 - 1][y2]
                else:
                    res[i][j] = s[x2][y2] - s[x1 - 1][y2] - s[x2][y1 - 1] + s[x1 - 1][y1 - 1]
        
        return res
```
