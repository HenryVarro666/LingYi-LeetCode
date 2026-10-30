---
title: "67. 二进制求和"
aliases: ["yiduobo的每日leetcode 67.二进制求和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/simulation", "题单/面试经典-150-题", "题单/面试经典-150-题/位运算"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/130821156"
zhihu_id: "130821156"
zhihu_title: "yiduobo的每日leetcode 67.二进制求和"
question_id: "67"
question: "二进制求和"
problem_url: "https://leetcode.cn/problems/add-binary/"
difficulty: "Easy"
created: "2020-04-15T13:49:36+08:00"
updated: "2020-04-15T13:49:36+08:00"
upvotes: 0
comments: 0
---

# 67. 二进制求和

> **[yiduobo的每日leetcode 67.二进制求和](https://zhuanlan.zhihu.com/p/130821156) · 知乎 · 2020-04-15 · 赞同 0**
> 力扣：[67. 二进制求和](https://leetcode.cn/problems/add-binary/) · Easy · 灵茶山艾府：[模拟加法计算过程（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

67.二进制求和<https://leetcode-cn.com/problems/add-binary/>

高精度加法二进制版本，依然是从低位到高位一位一位相加，不过这里每位的和应该是模2而不是模10，最后也需要注意最高位进位的情况。

最后附上python代码：

```
class Solution(object):
    def addBinary(self, a, b):
        """
        :type a: str
        :type b: str
        :rtype: str
        """

        pos_a = len(a) - 1
        pos_b = len(b) - 1

        tmp = 0
        res = ''

        while pos_a > -1 or pos_b > -1:
            if pos_a > -1:
                tmp += int(a[pos_a])
            if pos_b > -1:
                tmp += int(b[pos_b])

            if tmp >= 2:
                tmp -= 2
                res = str(tmp) + res
                tmp = 1
            else:
                res = str(tmp) + res
                tmp = 0

            pos_a -= 1
            pos_b -= 1
        
        if tmp:
            res = '1' + res

        return res
```
