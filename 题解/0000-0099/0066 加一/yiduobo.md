---
title: "66. 加一"
aliases: ["yiduobo的每日leetcode 66.加一"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "题单/面试经典-150-题", "题单/面试经典-150-题/数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/130819200"
zhihu_id: "130819200"
zhihu_title: "yiduobo的每日leetcode 66.加一"
question_id: "66"
question: "加一"
problem_url: "https://leetcode.cn/problems/plus-one/"
difficulty: "Easy"
created: "2020-04-15T13:46:26+08:00"
updated: "2020-04-15T13:46:26+08:00"
upvotes: 0
comments: 0
---

# 66. 加一

> **[yiduobo的每日leetcode 66.加一](https://zhuanlan.zhihu.com/p/130819200) · 知乎 · 2020-04-15 · 赞同 0**
> 力扣：[66. 加一](https://leetcode.cn/problems/plus-one/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

昨天因为有点事情出门了，没来得及写，今天补上。

66.加一<https://leetcode-cn.com/problems/plus-one/>

比较基础的题目。注意到加法中的进位每次最多进1，于是可以从低位到高位扫描，如果当前位上是9，那么将当前位置0，并继续看下一位。如果当前位上不是9，那么当前位加上1返回结果即可。

需要注意全都是9的情况，此时答案应该是1000...000，即需要在list的最高位加入1：

最后附上python代码：

```python
class Solution(object):
    def plusOne(self, digits):
        """
        :type digits: List[int]
        :rtype: List[int]
        """

        pos = len(digits) - 1
        while pos > -1 and digits[pos] == 9:
            digits[pos] = 0
            pos -= 1

        if pos == -1:
            digits[0] = 1
            digits.append(0)
        else:
            digits[pos] += 1
            
        return digits
```
