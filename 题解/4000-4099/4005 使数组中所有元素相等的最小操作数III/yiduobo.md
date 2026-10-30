---
title: "4005. 使数组中所有元素相等的最小操作数III"
aliases: ["yiduobo的每日leetcode 4005.使数组中所有元素相等的最小操作数III"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2067743425168937396"
zhihu_id: "2067743425168937396"
zhihu_title: "yiduobo的每日leetcode 4005.使数组中所有元素相等的最小操作数III"
question_id: "4005"
question: "使数组中所有元素相等的最小操作数III"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-array-equal-iii/"
created: "2026-08-03T23:00:02+08:00"
updated: "2026-08-03T23:00:02+08:00"
upvotes: 0
comments: 0
---

# 4005. 使数组中所有元素相等的最小操作数III

> **[yiduobo的每日leetcode 4005.使数组中所有元素相等的最小操作数III](https://zhuanlan.zhihu.com/p/2067743425168937396) · 知乎 · 2026-08-03 · 赞同 0**
> 力扣：[4005. 使数组中所有元素相等的最小操作数III](https://leetcode.cn/problems/minimum-operations-to-make-array-equal-iii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4005.使数组中所有元素相等的最小操作数III

<https://leetcode.cn/problems/minimum-operations-to-make-array-equal-iii/description/>

题目给出一个整数数组nums。

在一次操作中，可以选择任意元素nums[index]，并执行以下操作之一：

- 乘法：将nums[index]乘以一个整数k，这里的k需要大于等于2
- 除法：将nums[index]除以一个整数k，这里的k需要在2到nums[index - 1]之间，且k必须是nums[index]的约数

问使得nums中所有元素都相等的最少操作次数。

根据题目描述，很容易得到一个操作次数的上限：

令t表示nums中所有元素的最小公倍数，那么对于不等于t的元素，只需要一次操作就能变成t，而等于t的元素则无需操作。换言之，选择t所需的操作次数不会超过n次。

更进一步的，优化的目标就是改为选择nums中原始就存在的某个元素x，此时可以省去所有等于x的元素的操作次数，除此之外，对于不等于x的自身，且为x约数或者倍数的元素，依然需要一次操作，而剩余的元素则需要两次操作。基于这个结论计算操作次数之和，就能判断是否更优了。

到了这里，问题就转化成了给出一个数组，对于其中每种元素，计算在数组中的该元素的约数以及倍数的总量。本题中数组的长度可达10^5，因此朴素的平方算法是不行的。而取值的值域可达10^9，因此使用类似筛法的倍数枚举也是不行的。

我在这里选择的是先分解质因数，然后构造约数的做法，具体来说：

- 先取出nums中的最大值ma，并计算不超过sqrt(ma)的所有质数
- 对nums中每个元素分解质因数，同时依照分解的结果构造nums的约数列表
- 使用两个数组mul以及div分别记录每个元素的倍数以及约数的数量，那么对于当前元素v的每个约数x，只需将freq[v]累加到mul[x]，并将freq[x]累加到div[v]即可
- 最后遍历nums中的所有元素，对于当前元素v，由于v是自身的约数以及倍数，因此上面所说的需要一次操作的元素数量one就是mul[v] - freq[v] + div[v] - freq[v]，最后所需的操作次数就是(n - one - freq[v]) \* 2 + one。需要注意，由于题目的性质，1不能作为最终的v，因此这里只需要考虑大于1的元素

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        ma = int(max(nums) ** 0.5 + 0.5)
        f = [True] * (ma + 1)
        prime = []
        for v in range(2, ma + 1):
            if f[v]:
                prime.append(v)
                for x in range(v + v, ma + 1, v):
                    f[v] = False
        
        freq = {}
        for v in nums:
            freq[v] = freq.get(v, 0) + 1
        
        mul = {}
        div = {}
        for v in freq.keys():
            x = v
            d = [1]
            for p in prime:
                if p * p > x:
                    break
                new_d = []
                power = 1
                while x % p == 0:
                    x //= p
                    power *= p
                    new_d.extend([num * power for num in d])
                d.extend(new_d)

            if x > 1:
                d.extend([num * x for num in d])

            for x in d:
                mul[x] = mul.get(x, 0) + freq[v]
                div[v] = div.get(v, 0) + freq.get(x, 0)
        
        res = len(nums)
        for v in freq.keys():
            if v > 1:
                one = mul[v] - freq[v] + div[v] - freq[v]
                res = min(res, (len(nums) - freq[v] - one) * 2 + one)
        
        return res
```
