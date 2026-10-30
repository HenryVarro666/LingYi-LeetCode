---
title: "2443. 反转之后的数字和"
aliases: ["yiduobo的每日leetcode 2443.反转之后的数字和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/584448181"
zhihu_id: "584448181"
zhihu_title: "yiduobo的每日leetcode 2443.反转之后的数字和"
question_id: "2443"
question: "反转之后的数字和"
problem_url: "https://leetcode.cn/problems/sum-of-number-and-its-reverse/"
difficulty: "Medium"
created: "2022-11-18T00:11:50+08:00"
updated: "2022-11-18T00:11:50+08:00"
upvotes: 1
comments: 0
---

# 2443. 反转之后的数字和

> **[yiduobo的每日leetcode 2443.反转之后的数字和](https://zhuanlan.zhihu.com/p/584448181) · 知乎 · 2022-11-18 · 赞同 1**
> 力扣：[2443. 反转之后的数字和](https://leetcode.cn/problems/sum-of-number-and-its-reverse/) · Medium · 灵茶山艾府：[暴力枚举](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2443.反转之后的数字和

[力扣](https://leetcode.cn/problems/sum-of-number-and-its-reverse/)

由于num不会超过100000，那么只需从0开始到100000进行枚举，检测当前枚举到的数以及其反转之后的数之和是否等于num。

最后附上python代码：

```python
class Solution(object):
    def sumOfNumberAndReverse(self, num):
        """
        :type num: int
        :rtype: bool
        """

        for k in range(num + 1):
            now = k
            digit_list = []
            while now:
                digit_list.append(now % 10)
                now /= 10
            
            now = 0
            for digit in digit_list:
                now = now * 10 + digit
            
            if k + now == num:
                return True

        return False
```
