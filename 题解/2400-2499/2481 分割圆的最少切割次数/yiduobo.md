---
title: "2481. 分割圆的最少切割次数"
aliases: ["yiduobo的每日leetcode 2481.分割圆的最少切割次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/geometry"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/589004928"
zhihu_id: "589004928"
zhihu_title: "yiduobo的每日leetcode 2481.分割圆的最少切割次数"
question_id: "2481"
question: "分割圆的最少切割次数"
problem_url: "https://leetcode.cn/problems/minimum-cuts-to-divide-a-circle/"
difficulty: "Easy"
created: "2022-12-04T04:04:58+08:00"
updated: "2022-12-04T04:04:58+08:00"
upvotes: 0
comments: 0
---

# 2481. 分割圆的最少切割次数

> **[yiduobo的每日leetcode 2481.分割圆的最少切割次数](https://zhuanlan.zhihu.com/p/589004928) · 知乎 · 2022-12-04 · 赞同 0**
> 力扣：[2481. 分割圆的最少切割次数](https://leetcode.cn/problems/minimum-cuts-to-divide-a-circle/) · Easy · 灵茶山艾府：[根据对称性作答](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2481.分割圆的最少切割次数

[力扣](https://leetcode.cn/problems/minimum-cuts-to-divide-a-circle/)

观察题目给出的样例可以找出规律，当n为奇数时，必须使用半径来进行切割，否则就可以使用直径来进行切分，因此当n为奇数时，答案为n，否则为n / 2。

另外需要特别注意的是，当n \= 1时，不需要进行任何分割，此时的答案应该为0。

最后附上python代码：

```python
class Solution(object):
    def numberOfCuts(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n == 1:
            return 0
        elif n & 1:
            return n
        else:
            return n >> 1
```
