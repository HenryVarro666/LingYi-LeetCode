---
title: "306. 累加数"
aliases: ["yiduobo的每日leetcode 306.累加数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/158223636"
zhihu_id: "158223636"
zhihu_title: "yiduobo的每日leetcode 306.累加数"
question_id: "306"
question: "累加数"
problem_url: "https://leetcode.cn/problems/additive-number/"
created: "2020-07-09T22:52:48+08:00"
updated: "2020-07-09T22:52:48+08:00"
upvotes: 0
comments: 0
---

# 306. 累加数

> **[yiduobo的每日leetcode 306.累加数](https://zhuanlan.zhihu.com/p/158223636) · 知乎 · 2020-07-09 · 赞同 0**
> 力扣：[306. 累加数](https://leetcode.cn/problems/additive-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

306.累加数<https://leetcode-cn.com/problems/additive-number/>

目前只想到最暴力的枚举法，即枚举第一个数和第二个数，然后逐个计算后面的数并验证。

需要注意枚举的数最高位如果为0，那么这个数就只能为0。

最后附上python代码：

```python
class Solution(object):
    def isAdditiveNumber(self, num):
        """
        :type num: str
        :rtype: bool
        """

        for i in range(0, len(num) - 2):
            if i > 0 and num[0] == '0':
                break
            first_num = int(num[:i + 1])

            for j in range(i + 1, len(num) - 1):
                if j > i + 1 and num[i + 1] == '0':
                    break
                second_num = int(num[i + 1 : j + 1])
                a = first_num
                b = second_num
                now = j + 1
            
                while True:
                    c = a + b
                    if now + len(str(c)) - 1 >= len(num):
                        break
                    if int(num[now : now + len(str(c))]) != c:
                        break

                    now += len(str(c))
                    if now == len(num):
                        return True
                    a = b
                    b = c
        
        return False
```
