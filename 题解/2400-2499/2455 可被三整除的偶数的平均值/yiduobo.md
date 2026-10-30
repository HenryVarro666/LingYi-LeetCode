---
title: "2455. 可被三整除的偶数的平均值"
aliases: ["yiduobo的每日leetcode 2455.可被三整除的偶数的平均值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/number-theory"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/585845745"
zhihu_id: "585845745"
zhihu_title: "yiduobo的每日leetcode 2455.可被三整除的偶数的平均值"
question_id: "2455"
question: "可被三整除的偶数的平均值"
problem_url: "https://leetcode.cn/problems/average-value-of-even-numbers-that-are-divisible-by-three/"
difficulty: "Easy"
created: "2022-11-22T23:26:58+08:00"
updated: "2022-11-22T23:27:00+08:00"
upvotes: 0
comments: 0
---

# 2455. 可被三整除的偶数的平均值

> **[yiduobo的每日leetcode 2455.可被三整除的偶数的平均值](https://zhuanlan.zhihu.com/p/585845745) · 知乎 · 2022-11-22 · 赞同 0**
> 力扣：[2455. 可被三整除的偶数的平均值](https://leetcode.cn/problems/average-value-of-even-numbers-that-are-divisible-by-three/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2455.可被三整除的偶数的平均值

[力扣](https://leetcode.cn/problems/average-value-of-even-numbers-that-are-divisible-by-three/)

可以被三整除的偶数，也就是可以被6整除的数。那么只需一趟遍历，找出所有能被6整除的数并求出这些数的平均值即可。

最后附上python代码：

```python
class Solution(object):
    def averageValue(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        s = 0
        cnt = 0
        for num in nums:
            if num % 6 == 0:
                s += num
                cnt += 1
        
        if cnt == 0:
            return 0
        else:
            return s / cnt
```
