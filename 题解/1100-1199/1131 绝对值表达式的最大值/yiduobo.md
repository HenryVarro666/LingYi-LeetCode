---
title: "1131. 绝对值表达式的最大值"
aliases: ["yiduobo的每日leetcode 1131.绝对值表达式的最大值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/376520018"
zhihu_id: "376520018"
zhihu_title: "yiduobo的每日leetcode 1131.绝对值表达式的最大值"
question_id: "1131"
question: "绝对值表达式的最大值"
problem_url: "https://leetcode.cn/problems/maximum-of-absolute-value-expression/"
created: "2021-05-30T20:12:33+08:00"
updated: "2021-05-30T20:12:33+08:00"
upvotes: 1
comments: 0
---

# 1131. 绝对值表达式的最大值

> **[yiduobo的每日leetcode 1131.绝对值表达式的最大值](https://zhuanlan.zhihu.com/p/376520018) · 知乎 · 2021-05-30 · 赞同 1**
> 力扣：[1131. 绝对值表达式的最大值](https://leetcode.cn/problems/maximum-of-absolute-value-expression/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1131.绝对值表达式的最大值

[力扣](https://leetcode-cn.com/problems/maximum-of-absolute-value-expression/)

由于这里的arr长度最多有40000，那么只能使用O(n)或者O(nlogn)的做法，看样子必须将绝对值拆出来。

对于|arr1[i] - arr1[j]| + |arr2[i] - arr2[j]| + |i - j|，拆出来可能有下面八种情况：

s1 \= arr1[i] - arr1[j] + arr2[i] - arr2[j] + i - j

s2 \= arr1[i] - arr1[j] + arr2[i] - arr2[j] - i + j

s3 \= arr1[i] - arr1[j] - arr2[i] + arr2[j] + i - j

s4 \= arr1[i] - arr1[j] - arr2[i] + arr2[j] - i + j

s5 \= -arr1[i] + arr1[j] + arr2[i] - arr2[j] + i - j

s6 \= -arr1[i] + arr1[j] + arr2[i] - arr2[j] - i + j

s7 \= -arr1[i] + arr1[j] - arr2[i] + arr2[j] + i - j

s8 \= -arr1[i] + arr1[j] - arr2[i] + arr2[j] - i + j

如果将i和j分别合并起来，那么就有

s1 \= (arr1[i] + arr2[i] + i) - (arr1[j] + arr2[j] + j)

s2 \= (arr1[i] + arr2[i] - i) - (arr1[j] + arr2[j] - j)

s3 \= (arr1[i] - arr2[i] + i) - (arr1[j] - arr2[j] + j)

s4 \= (arr1[i] - arr2[i] - i) - (arr1[j] - arr2[j] - j)

s5 \= -s4

s6 \= -s3

s7 \= -s2

s8 \= -s1

可以发现，括号里面的构成形式是一致的，仅有下标的区别。那么设

a[i] \= arr1[i] + arr2[i] + i

b[i] \= arr1[i] + arr2[i] - i

c[i] \= arr1[i] - arr2[i] + i

d[i] \= arr1[i] - arr2[i] - i

那么就有

s1 \= a[i] - a[j]

s2 \= b[i] - b[j]

s3 \= c[i] - c[j]

s4 \= d[i] - d[j]

s5 \= -s4 \= d[j] - d[i]

s6 \= -s3 \= c[j] - c[i]

s7 \= -s2 \= b[j] - b[i]

s8 \= -s1 \= a[j] - a[i]

到了这里，我们就可以先一趟扫描，求出所有的a、b、c、d，那么最终答案就是

max(max(a) - min(a), max(b) - min(b), max(c) - min(c), max(d) - min(d))

关于这个做法正确性，若某种情况下求出来的值v1不满足绝对值条件，那么其满足绝对值的形式的值必然可以对应到另一种情况下，而对应的值v2必然是大于v1的，因此最终答案必然是满足绝对值条件的。

最后附上python代码：

```python
class Solution(object):
    def maxAbsValExpr(self, arr1, arr2):
        """
        :type arr1: List[int]
        :type arr2: List[int]
        :rtype: int
        """

        n = len(arr1)
        max_a = min_a = arr1[0] + arr2[0]
        max_b = min_b = arr1[0] + arr2[0]
        max_c = min_c = arr1[0] - arr2[0]
        max_d = min_d = arr1[0] - arr2[0]
        for index in range(1, n):
            a = arr1[index] + arr2[index] + index
            max_a = max(max_a, a)
            min_a = min(min_a, a)

            b = arr1[index] + arr2[index] - index
            max_b = max(max_b, b)
            min_b = min(min_b, b)

            c = arr1[index] - arr2[index] + index
            max_c = max(max_c, c)
            min_c = min(min_c, c)

            d = arr1[index] - arr2[index] - index
            max_d = max(max_d, d)
            min_d = min(min_d, d)
        
        return max(max_a - min_a, max_b - min_b, max_c - min_c, max_d - min_d)
```
