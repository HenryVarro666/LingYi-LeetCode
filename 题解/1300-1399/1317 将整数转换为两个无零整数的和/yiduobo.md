---
title: "1317. 将整数转换为两个无零整数"
aliases: ["yiduobo的每日leetcode 1317.将整数转换为两个无零整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/random", "leetcode/probability-and-statistics", "题单/数学算法", "题单/贪心算法", "题单/数学算法/六-随机算法", "题单/贪心算法/六-构造题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/392949583"
zhihu_id: "392949583"
zhihu_title: "yiduobo的每日leetcode 1317.将整数转换为两个无零整数"
question_id: "1317"
question: "将整数转换为两个无零整数的和"
problem_url: "https://leetcode.cn/problems/convert-integer-to-the-sum-of-two-no-zero-integers/"
difficulty: "Easy"
rating: 1278
created: "2021-07-25T13:11:19+08:00"
updated: "2021-07-25T13:11:19+08:00"
upvotes: 1
comments: 0
---

# 1317. 将整数转换为两个无零整数

> **[yiduobo的每日leetcode 1317.将整数转换为两个无零整数](https://zhuanlan.zhihu.com/p/392949583) · 知乎 · 2021-07-25 · 赞同 1**
> 力扣：[1317. 将整数转换为两个无零整数的和](https://leetcode.cn/problems/convert-integer-to-the-sum-of-two-no-zero-integers/) · Easy · 灵茶山艾府：[三种方法：枚举/随机/构造（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1317.将整数转换为两个无零整数

[力扣](https://leetcode-cn.com/problems/convert-integer-to-the-sum-of-two-no-zero-integers/)

题目要求找出两个不含0的整数，二者之和为n。

若n的位数为1，那么1和n - 1必然是一组可行解。

若n的位数大于1，设为l，那么我们可以先将其分解成x \= 99...9与y \= n - 99...9，这里的x中一共是l - 1个9。接下来，对于y中所有为0的位数，我们将其变为1，同时将x中对应的位数减去1，这样就得到一组可行解了。

最后附上python代码：

```python
class Solution(object):
    def getNoZeroIntegers(self, n):
        """
        :type n: int
        :rtype: List[int]
        """

        tmp = n
        l = 0
        while tmp:
            l += 1
            tmp /= 10
        
        if l == 1:
            return [1, n - 1]
        else:
            x = 10 ** (l - 1) - 1
            y = n - x
            tmp = y
            p = 1
            while tmp:
                if tmp % 10 == 0:
                    y += p
                    x -= p
                p *= 10
                tmp /= 10
            return [x, y]
```
