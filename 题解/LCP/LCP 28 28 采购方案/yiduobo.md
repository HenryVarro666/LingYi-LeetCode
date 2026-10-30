---
title: "LCP 28. 采购方案"
aliases: ["yiduobo的每日leetcode LCP28.采购方案"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/573786401"
zhihu_id: "573786401"
zhihu_title: "yiduobo的每日leetcode LCP28.采购方案"
question_id: "LCP 28"
question: "采购方案"
problem_url: "https://leetcode.cn/problems/4xy4/"
created: "2022-10-15T08:37:57+08:00"
updated: "2022-10-15T08:37:57+08:00"
upvotes: 0
comments: 0
---

# LCP 28. 采购方案

> **[yiduobo的每日leetcode LCP28.采购方案](https://zhuanlan.zhihu.com/p/573786401) · 知乎 · 2022-10-15 · 赞同 0**
> 力扣：[LCP 28. 采购方案](https://leetcode.cn/problems/4xy4/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP28.采购方案

[力扣](https://leetcode.cn/problems/4xy4Wx/)

两数之和问题的变种，处理方法也一样。

将所有零件按价格从小到大进行排序，接下来枚举比较便宜的那个零件index。随着便宜零件价格的上涨，比较贵的那个零件的价格只能是越来越便宜，因此在这里利用单调性就可以在均摊O(1)的时间内找出比较贵的那个零件的最大下标p。得到p之后，(index, index + 1), (index, index + 2), ..., (index, p)这一共p - index种组合都是可行的，因此在这类应该使用p - index更新答案。

若某一时刻p \<\= index，说明找不到能与index配对的较贵的零件了，此时可以直接退出循环返回结果。

最后附上python代码：

```python
class Solution(object):
    def purchasePlans(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """

        nums.sort()
        p = len(nums) - 1
        res = 0
        mod = 10 ** 9 + 7
        for index in range(len(nums)):
            while p > index and nums[p] + nums[index] > target:
                p -= 1
            if p == index:
                break
            res += p - index
            if res >= mod:
                res -= mod
        
        return res
```
