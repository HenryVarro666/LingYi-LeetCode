---
title: "1608. 特殊数组的特征值"
aliases: ["yiduobo的每日leetcode 1608.特殊数组的特征值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/434126131"
zhihu_id: "434126131"
zhihu_title: "yiduobo的每日leetcode 1608.特殊数组的特征值"
question_id: "1608"
question: "特殊数组的特征值"
problem_url: "https://leetcode.cn/problems/special-array-with-x-elements-greater-than-or-equal-x/"
created: "2021-11-17T00:09:36+08:00"
updated: "2021-11-17T00:09:36+08:00"
upvotes: 0
comments: 0
---

# 1608. 特殊数组的特征值

> **[yiduobo的每日leetcode 1608.特殊数组的特征值](https://zhuanlan.zhihu.com/p/434126131) · 知乎 · 2021-11-17 · 赞同 0**
> 力扣：[1608. 特殊数组的特征值](https://leetcode.cn/problems/special-array-with-x-elements-greater-than-or-equal-x/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1608.特殊数组的特征值

[力扣](https://leetcode-cn.com/problems/special-array-with-x-elements-greater-than-or-equal-x/)

如果将数据规模放大一点的话，可能是一道不错的数据结构题，不过这里数据规模很小，我直接采用的暴力算法，先将nums从大到小进行排序，然后从1000开始向下枚举答案res，并判断当前数据中有多少数大于等于res。

最后附上python代码：

```python
class Solution(object):
    def specialArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        nums = sorted(nums, reverse = True)
        now = 0
        cnt = 0
        for res in range(1000, -1, -1):
            while now < len(nums) and nums[now] >= res:
                cnt += 1
                now += 1

            if res == cnt:
                return res
        
        return -1
```
