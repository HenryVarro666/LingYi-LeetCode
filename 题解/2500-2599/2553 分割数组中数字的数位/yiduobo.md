---
title: "2553. 分割数组中数字的数位"
aliases: ["yiduobo的每日leetcode 2553.分割数组中数字的数位"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/638957774"
zhihu_id: "638957774"
zhihu_title: "yiduobo的每日leetcode 2553.分割数组中数字的数位"
question_id: "2553"
question: "分割数组中数字的数位"
problem_url: "https://leetcode.cn/problems/separate-the-digits-in-an-array/"
difficulty: "Easy"
created: "2023-06-25T22:51:17+08:00"
updated: "2023-06-25T22:51:17+08:00"
upvotes: 1
comments: 0
---

# 2553. 分割数组中数字的数位

> **[yiduobo的每日leetcode 2553.分割数组中数字的数位](https://zhuanlan.zhihu.com/p/638957774) · 知乎 · 2023-06-25 · 赞同 1**
> 力扣：[2553. 分割数组中数字的数位](https://leetcode.cn/problems/separate-the-digits-in-an-array/) · Easy · 灵茶山艾府：[两种方法：用字符串 / 不用字符串（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2553.分割数组中数字的数位

[力扣](https://leetcode.cn/problems/separate-the-digits-in-an-array/)

直接按照模10除以10的方法将每个数字都逐位分离即可。

另外注意到单个数字分离出的结果是倒序的，为了方便处理，在这里可以从后往前遍历这些数字并进行逐位分离，这样一来就只需最后进行一次总的翻转操作就行了。

最后附上python代码：

```python
class Solution(object):
    def separateDigits(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        res = []
        for x in nums[::-1]:
            while x:
                res.append(x % 10)
                x /= 10
        
        res.reverse()
        return res
```
