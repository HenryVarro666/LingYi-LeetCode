---
title: "1189. “气球”的最大数量"
aliases: ["yiduobo的每日leetcode 1189.“气球”的最大数量"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/380588219"
zhihu_id: "380588219"
zhihu_title: "yiduobo的每日leetcode 1189.“气球”的最大数量"
question_id: "1189"
question: "“气球” 的最大数量"
problem_url: "https://leetcode.cn/problems/maximum-number-of-balloons/"
difficulty: "Easy"
created: "2021-06-14T19:33:14+08:00"
updated: "2021-06-14T19:33:14+08:00"
upvotes: 0
comments: 0
---

# 1189. “气球”的最大数量

> **[yiduobo的每日leetcode 1189.“气球”的最大数量](https://zhuanlan.zhihu.com/p/380588219) · 知乎 · 2021-06-14 · 赞同 0**
> 力扣：[1189. “气球” 的最大数量](https://leetcode.cn/problems/maximum-number-of-balloons/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1189.“气球”的最大数量

[力扣](https://leetcode-cn.com/problems/maximum-number-of-balloons/)

一个气球要求使用一个b，一个a，两个l，两个o以及一个n，那么可以统计各个字母出现的次数，并计算该字母最多可以供几个气球使用，然后取其中的最小值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxNumberOfBalloons(self, text):
        """
        :type text: str
        :rtype: int
        """

        char_dict = {}
        for char in text:
            char_dict[char] = char_dict.get(char, 0) + 1
        
        res = char_dict.get('b', 0)
        res = min(res, char_dict.get('a', 0))
        res = min(res, char_dict.get('l', 0) / 2)
        res = min(res, char_dict.get('o', 0) / 2)
        res = min(res, char_dict.get('n', 0))

        return res
```
