---
title: "3032. 统计各位数字都不同的数字个数II"
aliases: ["yiduobo的每日leetcode 3032.统计各位数字都不同的数字个数II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/695555363"
zhihu_id: "695555363"
zhihu_title: "yiduobo的每日leetcode 3032.统计各位数字都不同的数字个数II"
question_id: "3032"
question: "统计各位数字都不同的数字个数II"
problem_url: "https://leetcode.cn/problems/count-numbers-with-unique-digits-ii/"
created: "2024-05-01T01:51:03+08:00"
updated: "2024-05-01T01:51:03+08:00"
upvotes: 0
comments: 0
---

# 3032. 统计各位数字都不同的数字个数II

> **[yiduobo的每日leetcode 3032.统计各位数字都不同的数字个数II](https://zhuanlan.zhihu.com/p/695555363) · 知乎 · 2024-05-01 · 赞同 0**
> 力扣：[3032. 统计各位数字都不同的数字个数II](https://leetcode.cn/problems/count-numbers-with-unique-digits-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3032.统计各位数字都不同的数字个数II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-numbers-with-unique-digits-ii/description/)

看题设可以使用数位动态规划来处理，不过本题的数据规模非常小，直接暴力枚举就可以了。

另外，本题使用数学方法应该也很方便。在不考虑前导0的情况下，用k个不同数字形成n位数的方案数就是C(k, n) \* n!，因此在这里只需从高位向低位遍历，枚举当前位填充的数字，对于未压线的情况，使用上面的结论计算可行的方案，对于压线的情况，则相当于缩小了问题的规模，只需继续向后使用相同的做法计算就行了。

最后附上python代码：

```python
class Solution(object):
    def numberCount(self, a, b):
        """
        :type a: int
        :type b: int
        :rtype: int
        """

        res = 0
        for x in range(a, b + 1):
            y = x
            vis = set()
            flag = True
            while y:
                v = y % 10
                if v in vis:
                    flag = False
                    break
                vis.add(v)
                y /= 10
            
            if flag:
                res += 1
        
        return res
```
