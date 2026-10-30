---
title: "1281. 整数的各位积和之差"
aliases: ["yiduobo的每日leetcode 1281.整数的各位积和之差"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/388479703"
zhihu_id: "388479703"
zhihu_title: "yiduobo的每日leetcode 1281.整数的各位积和之差"
question_id: "1281"
question: "整数的各位积和之差"
problem_url: "https://leetcode.cn/problems/subtract-the-product-and-sum-of-digits-of-an-integer/"
difficulty: "Easy"
created: "2021-07-10T18:16:45+08:00"
updated: "2021-07-10T18:16:45+08:00"
upvotes: 0
comments: 0
---

# 1281. 整数的各位积和之差

> **[yiduobo的每日leetcode 1281.整数的各位积和之差](https://zhuanlan.zhihu.com/p/388479703) · 知乎 · 2021-07-10 · 赞同 0**
> 力扣：[1281. 整数的各位积和之差](https://leetcode.cn/problems/subtract-the-product-and-sum-of-digits-of-an-integer/) · Easy · 灵茶山艾府：[枚举数位，不用字符串（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1281.整数的各位积和之差

[力扣](https://leetcode-cn.com/problems/subtract-the-product-and-sum-of-digits-of-an-integer/)

比较基础的题目，直接分离每一位，分别求和求积之后作差即可。

最后附上python代码：

```python
class Solution(object):
    def subtractProductAndSum(self, n):
        """
        :type n: int
        :rtype: int
        """

        x = 0
        y = 1
        while n:
            now = n % 10
            n /= 10
            x += now
            y *= now
        
        return y - x
```
