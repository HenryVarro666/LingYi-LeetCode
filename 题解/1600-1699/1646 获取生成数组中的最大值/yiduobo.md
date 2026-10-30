---
title: "1646. 获取生成数组中的最大值"
aliases: ["yiduobo的每日leetcode 1646.获取生成数组中的最大值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/439724392"
zhihu_id: "439724392"
zhihu_title: "yiduobo的每日leetcode 1646.获取生成数组中的最大值"
question_id: "1646"
question: "获取生成数组中的最大值"
problem_url: "https://leetcode.cn/problems/get-maximum-in-generated-array/"
created: "2021-11-30T23:43:02+08:00"
updated: "2021-11-30T23:43:02+08:00"
upvotes: 0
comments: 0
---

# 1646. 获取生成数组中的最大值

> **[yiduobo的每日leetcode 1646.获取生成数组中的最大值](https://zhuanlan.zhihu.com/p/439724392) · 知乎 · 2021-11-30 · 赞同 0**
> 力扣：[1646. 获取生成数组中的最大值](https://leetcode.cn/problems/get-maximum-in-generated-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1646.获取生成数组中的最大值

[力扣](https://leetcode-cn.com/problems/get-maximum-in-generated-array/)

感觉应该有数学方法可以直接计算，但是没有想出来，只好老老实实逐个模拟计算。

初始化f为[0, 1]，接下从2到n枚举，对于当前枚举到的index，首先初始化f[index]为f[index / 2]，接下来若index为奇数，则还需要将f[index / 2 + 1]累加到f[index]上。在得到每个f[index]后记得顺便更新答案。

最后附上python代码：

```python
class Solution(object):
    def getMaximumGenerated(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n == 0:
            return 0
        
        res = 1
        f = [0, 1]
        for index in range(2, n + 1):
            f.append(f[index / 2])
            if index & 1:
                f[-1] += f[index / 2 + 1]
            res = max(res, f[-1])

        return res
```
