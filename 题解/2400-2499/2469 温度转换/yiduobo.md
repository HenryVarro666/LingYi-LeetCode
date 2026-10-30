---
title: "2469. 温度转换"
aliases: ["yiduobo的每日leetcode 2469.温度转换"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/587560063"
zhihu_id: "587560063"
zhihu_title: "yiduobo的每日leetcode 2469.温度转换"
question_id: "2469"
question: "温度转换"
problem_url: "https://leetcode.cn/problems/convert-the-temperature/"
difficulty: "Easy"
created: "2022-11-29T00:00:22+08:00"
updated: "2022-11-29T00:00:22+08:00"
upvotes: 0
comments: 0
---

# 2469. 温度转换

> **[yiduobo的每日leetcode 2469.温度转换](https://zhuanlan.zhihu.com/p/587560063) · 知乎 · 2022-11-29 · 赞同 0**
> 力扣：[2469. 温度转换](https://leetcode.cn/problems/convert-the-temperature/) · Easy · 灵茶山艾府：[根据公式计算（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2469.温度转换

<https://leetcode.cn/problems/convert-the-temperature/>

比较基础的题目，根据题目给出的转换公式计算答案即可。

最后附上python代码：

```python
class Solution(object):
    def convertTemperature(self, celsius):
        """
        :type celsius: float
        :rtype: List[float]
        """

        return [celsius + 273.15, celsius * 1.8 + 32]
```
