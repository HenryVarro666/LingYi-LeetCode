---
title: "976. 三角形的最大周长"
aliases: ["yiduobo的每日leetcode 976.三角形的最大周长"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/贪心算法", "题单/滑动窗口与双指针/三-单序列双指针", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/362768826"
zhihu_id: "362768826"
zhihu_title: "yiduobo的每日leetcode 976.三角形的最大周长"
question_id: "976"
question: "三角形的最大周长"
problem_url: "https://leetcode.cn/problems/largest-perimeter-triangle/"
difficulty: "Easy"
rating: 1341
created: "2021-04-06T22:36:46+08:00"
updated: "2021-04-06T22:36:46+08:00"
upvotes: 0
comments: 0
---

# 976. 三角形的最大周长

> **[yiduobo的每日leetcode 976.三角形的最大周长](https://zhuanlan.zhihu.com/p/362768826) · 知乎 · 2021-04-06 · 赞同 0**
> 力扣：[976. 三角形的最大周长](https://leetcode.cn/problems/largest-perimeter-triangle/) · Easy · 灵茶山艾府：[枚举最长边，附思考题（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

976.三角形的最大周长

[力扣](https://leetcode-cn.com/problems/largest-perimeter-triangle/)

形成三角形的条件是两短边之和大于长边，那么我们可以先将边按长度进行排序，然后从大到小枚举长边。为了使得周长最大，那么对于枚举到的长边，我们应该尝试使用长度仅次于长边的两条边与长边形成三角形。若可以，那么当前这三条吧形成的答案显然要大于之后继续枚举得到的答案，因此直接返回三边之和即可，否则剩余的短边更加不可能与长边形成三角形，于是我们需要继续向前枚举长边。若枚举结束，说明找不到合法的三角形，此时返回0即可。

最后附上python代码：

```python
class Solution(object):
    def largestPerimeter(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        nums = sorted(nums)

        for i in range(len(nums) - 1, 1, -1):
            if nums[i] < nums[i - 1] + nums[i - 2]:
                return nums[i] + nums[i - 1] + nums[i - 2]
        
        return 0
```
