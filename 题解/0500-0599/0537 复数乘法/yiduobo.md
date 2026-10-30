---
title: "537. 复数乘法"
aliases: ["yiduobo的每日leetcode 537.复数乘法"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261204542"
zhihu_id: "261204542"
zhihu_title: "yiduobo的每日leetcode 537.复数乘法"
question_id: "537"
question: "复数乘法"
problem_url: "https://leetcode.cn/problems/complex-number-multiplication/"
difficulty: "Medium"
created: "2020-10-07T01:27:09+08:00"
updated: "2020-10-07T01:27:09+08:00"
upvotes: 1
comments: 0
---

# 537. 复数乘法

> **[yiduobo的每日leetcode 537.复数乘法](https://zhuanlan.zhihu.com/p/261204542) · 知乎 · 2020-10-07 · 赞同 1**
> 力扣：[537. 复数乘法](https://leetcode.cn/problems/complex-number-multiplication/) · Medium · 灵茶山艾府：[Go 三行解决](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

537.复数乘法<https://leetcode-cn.com/problems/complex-number-multiplication/>

比较基础的题目，题目还很贴心地不需要判断0的情况，直接按定义做就行了。

最后附上python代码：

```python
class Solution(object):
    def complexNumberMultiply(self, a, b):
        """
        :type a: str
        :type b: str
        :rtype: str
        """

        x1, y1 = a.replace('i', '').split('+')
        x2, y2 = b.replace('i', '').split('+')
        x3 = int(x1) * int(x2) - int(y1) * int(y2)
        y3 = int(x1) * int(y2) + int(y1) * int(x2)
        return '%d+%di' % (x3, y3)
```
