---
title: "566. 重塑矩阵"
aliases: ["yiduobo的每日leetcode 566.重塑矩阵"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/266489171"
zhihu_id: "266489171"
zhihu_title: "yiduobo的每日leetcode 566.重塑矩阵"
question_id: "566"
question: "重塑矩阵"
problem_url: "https://leetcode.cn/problems/reshape-the-matrix/"
created: "2020-10-17T21:59:33+08:00"
updated: "2020-10-17T21:59:33+08:00"
upvotes: 0
comments: 0
---

# 566. 重塑矩阵

> **[yiduobo的每日leetcode 566.重塑矩阵](https://zhuanlan.zhihu.com/p/266489171) · 知乎 · 2020-10-17 · 赞同 0**
> 力扣：[566. 重塑矩阵](https://leetcode.cn/problems/reshape-the-matrix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

566.重塑矩阵<https://leetcode-cn.com/problems/reshape-the-matrix/>

比较基础的题目，首先判断m \* n是否等于r \* c，若不等于那么就无法reshape，直接返回原矩阵即可。若可以变换，那么逐行逐列遍历原矩阵中的数字，将其加入到答案矩阵中，当答案矩阵中当前行的数字达到c个时就另起一行。

最后附上python代码：

```python
class Solution(object):
    def matrixReshape(self, nums, r, c):
        """
        :type nums: List[List[int]]
        :type r: int
        :type c: int
        :rtype: List[List[int]]
        """

        m = len(nums)
        n = len(nums[0])
        if m * n != r * c:
            return nums

        res = []
        cnt = 0
        for i in range(m):
            for j in range(n):
                if cnt == 0:
                    res.append([])
                    cnt = 0
                res[-1].append(nums[i][j])
                cnt += 1
                if cnt == c:
                    cnt = 0

        return res
```
