---
title: "867. 转置矩阵"
aliases: ["yiduobo的每日leetcode 867.转置矩阵"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/matrix"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/349924512"
zhihu_id: "349924512"
zhihu_title: "yiduobo的每日leetcode 867.转置矩阵"
question_id: "867"
question: "转置矩阵"
problem_url: "https://leetcode.cn/problems/transpose-matrix/"
difficulty: "Easy"
created: "2021-02-10T20:50:02+08:00"
updated: "2021-02-10T20:50:02+08:00"
upvotes: 0
comments: 0
---

# 867. 转置矩阵

> **[yiduobo的每日leetcode 867.转置矩阵](https://zhuanlan.zhihu.com/p/349924512) · 知乎 · 2021-02-10 · 赞同 0**
> 力扣：[867. 转置矩阵](https://leetcode.cn/problems/transpose-matrix/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

867.转置矩阵

[力扣](https://leetcode-cn.com/problems/transpose-matrix/)

根据转置矩阵的定义，我们只需先列后行遍历整个矩阵，然后依次将遍历到的数按先行后列的顺序加入到答案矩阵中即可。

最后附上python代码：

```python
class Solution(object):
    def transpose(self, A):
        """
        :type A: List[List[int]]
        :rtype: List[List[int]]
        """

        res = []

        m = len(A)
        n = len(A[0])
        for j in range(n):
            res.append([])
            for i in range(m):
                res[-1].append(A[i][j])
        
        return res
```
