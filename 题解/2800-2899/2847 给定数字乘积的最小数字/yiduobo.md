---
title: "2847. 给定数字乘积的最小数字"
aliases: ["yiduobo的每日leetcode 2847.给定数字乘积的最小数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/660403563"
zhihu_id: "660403563"
zhihu_title: "yiduobo的每日leetcode 2847.给定数字乘积的最小数字"
question_id: "2847"
question: "给定数字乘积的最小数字"
problem_url: "https://leetcode.cn/problems/smallest-number-with-given-digit-product/"
created: "2023-10-10T03:18:16+08:00"
updated: "2023-10-10T03:18:16+08:00"
upvotes: 0
comments: 0
---

# 2847. 给定数字乘积的最小数字

> **[yiduobo的每日leetcode 2847.给定数字乘积的最小数字](https://zhuanlan.zhihu.com/p/660403563) · 知乎 · 2023-10-10 · 赞同 0**
> 力扣：[2847. 给定数字乘积的最小数字](https://leetcode.cn/problems/smallest-number-with-given-digit-product/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2847.给定数字乘积的最小数字

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/smallest-number-with-given-digit-product/)

由于题目中得到的答案只能逐位相乘，那么就意味着n的质因子只能包含2、3、5、7。其中5和7只能单独出现，而对于2和3则可以组合出现，例如两个2构成4，两个3构成9。

为了使得答案最小，那么就应该尽量组合2和3，现在的问题是应该如何组合。例如有一个2和两个3，在这里可以让2和3组合得到6，另一个3落单，也可以让两个3组合得到9，单独的2落单。可以发现，组合的一遍越大，另一边就越小，而让小的这边放在高位最终得到的数显然是更小的，也就是说应该尽量组合出较大的数。更具体的，就是应该优先组合9和8，然后是6，最后是4。

另外由于5和7是单独的，因此在这里就可以直接从9到2倒序枚举，每次尽量从n中分离出当前枚举到的因子，直到无法分离。若最终的n大于1，说明n包含大于7的质因子，此时直接返回-1，否则只需按照2到9的顺序将分离出的因子拼接好返回即可。

最后附上python代码：

```python
class Solution(object):
    def smallestNumber(self, n):
        """
        :type n: int
        :rtype: str
        """

        if n == 1:
            return "1"

        cnt = [0] * 10
        for i in range(9, 1, -1):
            while n % i == 0:
                cnt[i] += 1
                n /= i
        
        if n > 1:
            return "-1"
        
        return "".join([str(i) * cnt[i] for i in range(2, 10)])
```
