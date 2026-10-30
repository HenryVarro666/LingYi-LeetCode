---
title: "954. 二倍数对数组"
aliases: ["yiduobo的每日leetcode 954.二倍数对数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/360238326"
zhihu_id: "360238326"
zhihu_title: "yiduobo的每日leetcode 954.二倍数对数组"
question_id: "954"
question: "二倍数对数组"
problem_url: "https://leetcode.cn/problems/array-of-doubled-pairs/"
created: "2021-03-26T23:54:36+08:00"
updated: "2021-03-26T23:54:36+08:00"
upvotes: 0
comments: 0
---

# 954. 二倍数对数组

> **[yiduobo的每日leetcode 954.二倍数对数组](https://zhuanlan.zhihu.com/p/360238326) · 知乎 · 2021-03-26 · 赞同 0**
> 力扣：[954. 二倍数对数组](https://leetcode.cn/problems/array-of-doubled-pairs/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

954.二倍数对数组

[力扣](https://leetcode-cn.com/problems/array-of-doubled-pairs/)

首先，注意到题目给出的数组中可能存在正数、负数或者0，那么对于一个正数而言，其二倍必然也是正数。同样的，负数的二倍还是负数，0的二倍还是0，因此我们需要先将原始数组arr划分成正数、负数以及0三个部分。若其中某个部分的长度为奇数，那么说明某个部分存在落单的数组元素，而这个落单的数组元素也无法与其他部分的元素达成二倍关系，因此此时必然无法构造出符合题目要求的数组。

接下来，0的部分我们无需处理，只需要判断正数和负数的部分。由于我们不关心最终构造的结果，因此对于负数的部分，我们也可以将所有数取相反数来处理。此时，问题就转化成了两个由正数构成的数组，能否分别形成二倍数对数组。

对于这个问题，一个自然的想法就是从边界入手，不妨先考虑当前最小的元素。设当前剩下数中最小的数为x，如果x没有通过之前处理的数放在奇数位上，由于x不可能是之后剩下数的两倍，因此当前的x必然要放在偶数位上，同时还需要一个2x放在x对应的奇数位上。于是可以使用一个dict记录当前放在奇数位上的数以及使用的次数。

对于当前处理的x：

1、若x不在dict中或dict中x使用次数为0，那么就将x放在偶数位上，同时将dict中的2x加上1

2、否则将x放在奇数位上，同时将dict中的x减去1

若处理完所有数之后dict为空，那么就可以成功构造出符合题目要求的数组。

最后附上python代码：

```python
import heapq

class Solution(object):
    def canReorderDoubled(self, arr):
        """
        :type arr: List[int]
        :rtype: bool
        """

        pos_list = []
        neg_list = []
        zero_cnt = 0
        for num in arr:
            if num > 0:
                pos_list.append(num)
            elif num < 0:
                neg_list.append(-num)
            else:
                zero_cnt += 1
        
        if zero_cnt % 2 == 1:
            return False

        if len(pos_list) % 2 == 1:
            return False

        if len(neg_list) % 2 == 1:
            return False

        return self.check(pos_list) and self.check(neg_list)

    def check(self, num_list):
        heapq.heapify(num_list)
        used = {}
        while num_list:
            min_num = heapq.heappop(num_list)
            if used.get(min_num, 0) > 0:
                used[min_num] -= 1
            else:
                used[min_num * 2] = used.get(min_num * 2, 0) + 1
        
        return sum(used.values()) == 0
```
