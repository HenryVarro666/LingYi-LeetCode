---
title: "1881. 插入后的最大值"
aliases: ["yiduobo的每日leetcode 1881.插入后的最大值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/476786591"
zhihu_id: "476786591"
zhihu_title: "yiduobo的每日leetcode 1881.插入后的最大值"
question_id: "1881"
question: "插入后的最大值"
problem_url: "https://leetcode.cn/problems/maximum-value-after-insertion/"
difficulty: "Medium"
rating: 1381
created: "2022-03-06T23:59:17+08:00"
updated: "2022-03-06T23:59:17+08:00"
upvotes: 0
comments: 0
---

# 1881. 插入后的最大值

> **[yiduobo的每日leetcode 1881.插入后的最大值](https://zhuanlan.zhihu.com/p/476786591) · 知乎 · 2022-03-06 · 赞同 0**
> 力扣：[1881. 插入后的最大值](https://leetcode.cn/problems/maximum-value-after-insertion/) · Medium · 灵茶山艾府：[贪心，扫描一遍寻找插入位置](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1881.插入后的最大值

[力扣](https://leetcode-cn.com/problems/maximum-value-after-insertion/)

首先，题目给出的n可能为正也可能为负，因此需要分开讨论。

当n为正数时，为了使得答案最大，显然应该将较大的数放在高位上。那么可以从高位开始向后遍历，若要插入的数比当前位上的数更大，那么就插入到当前位置。

在这里必须是严格的大于而不是大于等于，举个例子很容易就能说明。对于231而言，如果要插入一个2，那么插入在1的前方可以得到2321，而如果插入到2的前方得到的是2231，即要插入的数等于当前位上的数时，插入到当前位置将会让后面位上的数向后移动，可能出现后面更大的数被之前较小的数占据了位置的情况。

当n为负数时，为了使得答案最大，则应该将较小的数放在高位上。那么同样是从高位开始向后遍历，若要插入的数比当前位上的数更小，那么就插入到当前位置。

在这里同样是必须严格小于，理由与上面一样就不展开了。

最后附上python代码：

```python
class Solution(object):
    def maxValue(self, n, x):
        """
        :type n: str
        :type x: int
        :rtype: str
        """

        if n[0] == '-':
            for index in range(1, len(n)):
                if int(n[index]) > x:
                    return n[:index] + str(x) + n[index:]
        else:
            for index in range(len(n)):
                if int(n[index]) < x:
                    return n[:index] + str(x) + n[index:]
            
        return n + str(x)
```
