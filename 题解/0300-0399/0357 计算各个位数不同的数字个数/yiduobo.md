---
title: "357. 计算各个位数不同的数字个数"
aliases: ["yiduobo的每日leetcode 357.计算各个位数不同的数字个数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/164636818"
zhihu_id: "164636818"
zhihu_title: "yiduobo的每日leetcode 357.计算各个位数不同的数字个数"
question_id: "357"
question: "计算各个位数不同的数字个数"
problem_url: "https://leetcode.cn/problems/count-numbers-with-unique-digits/"
created: "2020-07-27T22:53:41+08:00"
updated: "2020-07-27T22:53:41+08:00"
upvotes: 0
comments: 0
---

# 357. 计算各个位数不同的数字个数

> **[yiduobo的每日leetcode 357.计算各个位数不同的数字个数](https://zhuanlan.zhihu.com/p/164636818) · 知乎 · 2020-07-27 · 赞同 0**
> 力扣：[357. 计算各个位数不同的数字个数](https://leetcode.cn/problems/count-numbers-with-unique-digits/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

357.计算各个位数不同的数字个数<https://leetcode-cn.com/problems/count-numbers-with-unique-digits/>

组合数学的题目。首先考察一位数的情况，可以取0到9，因此有10种可能。

接下来考察两位数的情况。首先，十位上不能为0，因此有1到9一共9种选择，之后的个位数上不能与十位数相同，因此也有9种选择，因此最后有9 \* 9 \= 81种选择。

对于之后的k位数，也都是因为最高位不能为0，只有9中选择，其他位上的选择则是逐位减1，即3位数一共有9 \* 9 \* 8种组合，4位数则是9 \* 9 \* 8 \* 7种组合，以此类推。

于是一趟循环，逐位计算可能的情况数然后累加起来即可。

最后附上python代码：

```python
class Solution(object):
    def countNumbersWithUniqueDigits(self, n):
        """
        :type n: int
        :rtype: int
        """

        now = 9
        res = 1
        for index in range(n):
            res += now
            now *= (9 - index)

        return res
```
