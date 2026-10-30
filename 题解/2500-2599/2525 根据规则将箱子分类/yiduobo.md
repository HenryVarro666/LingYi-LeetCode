---
title: "2525. 根据规则将箱子分类"
aliases: ["yiduobo的每日leetcode 2525.根据规则将箱子分类"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/636325786"
zhihu_id: "636325786"
zhihu_title: "yiduobo的每日leetcode 2525.根据规则将箱子分类"
question_id: "2525"
question: "根据规则将箱子分类"
problem_url: "https://leetcode.cn/problems/categorize-box-according-to-criteria/"
difficulty: "Easy"
rating: 1301
created: "2023-06-11T21:56:30+08:00"
updated: "2023-06-11T21:56:30+08:00"
upvotes: 1
comments: 0
---

# 2525. 根据规则将箱子分类

> **[yiduobo的每日leetcode 2525.根据规则将箱子分类](https://zhuanlan.zhihu.com/p/636325786) · 知乎 · 2023-06-11 · 赞同 1**
> 力扣：[2525. 根据规则将箱子分类](https://leetcode.cn/problems/categorize-box-according-to-criteria/) · Easy · 灵茶山艾府：[分类讨论（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2525.根据规则将箱子分类

[力扣](https://leetcode.cn/problems/categorize-box-according-to-criteria/)

按照题目描述分别判断箱子是否为bulky和heavy，然后返回最终结果即可。

最后附上python代码：

```python
class Solution(object):
    def categorizeBox(self, length, width, height, mass):
        """
        :type length: int
        :type width: int
        :type height: int
        :type mass: int
        :rtype: str
        """

        bulky = (max(length, width, height) >= 10000) or (length * width * height >= (10 ** 9))
        heavy = (mass >= 100)

        if bulky:
            if heavy:
                return "Both"
            else:
                return "Bulky"
        elif heavy:
            return "Heavy"
        else:
            return "Neither"
```
