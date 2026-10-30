---
title: "805. 数组的均值分割"
aliases: ["yiduobo的每日leetcode 805.数组的均值分割"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343116689"
zhihu_id: "343116689"
zhihu_title: "yiduobo的每日leetcode 805.数组的均值分割"
question_id: "805"
question: "数组的均值分割"
problem_url: "https://leetcode.cn/problems/split-array-with-same-average/"
created: "2021-01-09T21:22:00+08:00"
updated: "2021-01-09T21:22:00+08:00"
upvotes: 2
comments: 0
---

# 805. 数组的均值分割

> **[yiduobo的每日leetcode 805.数组的均值分割](https://zhuanlan.zhihu.com/p/343116689) · 知乎 · 2021-01-09 · 赞同 2**
> 力扣：[805. 数组的均值分割](https://leetcode.cn/problems/split-array-with-same-average/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

805.数组的均值分割

[力扣](https://leetcode-cn.com/problems/split-array-with-same-average/)

拿到题目的第一想法是使用状态压缩动态规划，但是发现这里的数字达到了30个，那么状态数就有2^30，时空复杂度都不允许。

接下来想到的是传统的动态规划，令f[i][j][k]表示前i个数中选择j个数，是否能让其和为k。这个做法的复杂度则是n^3 \* 10000，依然不行。

这两种做法都不可行，那么需要从题目中挖掘更多有用的信息。

题目要求B和C平均值相等，那么也就是

sum(B) / len(B) \= sum(C) / len(C)

由于B和C都不为空，那么可以两边同时乘上len(B) \* len(C)，得到

sum(B) \* len(C) \= sum(C) \* len(B)

其中len(C)又可以认为是len(A) - len(B)，那么就有

sum(B) \* (len(A) - len(B)) \= sum(C) \* len(B)

化简之后可以得到

sum(B) \* len(A) \= (sum(C) + sum(B)) \* len(B)

由于sum(C) + sum(B) \= sum(A)，那么两边再同时除以len(A) \* len(B)，就有

sum(B) / len(B) \= sum(A) / len(A)

可以发现，题目可以转化成从集合A中找出若干个数，使这些数的平均数恰好等于所有数的平均数。那么一个自然的想法就是所有数全部减去平均数avg，然后判断是否存在若干个数的和为0。由于avg不一定是整数，那么可以先将所有数全部乘上n，不会影响最终的结果。

到了这里，问题就转化成了给出一些整数，判断是否存在若干个数的和恰好为0。这里的若干个数必须大于0，且不能全选。不过这里最多还是30个整数 ，直接判断的复杂度还是很高，不过可以将这n个数分为两组，然后计算每一组所有可能的情况，并利用set来判断当前形成的sum是否等于0，或者在另一组内是否存在若干个数和为-sum。如果满足其中一种情况，那么答案就是true。

最后附上python代码：

```python
class Solution(object):
    def splitArraySameAverage(self, A):
        """
        :type A: List[int]
        :rtype: bool
        """

        n = len(A)
        if n == 1:
            return False
        A = [x * n for x in A]
        avg = sum(A) / n
        A = [x - avg for x in A]
        s_first = sum(A[:n/2])
        s_second = sum(A[n/2:])
        first_set = set([0])
        for now in A[:n/2]:
            for num in list(first_set):
                tmp = now + num
                if tmp == 0:
                    return True
                first_set.add(tmp)
        
        second_set = set([0])
        for now in A[n/2:]:
            for num in list(second_set):
                tmp = now + num
                if tmp == 0:
                    return True
                if -tmp in first_set and (tmp != s_second or -tmp != s_first):
                    return True
                second_set.add(tmp)
        
        return False
```
