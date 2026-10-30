---
title: "3899. 三角形的内角度数"
aliases: ["yiduobo的每日leetcode 3899.三角形的内角度数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/geometry", "leetcode/math", "题单/数学算法", "题单/数学算法/五-计算几何"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2028243628615636826"
zhihu_id: "2028243628615636826"
zhihu_title: "yiduobo的每日leetcode 3899.三角形的内角度数"
question_id: "3899"
question: "三角形的内角度数"
problem_url: "https://leetcode.cn/problems/angles-of-a-triangle/"
difficulty: "Medium"
rating: 1407
created: "2026-04-16T22:53:12+08:00"
updated: "2026-04-16T22:53:13+08:00"
upvotes: 1
comments: 0
---

# 3899. 三角形的内角度数

> **[yiduobo的每日leetcode 3899.三角形的内角度数](https://zhuanlan.zhihu.com/p/2028243628615636826) · 知乎 · 2026-04-16 · 赞同 1**
> 力扣：[3899. 三角形的内角度数](https://leetcode.cn/problems/angles-of-a-triangle/) · Medium · 灵茶山艾府：[余弦定理（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3899.三角形的内角度数

<https://leetcode.cn/problems/angles-of-a-triangle/description/>

题目给出一个长度为3的正整数数组sides。

判断能否由sides中的三个元素作为边长，构成一个面积为正的三角形。若可以，返回一个包含3个浮点数的数组，表示该三角形的三个内角(单位为度)，并按非递减顺序排序。若不行，则返回空数组。

题目要求先判断能否形成三角形，可以直接通过两边之和是否大于第三边来进行判断。若可以，则可以利用余弦定理，计算出每个角的cos值，然后计算acos，再转化为角度即可。

最后附上python代码：

```python
class Solution(object):
    def internalAngles(self, sides):
        """
        :type sides: List[int]
        :rtype: List[float]
        """
        
        a, b, c = sides
        if a + b <= c or a + c <= b or b + c <= a:
            return []
        
        cosA = (b ** 2 + c ** 2 - a ** 2) / 2.0 / b / c
        cosB = (a ** 2 + c ** 2 - b ** 2) / 2.0 / a / c
        cosC = (a ** 2 + b ** 2 - c ** 2) / 2.0 / a / b
        return sorted([acos(cosA) / pi * 180, acos(cosB) / pi * 180, acos(cosC) / pi * 180])
```
