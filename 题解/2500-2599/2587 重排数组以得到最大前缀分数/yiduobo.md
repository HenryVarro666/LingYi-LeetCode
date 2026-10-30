---
title: "2587. 重排数组以得到最大前缀分数"
aliases: ["yiduobo的每日leetcode 2587.重排数组以得到最大前缀分数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/643220746"
zhihu_id: "643220746"
zhihu_title: "yiduobo的每日leetcode 2587.重排数组以得到最大前缀分数"
question_id: "2587"
question: "重排数组以得到最大前缀分数"
problem_url: "https://leetcode.cn/problems/rearrange-array-to-maximize-prefix-score/"
difficulty: "Medium"
rating: 1337
created: "2023-07-13T03:14:23+08:00"
updated: "2023-07-13T03:14:23+08:00"
upvotes: 0
comments: 0
---

# 2587. 重排数组以得到最大前缀分数

> **[yiduobo的每日leetcode 2587.重排数组以得到最大前缀分数](https://zhuanlan.zhihu.com/p/643220746) · 知乎 · 2023-07-13 · 赞同 0**
> 力扣：[2587. 重排数组以得到最大前缀分数](https://leetcode.cn/problems/rearrange-array-to-maximize-prefix-score/) · Medium · 灵茶山艾府：[排序+贪心](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2587.重排数组以得到最大前缀分数

[力扣](https://leetcode.cn/problems/rearrange-array-to-maximize-prefix-score/)

所谓的最大前缀分数实际上就是问最长的和大于0的前缀有多长，那么很明显就应该将正数全部放到数组的头部，然后将负数按从大到小的顺序排在正数的后面，然后一趟遍历计算最长的和大于0的前缀长度即可。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        now = 0
        res = 0
        for v in sorted(nums, reverse=True):
            now += v
            if now > 0:
                res += 1
            else:
                break
        
        return res
```
