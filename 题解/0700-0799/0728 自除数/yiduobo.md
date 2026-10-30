---
title: "728. 自除数"
aliases: ["yiduobo的每日leetcode 728.自除数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/335335641"
zhihu_id: "335335641"
zhihu_title: "yiduobo的每日leetcode 728.自除数"
question_id: "728"
question: "自除数"
problem_url: "https://leetcode.cn/problems/self-dividing-numbers/"
created: "2020-12-09T22:22:02+08:00"
updated: "2020-12-09T22:22:02+08:00"
upvotes: 0
comments: 0
---

# 728. 自除数

> **[yiduobo的每日leetcode 728.自除数](https://zhuanlan.zhihu.com/p/335335641) · 知乎 · 2020-12-09 · 赞同 0**
> 力扣：[728. 自除数](https://leetcode.cn/problems/self-dividing-numbers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

728.自除数

[力扣](https://leetcode-cn.com/problems/self-dividing-numbers/)

由于题目给出的上界最多也只到10000，那么可以直接从left枚举到right，对于当前处理的数num，通过模10分离出每一位x，然后判断x是否非0且num模x是否为0。

最后附上python代码：

```python
class Solution(object):
    def selfDividingNumbers(self, left, right):
        """
        :type left: int
        :type right: int
        :rtype: List[int]
        """

        res = []
        for num in range(left, right + 1):
            tmp = num
            flag = True
            while tmp:
                x = tmp % 10
                tmp /= 10
                if x == 0 or num % x != 0:
                    flag = False
                    break
            if flag:
                res.append(num)

        return res
```
