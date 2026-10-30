---
title: "2520. 统计能整除数字的计数"
aliases: ["yiduobo的每日leetcode 2520.统计能整除数字的计数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/634862833"
zhihu_id: "634862833"
zhihu_title: "yiduobo的每日leetcode 2520.统计能整除数字的计数"
question_id: "2520"
question: "统计能整除数字的位数"
problem_url: "https://leetcode.cn/problems/count-the-digits-that-divide-a-number/"
difficulty: "Easy"
created: "2023-06-08T23:53:04+08:00"
updated: "2023-06-08T23:53:04+08:00"
upvotes: 0
comments: 0
---

# 2520. 统计能整除数字的计数

> **[yiduobo的每日leetcode 2520.统计能整除数字的计数](https://zhuanlan.zhihu.com/p/634862833) · 知乎 · 2023-06-08 · 赞同 0**
> 力扣：[2520. 统计能整除数字的位数](https://leetcode.cn/problems/count-the-digits-that-divide-a-number/) · Easy · 灵茶山艾府：[O(1) 空间写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2520.统计能整除数字的计数

[力扣](https://leetcode.cn/problems/count-the-digits-that-divide-a-number/)

比较基础的题目。通过摸10不断分离出num的每一位，然后根据num能否整除该位来更新最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def countDigits(self, num):
        """
        :type num: int
        :rtype: int
        """

        tmp = num
        res = 0
        while tmp:
            v = tmp % 10
            tmp /= 10
            if num % v == 0:
                res += 1
        
        return res
```
