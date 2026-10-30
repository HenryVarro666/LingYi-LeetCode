---
title: "258. 各位相加"
aliases: ["yiduobo的每日leetcode 258.各位相加"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/number-theory"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/150994739"
zhihu_id: "150994739"
zhihu_title: "yiduobo的每日leetcode 258.各位相加"
question_id: "258"
question: "各位相加"
problem_url: "https://leetcode.cn/problems/add-digits/"
difficulty: "Easy"
created: "2020-06-27T16:06:51+08:00"
updated: "2020-06-27T16:06:51+08:00"
upvotes: 0
comments: 0
---

# 258. 各位相加

> **[yiduobo的每日leetcode 258.各位相加](https://zhuanlan.zhihu.com/p/150994739) · 知乎 · 2020-06-27 · 赞同 0**
> 力扣：[258. 各位相加](https://leetcode.cn/problems/add-digits/) · Easy · 灵茶山艾府：[O(1) 做法：解释清楚为什么要模 9！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

258.各位相加<https://leetcode-cn.com/problems/add-digits/>

数学题。设最初的num为num0，那么热对于num0，设其长度为L0，其可以写成：

10^(L0 - 1) \* a[L0 - 1] + 10^(L0 - 2) \* a[L0 - 2] + ... + 10^1 \* a[1] + a[0]

那么第一轮迭代后

num1 \= a[L0 - 1] + a[L0 - 2] + ... + a[1] + a[0] \= num0 - 9 \* m1

设num1的长度为L1，那么其可以写成：

10^(L1 - 1) \* b[L1 - 1] + 10^(L1 - 2) \* b[L1 - 2] + ... + 10^1 \* b[1] + b[0]

那么第二轮迭代后

num2 \= b[L1 - 1] + b[L1 - 2] + ... + b[1] + b[0] \= num1 - 9 \* m2

继续迭代直到numk在0到9之间，此时numk就是最终的答案，那么

numk \= num0 - 9 \* m1 - 9 \* m2 - ... - 9 \* mk \= num0 - 9 \* n

于是就可以直接对num0模9，余数就是numk了。需要注意num0模9等于0时，若num0等于0，那么numk也等于0，否则numk就应该等于9。

最后附上python代码：

```python
class Solution(object):
    def addDigits(self, num):
        """
        :type num: int
        :rtype: int
        """

        if num == 0:
            return num
        
        num %= 9
        if num == 0:
            num = 9
        return num
```
