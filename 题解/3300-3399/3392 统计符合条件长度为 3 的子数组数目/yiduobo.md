---
title: "3392. 统计符合条件长度为3的子数组数目"
aliases: ["yiduobo的每日leetcode 3392.统计符合条件长度为3的子数组数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/30351097935"
zhihu_id: "30351097935"
zhihu_title: "yiduobo的每日leetcode 3392.统计符合条件长度为3的子数组数目"
question_id: "3392"
question: "统计符合条件长度为 3 的子数组数目"
problem_url: "https://leetcode.cn/problems/count-subarrays-of-length-three-with-a-condition/"
difficulty: "Easy"
created: "2025-03-15T00:56:25+08:00"
updated: "2025-03-15T00:56:25+08:00"
upvotes: 1
comments: 0
---

# 3392. 统计符合条件长度为3的子数组数目

> **[yiduobo的每日leetcode 3392.统计符合条件长度为3的子数组数目](https://zhuanlan.zhihu.com/p/30351097935) · 知乎 · 2025-03-15 · 赞同 1**
> 力扣：[3392. 统计符合条件长度为 3 的子数组数目](https://leetcode.cn/problems/count-subarrays-of-length-three-with-a-condition/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3392.统计符合条件长度为3的子数组数目

[3392. 统计符合条件长度为 3 的子数组数目 - 力扣（LeetCode）](https://leetcode.cn/problems/count-subarrays-of-length-three-with-a-condition/description/)

题目给出一个整数数组nums，问其中包含有多少个长度为3，且第一个元素和第三个元素之和恰好是第二个元素一半的子数组。

直接从下标2开始向后遍历子数组中的第三个元素，对于当前遍历到的下标index，检测nums[index]与nums[index - 2]之和的两倍是否恰好等于nums[index - 1]即可。

最后附上python代码：

```python
class Solution(object):
    def countSubarrays(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = 0
        for index in range(2, len(nums)):
            if (nums[index] + nums[index - 2]) * 2 == nums[index - 1]:
                res += 1
                
        return res
```
