---
title: "1243. 数组变换"
aliases: ["yiduobo的每日leetcode 1243.数组变换"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/614317518"
zhihu_id: "614317518"
zhihu_title: "yiduobo的每日leetcode 1243.数组变换"
question_id: "1243"
question: "数组变换"
problem_url: "https://leetcode.cn/problems/array-transformation/"
created: "2023-03-15T22:14:01+08:00"
updated: "2023-03-15T22:14:01+08:00"
upvotes: 0
comments: 0
---

# 1243. 数组变换

> **[yiduobo的每日leetcode 1243.数组变换](https://zhuanlan.zhihu.com/p/614317518) · 知乎 · 2023-03-15 · 赞同 0**
> 力扣：[1243. 数组变换](https://leetcode.cn/problems/array-transformation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1243.数组变换

[力扣](https://leetcode.cn/problems/array-transformation/)

感觉应该可以通过数学和单调性分析直接得到最终答案，但是没有什么好的思路，不过好在本题的数据规模较小，因此可以直接按照题目的规则进行模拟。

最后附上python代码：

```python
class Solution(object):
    def transformArray(self, arr):
        """
        :type arr: List[int]
        :rtype: List[int]
        """

        f = arr[:]
        n = len(f)
        change = True
        while change:
            change = False
            g = f[:]
            f = []

            for index in range(n):
                if index == 0 or index == n - 1:
                    f.append(g[index])
                elif g[index] > g[index - 1] and g[index] > g[index + 1]:
                    f.append(g[index] - 1)
                    change = True
                elif g[index] < g[index - 1] and g[index] < g[index + 1]:
                    f.append(g[index] + 1)
                    change = True
                else:
                    f.append(g[index])
        
        return f
```
