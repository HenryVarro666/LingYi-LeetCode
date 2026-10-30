---
title: "2566. 替换一个数字后的最大差值"
aliases: ["yiduobo的每日leetcode 2566.替换一个数字后的最大差值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/640915220"
zhihu_id: "640915220"
zhihu_title: "yiduobo的每日leetcode 2566.替换一个数字后的最大差值"
question_id: "2566"
question: "替换一个数字后的最大差值"
problem_url: "https://leetcode.cn/problems/maximum-difference-by-remapping-a-digit/"
difficulty: "Easy"
created: "2023-07-02T00:52:58+08:00"
updated: "2023-07-02T00:52:58+08:00"
upvotes: 0
comments: 0
---

# 2566. 替换一个数字后的最大差值

> **[yiduobo的每日leetcode 2566.替换一个数字后的最大差值](https://zhuanlan.zhihu.com/p/640915220) · 知乎 · 2023-07-02 · 赞同 0**
> 力扣：[2566. 替换一个数字后的最大差值](https://leetcode.cn/problems/maximum-difference-by-remapping-a-digit/) · Easy · 灵茶山艾府：[贪心 O(log num) 做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2566.替换一个数字后的最大差值

[力扣](https://leetcode.cn/problems/maximum-difference-by-remapping-a-digit/)

为了使得替换后的数字最大，就应该将最高位上的非9的数字替换成9，而为了使得数字最小，则应该将最高位上的非0的数字替换成0。于是可以从高位到低位遍历两次，找出对应的数字并进行替换，然后计算差值即可。

最后附上python代码：

```python
class Solution(object):
    def minMaxDifference(self, num):
        """
        :type num: int
        :rtype: int
        """

        digits = list(str(num))

        p = 0
        while p < len(digits) and digits[p] == '9':
            p += 1
        
        if p < len(digits):
            target = digits[p]       
            ma = int(str(num).replace(target, '9'))
        else:
            ma = num

        p = 0
        while p < len(digits) and digits[p] == '0':
            p += 1
        
        if p < len(digits):
            target = digits[p]
            mi = int(str(num).replace(target, '0'))
        else:
            mi = num
        
        return ma - mi
```
