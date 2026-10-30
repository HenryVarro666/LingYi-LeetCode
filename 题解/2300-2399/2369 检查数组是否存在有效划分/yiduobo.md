---
title: "2369. 检查数组是否存在有效划分"
aliases: ["yiduobo的每日leetcode 2369.检查数组是否存在有效划分"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/五-划分型-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/563389568"
zhihu_id: "563389568"
zhihu_title: "yiduobo的每日leetcode 2369.检查数组是否存在有效划分"
question_id: "2369"
question: "检查数组是否存在有效划分"
problem_url: "https://leetcode.cn/problems/check-if-there-is-a-valid-partition-for-the-array/"
difficulty: "Medium"
rating: 1780
created: "2022-09-11T16:06:24+08:00"
updated: "2022-09-11T16:06:24+08:00"
upvotes: 0
comments: 0
---

# 2369. 检查数组是否存在有效划分

> **[yiduobo的每日leetcode 2369.检查数组是否存在有效划分](https://zhuanlan.zhihu.com/p/563389568) · 知乎 · 2022-09-11 · 赞同 0**
> 力扣：[2369. 检查数组是否存在有效划分](https://leetcode.cn/problems/check-if-there-is-a-valid-partition-for-the-array/) · Medium · 灵茶山艾府：[如何想出状态定义？（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2369.检查数组是否存在有效划分

[力扣](https://leetcode.cn/problems/check-if-there-is-a-valid-partition-for-the-array/)

经典的动态规划问题。令f[i]表示数组中前i个数是否能形成有效划分，首先初始化f[0] \= true，接下来一趟遍历，对于当前遍历到的f[i]：

1、若i >\= 2，且f[i - 2]为true，同时nums[i - 1] \= nums[i - 2]，此时就可以在f[i - 2]的基础上将nums[i - 1]与nums[i - 2]划分为一个子数组，因此f[i] \= true

2、若i >\= 3，且f[i - 3]为true，同时nums[i - 1] \= nums[i - 2] \= nums[i - 3]，或者nums[i - 1] \= nums[i - 2] + 1 \= nums[i - 3] + 2，此时就可以在f[i - 3]的基础上将nums[i - 1]、nums[i - 2]以及nums[i - 3]划分为一个子数组，因此f[i] \= true

其他情况下，都是f[i] \= false

全部遍历完成后，f[-1]就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def validPartition(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        f = [True]
        for index in range(1, len(nums) + 1):
            f.append(False)
            if index >= 2 and f[index - 2] and nums[index - 1] == nums[index - 2]:
                f[index] = True
            elif index >= 3 and f[index - 3] and ((nums[index - 1] == nums[index - 2] == nums[index - 3]) or (nums[index - 1] == nums[index - 2] + 1 == nums[index - 3] + 2)):
                f[index] = True
        
        return f[-1]
```
