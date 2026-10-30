---
title: "2028. 找出缺失的观测数据"
aliases: ["yiduobo的每日leetcode 2028.找出缺失的观测数据"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/507869288"
zhihu_id: "507869288"
zhihu_title: "yiduobo的每日leetcode 2028.找出缺失的观测数据"
question_id: "2028"
question: "找出缺失的观测数据"
problem_url: "https://leetcode.cn/problems/find-missing-observations/"
difficulty: "Medium"
created: "2022-04-30T21:56:06+08:00"
updated: "2022-04-30T21:56:06+08:00"
upvotes: 1
comments: 0
---

# 2028. 找出缺失的观测数据

> **[yiduobo的每日leetcode 2028.找出缺失的观测数据](https://zhuanlan.zhihu.com/p/507869288) · 知乎 · 2022-04-30 · 赞同 1**
> 力扣：[2028. 找出缺失的观测数据](https://leetcode.cn/problems/find-missing-observations/) · Medium · 灵茶山艾府：[数学+构造（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2028.找出缺失的观测数据

[力扣](https://leetcode-cn.com/problems/find-missing-observations/)

一共m + n个数，平均数为mean，因此原始的总和为(m + n) \* mean，减去当前已有的点数，即sum(rolls)，剩下的就是这缺失的n次投掷得到的数字总和，记为k \= (m + n) \* mean - sum(rolls)。

n次投掷的最小和为n，最大和为n \* 6，那么如果k \< n或者k > 6 \* n，说明无解，否则需要想办法将k分配给这n次投掷。

最简单的一种分配方式自然是平均分配，即先给每个骰子分配k / n，而对于剩下的k % n，则将前k % n个骰子的值再加上1。

最后附上python代码：

```python
class Solution(object):
    def missingRolls(self, rolls, mean, n):
        """
        :type rolls: List[int]
        :type mean: int
        :type n: int
        :rtype: List[int]
        """

        m = len(rolls)
        k = (m + n) * mean - sum(rolls)

        if k < n or k > n * 6:
            return []
        
        res = [k / n] * n
        for index in range(k % n):
            res[index] += 1
        
        return res
```
