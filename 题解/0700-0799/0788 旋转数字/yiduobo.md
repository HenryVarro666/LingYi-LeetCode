---
title: "788. 旋转数字"
aliases: ["yiduobo的每日leetcode 788.旋转数字"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/341224785"
zhihu_id: "341224785"
zhihu_title: "yiduobo的每日leetcode 788.旋转数字"
question_id: "788"
question: "旋转数字"
problem_url: "https://leetcode.cn/problems/rotated-digits/"
difficulty: "Medium"
created: "2021-01-01T14:31:20+08:00"
updated: "2021-01-01T14:31:20+08:00"
upvotes: 0
comments: 0
---

# 788. 旋转数字

> **[yiduobo的每日leetcode 788.旋转数字](https://zhuanlan.zhihu.com/p/341224785) · 知乎 · 2021-01-01 · 赞同 0**
> 力扣：[788. 旋转数字](https://leetcode.cn/problems/rotated-digits/) · Medium · 灵茶山艾府：[数位 DP 通用模板（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

788.旋转数字

[力扣](https://leetcode-cn.com/problems/rotated-digits/)

由于各位之间实际上都是独立的，因此可以从低位开始使用动态规划来计算。不过注意到n这里最多也就到10000，那么直接遍历1到n中的所有数，然后分离每位数字进行判断即可。判断的依据是对于一个数，若其各位数字中不包含3、4、7，且至少有2、5、6、9其中一个，那么这个数字就是好数。

最后附上python代码：

```python
class Solution(object):
    def rotatedDigits(self, N):
        """
        :type N: int
        :rtype: int
        """

        res = 0
        for x in range(1, N + 1):
            flag = False
            while x:
                tmp = x % 10
                x /= 10
                if tmp in (3, 4, 7):
                    flag = False
                    break
                if tmp in (2, 5, 6, 9):
                    flag = True
            
            if flag:
                res += 1
        
        return res
```
