---
title: "1295. 统计位数为偶数的数字"
aliases: ["yiduobo的每日leetcode 1295.统计位数为偶数的数字"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/390445554"
zhihu_id: "390445554"
zhihu_title: "yiduobo的每日leetcode 1295.统计位数为偶数的数字"
question_id: "1295"
question: "统计位数为偶数的数字"
problem_url: "https://leetcode.cn/problems/find-numbers-with-even-number-of-digits/"
difficulty: "Easy"
created: "2021-07-16T22:28:25+08:00"
updated: "2021-07-16T22:28:25+08:00"
upvotes: 0
comments: 0
---

# 1295. 统计位数为偶数的数字

> **[yiduobo的每日leetcode 1295.统计位数为偶数的数字](https://zhuanlan.zhihu.com/p/390445554) · 知乎 · 2021-07-16 · 赞同 0**
> 力扣：[1295. 统计位数为偶数的数字](https://leetcode.cn/problems/find-numbers-with-even-number-of-digits/) · Easy · 灵茶山艾府：[O(1) 空间，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1295.统计位数为偶数的数字

[力扣](https://leetcode-cn.com/problems/find-numbers-with-even-number-of-digits/)

由于题目中的数字都小于等于100000，那么偶数位的数字只有两位数、四位数以及100000，一趟循环判断即可。

最后附上python代码：

```python
class Solution(object):
    def findNumbers(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        for num in nums:
            if (num >= 10 and num < 100) or (num >= 1000 and num < 10000) or num == 100000:
                res += 1
        return res
```
