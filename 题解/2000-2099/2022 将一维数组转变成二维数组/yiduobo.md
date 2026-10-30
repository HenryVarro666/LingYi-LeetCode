---
title: "2022. 将一维数组变成二维数组"
aliases: ["yiduobo的每日leetcode 2022.将一维数组变成二维数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/506962646"
zhihu_id: "506962646"
zhihu_title: "yiduobo的每日leetcode 2022.将一维数组变成二维数组"
question_id: "2022"
question: "将一维数组转变成二维数组"
problem_url: "https://leetcode.cn/problems/convert-1d-array-into-2d-array/"
difficulty: "Easy"
created: "2022-04-29T02:09:27+08:00"
updated: "2022-04-29T02:09:27+08:00"
upvotes: 0
comments: 0
---

# 2022. 将一维数组变成二维数组

> **[yiduobo的每日leetcode 2022.将一维数组变成二维数组](https://zhuanlan.zhihu.com/p/506962646) · 知乎 · 2022-04-29 · 赞同 0**
> 力扣：[2022. 将一维数组转变成二维数组](https://leetcode.cn/problems/convert-1d-array-into-2d-array/) · Easy · 灵茶山艾府：[Go 模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2022.将一维数组变成二维数组

[力扣](https://leetcode-cn.com/problems/convert-1d-array-into-2d-array/)

比较基础的题目，python也有内置的转换函数，我在这里还是手动实现了一下。

首先判断original的长度是否等于m \* n，若不等于，说明无法转换，直接返回空。

若original的长度等于m \* n，则开始进行转换。使用一个行计数器p计算当前行已经填充了多少个数，p的初始值为0。接下来对original一趟遍历，每次将当前的数字加入到答案矩阵中最后一行的末尾，并更新计数器p。当p等于n时，则在答案矩阵中另起一行，并将p置为0。

最后附上python代码：

```python
class Solution(object):
    def construct2DArray(self, original, m, n):
        """
        :type original: List[int]
        :type m: int
        :type n: int
        :rtype: List[List[int]]
        """

        res = []
        if len(original) != m * n:
            return res

        p = 0
        for num in original:
            if p == 0:
                res.append([])
            res[-1].append(num)
            p += 1
            if p == n:
                p = 0
        
        return res
```
