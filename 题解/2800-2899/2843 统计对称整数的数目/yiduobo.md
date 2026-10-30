---
title: "2843. 统计对称整数的数目"
aliases: ["yiduobo的每日leetcode 2843.统计对称整数的数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/enumeration", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/660002567"
zhihu_id: "660002567"
zhihu_title: "yiduobo的每日leetcode 2843.统计对称整数的数目"
question_id: "2843"
question: "统计对称整数的数目"
problem_url: "https://leetcode.cn/problems/count-symmetric-integers/"
difficulty: "Easy"
created: "2023-10-08T03:01:29+08:00"
updated: "2023-10-08T03:01:29+08:00"
upvotes: 0
comments: 0
---

# 2843. 统计对称整数的数目

> **[yiduobo的每日leetcode 2843.统计对称整数的数目](https://zhuanlan.zhihu.com/p/660002567) · 知乎 · 2023-10-08 · 赞同 0**
> 力扣：[2843. 统计对称整数的数目](https://leetcode.cn/problems/count-symmetric-integers/) · Easy · 灵茶山艾府：[两种方法：枚举 / 数位 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2843.统计对称整数的数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-symmetric-integers/)

看题面应该可以使用数位动态规划求解，不过本题的数据规模非常小，完全可以直接枚举low到high之间的所有整数，将数位分离出来之后检测前半段之和是否等于后半段之和。

最后附上python代码：

```python
class Solution(object):
    def countSymmetricIntegers(self, low, high):
        """
        :type low: int
        :type high: int
        :rtype: int
        """

        res = 0
        for x in range(low, high + 1):
            str_x = str(x)
            if len(str_x) % 2 == 0:
                left = 0
                right = len(str_x) - 1
                s = 0
                while left < right:
                    s += int(str_x[left]) - int(str_x[right])
                    left += 1
                    right -= 1
                
                if s == 0:
                    res += 1
        
        return res
```
