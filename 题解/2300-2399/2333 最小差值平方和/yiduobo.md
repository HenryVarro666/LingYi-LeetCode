---
title: "2333. 最小差值平方和"
aliases: ["yiduobo的每日leetcode 2333.最小差值平方和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/math", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/558835002"
zhihu_id: "558835002"
zhihu_title: "yiduobo的每日leetcode 2333.最小差值平方和"
question_id: "2333"
question: "最小差值平方和"
problem_url: "https://leetcode.cn/problems/minimum-sum-of-squared-difference/"
difficulty: "Medium"
rating: 2011
created: "2022-08-28T23:27:36+08:00"
updated: "2022-08-28T23:27:36+08:00"
upvotes: 0
comments: 0
---

# 2333. 最小差值平方和

> **[yiduobo的每日leetcode 2333.最小差值平方和](https://zhuanlan.zhihu.com/p/558835002) · 知乎 · 2022-08-28 · 赞同 0**
> 力扣：[2333. 最小差值平方和](https://leetcode.cn/problems/minimum-sum-of-squared-difference/) · Medium · 灵茶山艾府：[等价转换 + 贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2333.最小差值平方和

[力扣](https://leetcode.cn/problems/minimum-sum-of-squared-difference/)

首先，由于是差值的平方，因此对nums1[i]加一就相当于对nums2[i]减一。令diff[i] \= abs(nums1[i] - nums2[i])，那么问题就可以转化为给出一共k \= k1 + k2次操作，每次可以将diff数组中的某个数减去1，问最终diff数组平方和的最小值是多少。

从直觉上来说，应该先操作diff数组中较大的值，可以给出简单的证明。

对于diff中的两个值x和y，满足0 \<\= x \< y。

此时如果操作x，那么二者的平方和就是(x - 1)^2 + y^2 \= x^2 + y^2 - 2x + 1。如果操作的是y，那么二者的平方和就是(y - 1)^2 + x^2 \= x^2 + y^2 - 2y + 1。后面的式子显然要小于前面的式子，因此每次操作都应该选择diff中的最大值来进行操作。

由于题目中给出的k1和k2取值范围都很大，因此不能直接模拟。在这里可以先将diff从大到小进行排序，然后逐个考虑。

在前diff[0] - diff[1]次操作中，diff[0]都是diff中最大的，因此这diff[0] - diff[1]次操作应该全部用在diff[0]上。接下来，diff数组中的最大值就是diff[0]和diff[1]两个，此时则应该交替操作这两个值，直到diff[0] \= diff[1] \= diff[2]为止，这个过程中需要的操作数为(diff[1] - diff[2]) \* 2。接下来则应该交替操作diff[0]、diff[1]、diff[2]直到三者都等于diff[3]为止，以此类推。

也就是说，在diff[0]到diff[index]都相等的情况下，需要(diff[index] - diff[index + 1]) \* (index + 1)次操作来将diff[0]到diff[index + 1]都变成diff[index + 1]。

于是可以一趟遍历，对于当前遍历到的diff[index]，考察当前剩下的k与上面这个操作次数间的大小关系。若k足够，那么就进行操作，然后继续向后遍历，否则就将k平均分配到diff[0]到diff[index]当中然后返回答案。

需要注意的是，还有一种特殊情况是k足够大，可以将所有的数都变为diff[n - 1]，此时就需要考察k与diff[n - 1] \* n的大小关系。如果k足够大，那么就可以将diff数组全部变为0，此时的答案就是0。若k不够大，那么同样是将剩下的k平均分给此时diff数组中的每一个数然后返回答案。

最后附上python代码：

```python
class Solution(object):
    def minSumSquareDiff(self, nums1, nums2, k1, k2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type k1: int
        :type k2: int
        :rtype: int
        """

        k = k1 + k2
        n = len(nums1)
        diff = sorted([abs(nums1[index] - nums2[index]) for index in range(n)], reverse=True)

        p = n - 1
        for index in range(n - 1):
            if (index + 1) * (diff[index] - diff[index + 1]) <= k:
                k -= (index + 1) * (diff[index] - diff[index + 1])
            else:
                p = index
                break

        if p == n - 1 and k >= diff[-1] * n:
            return 0

        delta = k / (p + 1)
        k %= (p + 1)
        res = 0

        for index in range(k):
            res += (diff[p] - delta - 1) ** 2
        for index in range(k, p + 1):
            res += (diff[p] - delta) ** 2
        for index in range(p + 1, n):
            res += diff[index] ** 2
        
        return res
```
