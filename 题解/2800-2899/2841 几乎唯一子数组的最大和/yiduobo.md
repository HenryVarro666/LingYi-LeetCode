---
title: "2841. 几乎唯一子数组的最大和"
aliases: ["yiduobo的每日leetcode 2841.几乎唯一子数组的最大和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659796536"
zhihu_id: "659796536"
zhihu_title: "yiduobo的每日leetcode 2841.几乎唯一子数组的最大和"
question_id: "2841"
question: "几乎唯一子数组的最大和"
problem_url: "https://leetcode.cn/problems/maximum-sum-of-almost-unique-subarray/"
difficulty: "Medium"
rating: 1546
created: "2023-10-06T23:26:23+08:00"
updated: "2023-10-06T23:26:23+08:00"
upvotes: 0
comments: 0
---

# 2841. 几乎唯一子数组的最大和

> **[yiduobo的每日leetcode 2841.几乎唯一子数组的最大和](https://zhuanlan.zhihu.com/p/659796536) · 知乎 · 2023-10-06 · 赞同 0**
> 力扣：[2841. 几乎唯一子数组的最大和](https://leetcode.cn/problems/maximum-sum-of-almost-unique-subarray/) · Medium · 灵茶山艾府：[定长滑动窗口（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2841.几乎唯一子数组的最大和

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-sum-of-almost-unique-subarray/)

非常标准的滑动窗口问题。使用一个长度为k的窗口从左向右滑动，并利用哈希表cnt记录窗口中每种数字出现的次数，另外还需要一个变量s记录窗口内数字之和。

当窗口向右滑动时，首先将右边界对应的数字在cnt中出现的次数加上1，并将其累加到s中，然后将左边界对应的数字从s中减去，并将其在cnt中出现的次数减去1。若这个数字出现次数变为了0，就将其弹出哈希表。

若哈希表的长度大于等于m，说明窗口内至少有m种不同的数字，此时应该用s更新答案。

最后附上python代码：

```python
class Solution(object):
    def maxSum(self, nums, m, k):
        """
        :type nums: List[int]
        :type m: int
        :type k: int
        :rtype: int
        """

        cnt = {}
        s = 0
        for v in nums[:k]:
            cnt[v] = cnt.get(v, 0) + 1
            s += v
        
        if len(cnt) >= m:
            res = s
        else:
            res = 0
        
        for index, v in enumerate(nums[k:]):
            cnt[v] = cnt.get(v, 0) + 1
            cnt[nums[index]] -= 1
            if cnt[nums[index]] == 0:
                cnt.pop(nums[index])
            
            s += v
            s -= nums[index]
            if len(cnt) >= m:
                res = max(res, s)
        
        return res
```
