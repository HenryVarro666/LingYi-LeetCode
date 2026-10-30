---
title: "2413. 最小偶倍数"
aliases: ["yiduobo的每日leetcode 2413.最小偶倍数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/math", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/568841305"
zhihu_id: "568841305"
zhihu_title: "yiduobo的每日leetcode 2413.最小偶倍数"
question_id: "2413"
question: "最小偶倍数"
problem_url: "https://leetcode.cn/problems/smallest-even-multiple/"
difficulty: "Easy"
rating: 1145
created: "2022-09-28T02:29:17+08:00"
updated: "2022-09-28T11:04:36+08:00"
upvotes: 0
comments: 0
---

# 2413. 最小偶倍数

> **[yiduobo的每日leetcode 2413.最小偶倍数](https://zhuanlan.zhihu.com/p/568841305) · 知乎 · 2022-09-28 · 赞同 0**
> 力扣：[2413. 最小偶倍数](https://leetcode.cn/problems/smallest-even-multiple/) · Easy · 灵茶山艾府：[一行代码搞定！两种写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2413.最小偶倍数

[力扣](https://leetcode.cn/problems/smallest-even-multiple/)

比较基础的题目。当n为奇数时，答案就是n \* 2，否则就是n自己。

最后附上python代码：

```python
class Solution(object):
    def smallestEvenMultiple(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n % 2 == 0:
            return n
        else:
            return n * 2
```
