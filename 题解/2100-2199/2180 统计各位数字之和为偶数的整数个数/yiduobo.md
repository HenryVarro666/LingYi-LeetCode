---
title: "2180. 统计各位数字之和为偶数的整数个数"
aliases: ["yiduobo的每日leetcode 2180.统计各位数字之和为偶数的整数个数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/535605739"
zhihu_id: "535605739"
zhihu_title: "yiduobo的每日leetcode 2180.统计各位数字之和为偶数的整数个数"
question_id: "2180"
question: "统计各位数字之和为偶数的整数个数"
problem_url: "https://leetcode.cn/problems/count-integers-with-even-digit-sum/"
difficulty: "Easy"
created: "2022-06-29T23:37:33+08:00"
updated: "2022-06-29T23:37:33+08:00"
upvotes: 0
comments: 0
---

# 2180. 统计各位数字之和为偶数的整数个数

> **[yiduobo的每日leetcode 2180.统计各位数字之和为偶数的整数个数](https://zhuanlan.zhihu.com/p/535605739) · 知乎 · 2022-06-29 · 赞同 0**
> 力扣：[2180. 统计各位数字之和为偶数的整数个数](https://leetcode.cn/problems/count-integers-with-even-digit-sum/) · Easy · 灵茶山艾府：[模拟 + 位运算](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2180.统计各位数字之和为偶数的整数个数

[力扣](https://leetcode.cn/problems/count-integers-with-even-digit-sum/)

本题最好的做法应该是基于数位的动态规划，不过由于本题的数据规模很小，所以我直接采用的暴力法，枚举2到num之间的所有数，然后将每个数字分离出来后求和再判断是否为偶数。

最后附上python代码：

```python
class Solution(object):
    def countEven(self, num):
        """
        :type num: int
        :rtype: int
        """

        res = 0
        for index in range(2, num + 1):
            tmp = index
            now = 0
            while tmp:
                now += tmp % 10
                tmp /= 10
            
            if now % 2 == 0:
                res += 1
        
        return res
```
