---
title: "2117. 一个区间内所有数乘积的缩写"
aliases: ["yiduobo的每日leetcode 2117.一个区间内所有数乘积的缩写"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/bao-li", "leetcode/gao-jing-du-suan-fa", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/524325138"
zhihu_id: "524325138"
zhihu_title: "yiduobo的每日leetcode 2117.一个区间内所有数乘积的缩写"
question_id: "2117"
question: "一个区间内所有数乘积的缩写"
problem_url: "https://leetcode.cn/problems/abbreviating-the-product-of-a-range/"
difficulty: "Hard"
rating: 2477
created: "2022-06-04T22:43:36+08:00"
updated: "2022-06-04T22:43:36+08:00"
upvotes: 0
comments: 0
---

# 2117. 一个区间内所有数乘积的缩写

> **[yiduobo的每日leetcode 2117.一个区间内所有数乘积的缩写](https://zhuanlan.zhihu.com/p/524325138) · 知乎 · 2022-06-04 · 赞同 0**
> 力扣：[2117. 一个区间内所有数乘积的缩写](https://leetcode.cn/problems/abbreviating-the-product-of-a-range/) · Hard · 灵茶山艾府：[[灵茶山艾府题解/solutions/2117 一个区间内所有数乘积的缩写 · -更新高精度算法- 拆分成四个问题：计算对数 + 对 1e5 取模 + 计算尾零个数 +|[更新高精度算法] 拆分成四个问题：计算对数 + 对 1e5 取模 + 计算尾零个数 + 判断剩余数字的长度]]

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2117.一个区间内所有数乘积的缩写

[力扣](https://leetcode.cn/problems/abbreviating-the-product-of-a-range/)

最直观的做法自然是暴力计算。使用python的话直接乘就行了，使用c++这类则需要写一个大数乘以int的乘法。在这里乘积的长度不到4000位，因此即使采用最纯粹的暴力乘法，时间复杂度也是没有问题的。

非暴力法则卡在了前5位上。

题目要求的三个部分，其中后5位和末尾0的个数都是比较好求的，不过需要优先处理末尾0才能处理最后5位。

对于末尾0的个数，只需统计left到right直接因此5的数目即可。在统计的过程中需要同步除掉这些5，同时还需要除掉等量的因子2。

接下来后5位只需一边乘一边对100000取模就好了。

问题是最高的5位没有什么好的想法。如果使用近似算法的话难免丢失精度，但是常规算法也没有什么特别好的处理方法，所以我最后还是采用的暴力法。

另外，对于python最好还是不要手动实现大整数乘法，真的是慢得过分了。

最后附上python代码：

```python
class Solution(object):
    def abbreviateProduct(self, left, right):
        """
        :type left: int
        :type right: int
        :rtype: str
        """

        c = 0
        now = 1
        for num in range(left, right + 1):
            now *= num

        s = str(now)
        l = 0
        r = len(s) - 1
        while s[r] == '0':
            r -= 1
            c += 1
        if r + 1 <= 10:
            return s[:r + 1] + 'e' + str(c)
        else:
            return s[:5] + '...' + s[r - 4 : r + 1] + 'e' + str(c)
```
