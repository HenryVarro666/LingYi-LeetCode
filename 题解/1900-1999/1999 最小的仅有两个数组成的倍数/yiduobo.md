---
title: "1999. 最小的仅有两个数组成的倍数"
aliases: ["yiduobo的每日leetcode 1999.最小的仅有两个数组成的倍数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/624653247"
zhihu_id: "624653247"
zhihu_title: "yiduobo的每日leetcode 1999.最小的仅有两个数组成的倍数"
question_id: "1999"
question: "最小的仅有两个数组成的倍数"
problem_url: "https://leetcode.cn/problems/smallest-greater-multiple-made-of-two-digits/"
created: "2023-04-25T03:16:41+08:00"
updated: "2023-04-25T03:16:41+08:00"
upvotes: 0
comments: 0
---

# 1999. 最小的仅有两个数组成的倍数

> **[yiduobo的每日leetcode 1999.最小的仅有两个数组成的倍数](https://zhuanlan.zhihu.com/p/624653247) · 知乎 · 2023-04-25 · 赞同 0**
> 力扣：[1999. 最小的仅有两个数组成的倍数](https://leetcode.cn/problems/smallest-greater-multiple-made-of-two-digits/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1999.最小的仅由两个数组成的倍数

[力扣](https://leetcode.cn/problems/smallest-greater-multiple-made-of-two-digits/)

由于本题限定了取数的范围不超过2^31，同时每一位上只有digit1和digit2这两种数字可选，那么完全可以一趟dfs，构造出所有大小在0到2^31 - 1之间且仅由这两个数字构成的数字，然后将这些数排序后逐个检测是否大于k且是k的倍数。

在这里需要注意数字中可能存在0，因此需要注意不要生成有多余前导0的数。

最后附上python代码：

```python
class Solution(object):
    def findInteger(self, k, digit1, digit2):
        """
        :type k: int
        :type digit1: int
        :type digit2: int
        :rtype: int
        """

        candidate = []

        def generate(now):
            if now > 2147483647:
                return
            
            candidate.append(now)
            if now > 0:
                generate(now * 10 + digit1)
                generate(now * 10 + digit2)
        

        generate(digit1)
        generate(digit2)

        for v in sorted(candidate):
            if v > k and v % k == 0:
                return v
        
        return -1
```
