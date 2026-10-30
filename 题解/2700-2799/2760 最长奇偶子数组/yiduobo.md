---
title: "2760. 最长奇偶子数组"
aliases: ["yiduobo的每日leetcode 2760.最长奇偶子数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/enumeration", "leetcode/bian-li", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/654540286"
zhihu_id: "654540286"
zhihu_title: "yiduobo的每日leetcode 2760.最长奇偶子数组"
question_id: "2760"
question: "最长奇偶子数组"
problem_url: "https://leetcode.cn/problems/longest-even-odd-subarray-with-threshold/"
difficulty: "Easy"
rating: 1420
created: "2023-09-06T03:09:51+08:00"
updated: "2023-09-06T03:09:51+08:00"
upvotes: 0
comments: 0
---

# 2760. 最长奇偶子数组

> **[yiduobo的每日leetcode 2760.最长奇偶子数组](https://zhuanlan.zhihu.com/p/654540286) · 知乎 · 2023-09-06 · 赞同 0**
> 力扣：[2760. 最长奇偶子数组](https://leetcode.cn/problems/longest-even-odd-subarray-with-threshold/) · Easy · 灵茶山艾府：[教你一次性把代码写对！O(n) 分组循环（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2760.最长奇偶子数组

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/longest-even-odd-subarray-with-threshold/)

题目的数据规模很小，完全可以直接枚举子数组的起点和终点，然后遍历子数组检测其是否合法。

我在这这里采用的方法是先找出数组中第一个大小不超过threshold的偶数，记这个下标为left，那么nums[left]就可以作为一个合法子数组的开头。

接下来从left + 1开始寻找这个子数组最大能扩展的右边界right，条件是nums[right]大小不超过threshold，同时nums[right]与nums[right - 1]之和必须为奇数，这里和为奇数能保证子数组中的数奇偶交替。找到最大的right后，使用right减left更新答案，然后从right开始，重复上述过程来寻找下一个合法子数组，直到left来到数组末尾为止。

最后附上python代码：

```python
class Solution(object):
    def longestAlternatingSubarray(self, nums, threshold):
        """
        :type nums: List[int]
        :type threshold: int
        :rtype: int
        """

        left = 0
        res = 0
        while left < len(nums):
            while left < len(nums) and (nums[left] > threshold or nums[left] % 2 == 1):
                left += 1
        
            if left == len(nums):
                return res
        
            right = left + 1
            while right < len(nums) and nums[right] <= threshold and (nums[right - 1] + nums[right]) % 2 == 1:
                right += 1

            res = max(res, right - left)
            left = right
        
        return res
```
