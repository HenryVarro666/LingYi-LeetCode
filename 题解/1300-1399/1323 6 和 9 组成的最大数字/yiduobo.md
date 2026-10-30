---
title: "1323. 6和9组成的最大数字"
aliases: ["yiduobo的每日leetcode 1323. 6和9组成的最大数字"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/math", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/393760184"
zhihu_id: "393760184"
zhihu_title: "yiduobo的每日leetcode 1323. 6和9组成的最大数字"
question_id: "1323"
question: "6 和 9 组成的最大数字"
problem_url: "https://leetcode.cn/problems/maximum-69-number/"
difficulty: "Easy"
rating: 1194
created: "2021-07-27T22:53:39+08:00"
updated: "2021-07-27T22:53:39+08:00"
upvotes: 0
comments: 0
---

# 1323. 6和9组成的最大数字

> **[yiduobo的每日leetcode 1323. 6和9组成的最大数字](https://zhuanlan.zhihu.com/p/393760184) · 知乎 · 2021-07-27 · 赞同 0**
> 力扣：[1323. 6 和 9 组成的最大数字](https://leetcode.cn/problems/maximum-69-number/) · Easy · 灵茶山艾府：[两种方法：用字符串/不用字符串（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1323\. 6和9组成的最大数字

[力扣](https://leetcode-cn.com/problems/maximum-69-number/)

比较基础的题目，将最高位的6变成9即可。将num转化为字符串然后从头开始扫描找到第一个6即可，当然也可以对num每次模10取出最低位，找到过程中最后一个出现的6。

最后附上python代码：

```python
class Solution(object):
    def maximum69Number (self, num):
        """
        :type num: int
        :rtype: int
        """

        delta = 0
        tmp = num
        p = 1
        while tmp:
            if tmp % 10 == 6:
                delta = p
            p *= 10
            tmp/= 10
        
        return num + delta * 3
```
