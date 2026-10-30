---
title: "1416. 恢复数组"
aliases: ["yiduobo的每日leetcode 1416.恢复数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/407066346"
zhihu_id: "407066346"
zhihu_title: "yiduobo的每日leetcode 1416.恢复数组"
question_id: "1416"
question: "恢复数组"
problem_url: "https://leetcode.cn/problems/restore-the-array/"
created: "2021-09-05T16:36:06+08:00"
updated: "2021-09-05T16:36:07+08:00"
upvotes: 0
comments: 0
---

# 1416. 恢复数组

> **[yiduobo的每日leetcode 1416.恢复数组](https://zhuanlan.zhihu.com/p/407066346) · 知乎 · 2021-09-05 · 赞同 0**
> 力扣：[1416. 恢复数组](https://leetcode.cn/problems/restore-the-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1416.恢复数组

[力扣](https://leetcode-cn.com/problems/restore-the-array/)

动态规划的问题，令f[i]表示字符串中最后i位可以恢复出的数组方案数，那么对于f[i]：

1、若当前位上的数字为0，由于不能出现前导0，因此无论怎么分割得到的都是非法的情况，于是就有f[i] \= 0

2、若当前位上的数字不为0，那么可以枚举从当前位开始的一位数、两位数、...、l位数，这里的l为k的位数，然后分别检测这些数与k的大小。若小于等于k，那么说明可以进行对应的分割，就有f[i] +\= f[i - j - 1]，这里的j是本次分割出的数字的位数。

可以发现，这里分割出来的数字是具有某种性质的，例如样例5中的1234567890，假设此时的k是1000，那么当我们在处理6时，可以分割的数字为6、67、678、6789，而在处理之前的5时，则为5、56、567、5678。对比一下可以发现，这里的

5就是当前位上5

56是之前的6 + 5 \* 10

567是之前的67 + 5 \* 100

5678是之前的678 + 5 \* 1000

即我们相当于将当前位上的数字添加到之前分割的前l - 1种数字的前面，形成本次分割的后l - 1种数字，然后再结合当前位上的数字构成本次分割的l种情况。

那么我们可以从后向前一趟扫描，使用一个num_list来维护当前分割的数字。每次先通过上一轮的结果和当前位上的数字计算出本轮分割的数字，然后逐个检测并更新当前的f。

最后附上python代码：

```python
class Solution(object):
    def numberOfArrays(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        mod = 10 ** 9 + 7

        tmp = k
        l = 0
        p = [1]
        while tmp:
            l += 1
            tmp /= 10
            p.append(p[-1] * 10)
        
        num_list = [0] * l
        f = [1]
        n = len(s)
        for i in range(n - 1, -1, -1):
            for j in range(l - 1, 0, -1):
                num_list[j] = num_list[j - 1] + (ord(s[i]) - 48) * p[j]
            num_list[0] = ord(s[i]) - 48
            f.append(0)

            if num_list[0] > 0:
                for j in range(0, min(l, len(f) - 1)):
                    if num_list[j] >= 1 and num_list[j] <= k:
                        f[-1] += f[-1 - j - 1]
                        f[-1] %= mod

        return f[-1]
```
