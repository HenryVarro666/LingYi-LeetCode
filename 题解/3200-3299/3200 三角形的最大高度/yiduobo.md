---
title: "3200. 三角形的最大高度"
aliases: ["yiduobo的每日leetcode 3200.三角形的最大高度"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/707323487"
zhihu_id: "707323487"
zhihu_title: "yiduobo的每日leetcode 3200.三角形的最大高度"
question_id: "3200"
question: "三角形的最大高度"
problem_url: "https://leetcode.cn/problems/maximum-height-of-a-triangle/"
difficulty: "Easy"
created: "2024-07-06T02:52:49+08:00"
updated: "2024-07-06T02:52:49+08:00"
upvotes: 1
comments: 1
---

# 3200. 三角形的最大高度

> **[yiduobo的每日leetcode 3200.三角形的最大高度](https://zhuanlan.zhihu.com/p/707323487) · 知乎 · 2024-07-06 · 赞同 1**
> 力扣：[3200. 三角形的最大高度](https://leetcode.cn/problems/maximum-height-of-a-triangle/) · Easy · 灵茶山艾府：[两种方法：枚举 / O(1) 数学公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3200.三角形的最大高度

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-height-of-a-triangle/description/)

题目给出两个整数blue和red，分别表示蓝色球和红色球的数量。接下来要求用这些球构造一个三角形，三角形的第k行中恰好有k个球，且这k个球同色。另外，三角形相邻行之间必须不同色，问最大可以构造出多大的三角形。

由于红色和蓝色在这里并没有本质区别，方便起见可以默认红色球的数量总是小于等于蓝色球的数量，如果不满足将二者互换即可。

接下来对于一个n行的三角形，其偶数行的数量even就是n整除2，而奇数行odd的数量则可以通过n减去even得到。接下来，奇数行上球的总数为1 + 3 + 5 + ... + (odd \* 2 - 1)，求和的结果恰好就是odd^2。另一方面，偶数行上球的总数为2 + 4 + 6 + ... + even \* 2，求和得结果为(even + 1) \* even。对比这两个数的大小，尝试用红球去填充较小的行，用蓝球去填充较大的行即可。

由于题目中球的总数不超过100，因此总的行数不可能超过20行，可以直接暴力枚举行数n，当然也采取二分答案的做法来处理。

最后附上python代码：

```python
class Solution(object):
    def maxHeightOfTriangle(self, red, blue):
        """
        :type red: int
        :type blue: int
        :rtype: int
        """

        if red > blue:
            red, blue = blue, red
        
        for res in range(20, 0, -1):
            even = res // 2
            odd = res - even

            even_balls = (1 + even) * even
            odd_balls = odd ** 2

            if min(odd_balls, even_balls) <= red and max(odd_balls, even_balls) <= blue:
                return res
```
