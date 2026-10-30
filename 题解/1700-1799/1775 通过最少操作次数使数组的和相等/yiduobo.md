---
title: "1775. 通过最少操作次数使数组的和相等"
aliases: ["yiduobo的每日leetcode 1775.通过最少操作次数使数组的和相等"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/461881370"
zhihu_id: "461881370"
zhihu_title: "yiduobo的每日leetcode 1775.通过最少操作次数使数组的和相等"
question_id: "1775"
question: "通过最少操作次数使数组的和相等"
problem_url: "https://leetcode.cn/problems/equal-sum-arrays-with-minimum-number-of-operations/"
difficulty: "Medium"
rating: 1850
created: "2022-01-25T23:31:33+08:00"
updated: "2022-01-25T23:31:33+08:00"
upvotes: 0
comments: 0
---

# 1775. 通过最少操作次数使数组的和相等

> **[yiduobo的每日leetcode 1775.通过最少操作次数使数组的和相等](https://zhuanlan.zhihu.com/p/461881370) · 知乎 · 2022-01-25 · 赞同 0**
> 力扣：[1775. 通过最少操作次数使数组的和相等](https://leetcode.cn/problems/equal-sum-arrays-with-minimum-number-of-operations/) · Medium · 灵茶山艾府：[没想明白？一个动画秒懂！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1775.通过最少操作次数使数组的和相等

[力扣](https://leetcode-cn.com/problems/equal-sum-arrays-with-minimum-number-of-operations/)

首先考虑边界情况。实际上样例二已经给出了提示。设两个数组的长度为m和n，那么两个数组的取值范围就分别是m到m \* 6以及n到n \* 6。由于两个数组等价，那么在这里不妨设m > n。为了使得两个区间是相交的，那么就必须要满足m \<\= n \* 6。换言之，若m > n \* 6，那么就无解。

接下来考虑一般情况。在这里不妨设ma为初始数组和较大的那个数组，其和为s1，设mi为初始数组和较小的数组，其和为s2。此时就需要想办法消减ma中较大的数，并增大mi中较小的数。

为了使得操作次数最少，那么显然应该从ma中的6和mi中的1开始进行操作，而接下来则是5和2，4和3，以此类推，直到枚举到1和6为止。

于是在这里可以从0到5开始进行枚举，对于枚举到的num，处理的就是ma中的6 - num以及mi中的num。

对于当前num，每次操作可以缩小5 - num的差距。设这两种数一共个k个，那么全部操作k次就可以缩小k \* (5 - num)的差距。记diff \= s1 - s2，那么此时就有两种情况：

1、若k \* (5 - num) \< diff，那么就还需要对别的数进行操作。现在这里操作全部的k次，使用k来更新答案，并将diff减去k \* 5，然后继续考察下一个num。

2、若k \* (5 - num) >\= diff，就说明只需要操作6和1就可以拉平差距了。这里的操作次数为(s1 - s2) / 5。当然，若(s1 - s2)不是5的倍数，就还需要一次额外的操作。使用本次的操作次数更新答案然后返回即可。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        l1 = len(nums1)
        l2 = len(nums2)
        if l1 > l2 * 6 or l2 > l1 * 6:
            return -1
        
        s1 = sum(nums1)
        s2 = sum(nums2)

        if s1 == s2:
            return 0
        
        if s1 > s2:
            ma = nums1
            mi = nums2
        else:
            mi = nums1
            ma = nums2
        
        ma_cnt = {}
        for num in ma:
            ma_cnt[num] = ma_cnt.get(num, 0) + 1
        
        mi_cnt = {}
        for num in mi:
            mi_cnt[num] = mi_cnt.get(num, 0) + 1
        
        diff = abs(s1 - s2)
        res = 0
        for num in range(5):
            cnt = ma_cnt.get(6 - num, 0) + mi_cnt.get(num + 1, 0)
            if cnt * (5 - num) < diff:
                diff -= cnt * (5 - num)
                res += cnt
            else:
                res += diff / (5 - num)
                if diff % (5 - num) != 0:
                    res += 1
                break
        
        return res
```
