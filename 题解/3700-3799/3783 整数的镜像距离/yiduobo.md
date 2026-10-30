---
title: "3783. 整数的镜像距离"
aliases: ["yiduobo的每日leetcode 3783.整数的镜像距离"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1986985153004856559"
zhihu_id: "1986985153004856559"
zhihu_title: "yiduobo的每日leetcode 3783.整数的镜像距离"
question_id: "3783"
question: "整数的镜像距离"
problem_url: "https://leetcode.cn/problems/mirror-distance-of-an-integer/"
difficulty: "Easy"
created: "2025-12-24T02:26:27+08:00"
updated: "2025-12-24T02:26:27+08:00"
upvotes: 1
comments: 0
---

# 3783. 整数的镜像距离

> **[yiduobo的每日leetcode 3783.整数的镜像距离](https://zhuanlan.zhihu.com/p/1986985153004856559) · 知乎 · 2025-12-24 · 赞同 1**
> 力扣：[3783. 整数的镜像距离](https://leetcode.cn/problems/mirror-distance-of-an-integer/) · Easy · 灵茶山艾府：[反转数字（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3783.整数的镜像距离

[3783. 整数的镜像距离 - 力扣（LeetCode）](https://leetcode.cn/problems/mirror-distance-of-an-integer/description/)

题目给出一个整数n，定义它的镜像距离为n与reverse(n)之差的绝对值。其中reverse(n)表示将n的数字反转后形成的整数。

问n的镜像距离是多少。

题目要计算n反转后的整数，那么在这里就可以按模10除以10的方法先将n的数位分离出来，得到数组digits。然后直接正序遍历digits，使用乘以10再加上当前位上元素的方法就能构造出n反转后的整数，计算其与n之差的绝对值即可。

最后附上python代码：

```python
class Solution(object):
    def mirrorDistance(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        m = n
        digits = []
        while m:
            digits.append(m % 10)
            m //= 10
        
        m = 0
        for d in digits:
            m = m * 10 + d
        return abs(n - m)
```
