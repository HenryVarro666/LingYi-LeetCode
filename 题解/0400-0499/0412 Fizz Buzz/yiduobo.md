---
title: "412. Fizz Buzz"
aliases: ["yiduobo的每日leetcode 412.Fizz Buzz"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/187594878"
zhihu_id: "187594878"
zhihu_title: "yiduobo的每日leetcode 412.Fizz Buzz"
question_id: "412"
question: "Fizz Buzz"
problem_url: "https://leetcode.cn/problems/fizz-buzz/"
difficulty: "Easy"
created: "2020-08-17T23:31:12+08:00"
updated: "2020-08-17T23:31:12+08:00"
upvotes: 0
comments: 0
---

# 412. Fizz Buzz

> **[yiduobo的每日leetcode 412.Fizz Buzz](https://zhuanlan.zhihu.com/p/187594878) · 知乎 · 2020-08-17 · 赞同 0**
> 力扣：[412. Fizz Buzz](https://leetcode.cn/problems/fizz-buzz/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

412.Fizz Buzz <https://leetcode-cn.com/problems/fizz-buzz/>

比较基础的题目，直接枚举每个数然后判断其模3以及模5的余数即可。

最后附上python代码：

```python
class Solution(object):
    def fizzBuzz(self, n):
        """
        :type n: int
        :rtype: List[str]
        """

        res = []
        for index in range(1, n + 1):
            if index % 3 == 0:
                if index % 5 == 0:
                    res.append('FizzBuzz')
                else:
                    res.append('Fizz')
            elif index % 5 == 0:
                res.append('Buzz')
            else:
                res.append(str(index))

        return res
```
