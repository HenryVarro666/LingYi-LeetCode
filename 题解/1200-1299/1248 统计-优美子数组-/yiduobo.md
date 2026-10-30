---
title: "1248. 统计[优美子数组]"
aliases: ["yiduobo的每日leetcode 1248.统计[优美子数组]"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/385521094"
zhihu_id: "385521094"
zhihu_title: "yiduobo的每日leetcode 1248.统计[优美子数组]"
question_id: "1248"
question: "统计[优美子数组]"
problem_url: "https://leetcode.cn/problems/count-number-of-nice-subarrays/"
created: "2021-06-30T23:18:40+08:00"
updated: "2021-06-30T23:18:40+08:00"
upvotes: 1
comments: 0
---

# 1248. 统计[优美子数组]

> **[yiduobo的每日leetcode 1248.统计[优美子数组]](https://zhuanlan.zhihu.com/p/385521094) · 知乎 · 2021-06-30 · 赞同 1**
> 力扣：[1248. 统计[优美子数组]](https://leetcode.cn/problems/count-number-of-nice-subarrays/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1248.统计[优美子数组]

[力扣](https://leetcode-cn.com/problems/count-number-of-nice-subarrays/)

经典的滑动窗口问题。

首先设左边界l为0,，然后向后扫描寻找右边界mi_r和ma_r，二者分别表示以l为左边界的最短优美子数组的右边界以及最长优美子数组的右边界，那么以l为左边界的优美子数组就一共有ma_r - mi_r + 1个。

接下来，我们向右移动左边界l，此时若nums[l]为偶数，则无需调整mi_r和ma_r，否则我们就需要将mi_r置为ma_r + 1，然后向后扫描直到出现一个奇数，此时就得到了新的mi_r。得到mi_r之后，就需要将ma_r置为mi_r，然后向后扫描直到出现下一个奇数的位置，此时就得到了新的ma_r。重复此过程直到mi_r或者l到达n位置。

另外，本题也有另一种做法，由于题目中的偶数没有用处，奇数则需要计数，因此可以将数组按照奇偶变换成01数组，然后通过前缀和以及哈希表就能得到最终答案。

最后附上python代码：

```python
class Solution(object):
    def numberOfSubarrays(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        n = len(nums)
        res = 0
        l = 0
        mi_r = -1
        ma_r = -1
        now = 0
        while now < k and mi_r + 1 < n:
            mi_r += 1
            if nums[mi_r] % 2 == 1:
                now += 1

        if now < k:
            return 0

        while l < n and mi_r < n:
            ma_r = mi_r
            while ma_r + 1 < n and nums[ma_r + 1] % 2 == 0:
                ma_r += 1
            
            res += ma_r - mi_r + 1

            if nums[l] % 2 == 1:
                mi_r = ma_r + 1
            l += 1
        
        return res
```
