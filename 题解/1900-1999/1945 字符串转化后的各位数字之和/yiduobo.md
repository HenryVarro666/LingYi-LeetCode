---
title: "1945. 字符串转化后的各位数字之和"
aliases: ["yiduobo的每日leetcode 1945.字符串转化后的各位数字之和"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/490421357"
zhihu_id: "490421357"
zhihu_title: "yiduobo的每日leetcode 1945.字符串转化后的各位数字之和"
question_id: "1945"
question: "字符串转化后的各位数字之和"
problem_url: "https://leetcode.cn/problems/sum-of-digits-of-string-after-convert/"
difficulty: "Easy"
created: "2022-03-30T18:49:55+08:00"
updated: "2022-03-30T18:49:55+08:00"
upvotes: 0
comments: 0
---

# 1945. 字符串转化后的各位数字之和

> **[yiduobo的每日leetcode 1945.字符串转化后的各位数字之和](https://zhuanlan.zhihu.com/p/490421357) · 知乎 · 2022-03-30 · 赞同 0**
> 力扣：[1945. 字符串转化后的各位数字之和](https://leetcode.cn/problems/sum-of-digits-of-string-after-convert/) · Easy · 灵茶山艾府：[Go 模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1945.字符串转化后的各位数字之和

[力扣](https://leetcode-cn.com/problems/sum-of-digits-of-string-after-convert/)

比较基础的题目，直接按照题目意思进行模拟即可。注意到题目中的k大于0，因此至少会执行一次数位和，所以一开始就没必要将字符串转化为数字串，而是直接将每个字符拆出来之后计算数位和，然后再执行剩下的k - 1次数位和即可。

最后附上python代码：

```python
class Solution(object):
    def getLucky(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        now = 0
        for char in s:
            num = ord(char) - 96
            now += num % 10 + num / 10
        
        for _ in range(k - 1):
            tmp = now
            now = 0
            while tmp:
                now += tmp % 10
                tmp /= 10
        
        return now
```
