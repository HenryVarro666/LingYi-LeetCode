---
title: "2036. 最大交替子数组和"
aliases: ["yiduobo的每日leetcode 2036.最大交替子数组和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/625511396"
zhihu_id: "625511396"
zhihu_title: "yiduobo的每日leetcode 2036.最大交替子数组和"
question_id: "2036"
question: "最大交替子数组和"
problem_url: "https://leetcode.cn/problems/maximum-alternating-subarray-sum/"
created: "2023-04-28T00:53:40+08:00"
updated: "2023-04-28T00:53:40+08:00"
upvotes: 1
comments: 0
---

# 2036. 最大交替子数组和

> **[yiduobo的每日leetcode 2036.最大交替子数组和](https://zhuanlan.zhihu.com/p/625511396) · 知乎 · 2023-04-28 · 赞同 1**
> 力扣：[2036. 最大交替子数组和](https://leetcode.cn/problems/maximum-alternating-subarray-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

2036.最大交替子数组和

[力扣](https://leetcode.cn/problems/maximum-alternating-subarray-sum/)

最大子段和问题的升级版，可以使用动态规划来进行求解。令f[i]表示以nums[i]结尾的最大的以加号项结尾的子段和，g[i]则表示以nums[i]结尾的最大的以减号项结尾的子段和，接下来一趟遍历，对于f[i]和g[i]：

1、首先是边界情况。有f[0] \= nums[0]，而g[0]只能为空，因为g[0]之前没有可用的正好项

2、接下来对于i > 0的情况：

对于f[i]，若g[i - 1]为空，那么就有f[i] \= nums[i]，否则就有f[i] \= g[i - 1] + nums[i]

对于g[i]，f[i - 1]是必须要存在的，那么就有g[i] \= f[i - 1] + nums[i]。此时若g[i] \< 0，则可以将g[i]置为空，表示放弃g[i]这一段子段和

最终答案就是f[i]和非空的g[i]中的最大值

最后附上python代码：

```python
class Solution(object):
    def maximumAlternatingSubarraySum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        
        res = f = nums[0]
        g = None
        for v in nums[1:]:
            last_f = f
            if g is None:
                f = v
            else:
                f = g + v
            
            if last_f - v < 0:
                g = None
            else:
                g = last_f - v
            
            res = max(res, f)
            if g is not None:
                res = max(res, g)
        
        return res
```
