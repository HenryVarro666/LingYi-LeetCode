---
title: "477. 汉明距离总和"
aliases: ["yiduobo的每日leetcode 477.汉明距离总和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/240798723"
zhihu_id: "240798723"
zhihu_title: "yiduobo的每日leetcode 477.汉明距离总和"
question_id: "477"
question: "汉明距离总和"
problem_url: "https://leetcode.cn/problems/total-hamming-distance/"
created: "2020-09-13T22:12:04+08:00"
updated: "2020-09-13T22:12:04+08:00"
upvotes: 0
comments: 0
---

# 477. 汉明距离总和

> **[yiduobo的每日leetcode 477.汉明距离总和](https://zhuanlan.zhihu.com/p/240798723) · 知乎 · 2020-09-13 · 赞同 0**
> 力扣：[477. 汉明距离总和](https://leetcode.cn/problems/total-hamming-distance/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

477.汉明距离总和<https://leetcode-cn.com/problems/total-hamming-distance/>

这里需要求所有数两两之间汉明距离之和，但是这样做的复杂度就是O(n^2 \* log(maxnum))了。注意到汉明距离是按位计算的，不同位之间互不干扰，那么可以想办法按位计算出所有数在某一位上的汉明距离之和。

具体来说就是按位统计该位上1的个数cnt，那么该位上0的个数就是n - cnt。对于这一位而言，其中的所有0和1都需要两两进行一次比较，而0和0之间、1和1之间的比较不会影响最终的答案，因此只需要统计0和1比较的次数，而这个次数就是cnt \* (n - cnt)。

于是现在的做法就是按位统计所有数在该位上1的个数之和，然后通过上面的式子逐位计算在该位上产生的汉明距离之和。

最后附上python代码：

```python
class Solution(object):
    def totalHammingDistance(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        one_cnt = {}
        for num in nums:
            tmp = num
            pos = 0
            while tmp:
                if tmp & 1:
                    one_cnt[pos] = one_cnt.get(pos, 0) + 1
                tmp >>= 1
                pos += 1
        
        res = 0
        for cnt in one_cnt.values():
            res += (len(nums) - cnt) * cnt

        return res
```
