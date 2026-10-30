---
title: "2831. 找出最长等值子数组"
aliases: ["yiduobo的每日leetcode 2831.找出最长等值子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659277658"
zhihu_id: "659277658"
zhihu_title: "yiduobo的每日leetcode 2831.找出最长等值子数组"
question_id: "2831"
question: "找出最长等值子数组"
problem_url: "https://leetcode.cn/problems/find-the-longest-equal-subarray/"
difficulty: "Medium"
rating: 1976
created: "2023-10-02T02:07:11+08:00"
updated: "2023-10-02T02:07:11+08:00"
upvotes: 0
comments: 0
---

# 2831. 找出最长等值子数组

> **[yiduobo的每日leetcode 2831.找出最长等值子数组](https://zhuanlan.zhihu.com/p/659277658) · 知乎 · 2023-10-02 · 赞同 0**
> 力扣：[2831. 找出最长等值子数组](https://leetcode.cn/problems/find-the-longest-equal-subarray/) · Medium · 灵茶山艾府：[分组+滑动窗口（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2831.找出最长等值子数组

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/find-the-longest-equal-subarray/description/)

经典的变长滑动窗口的题目，一般有两种做法。第一种是直接滑，动态统计窗口内出现频率最高的数并根据窗口长度以及这个数出现的次数与k的大小来修正窗口的边界。第二种做法则是先分别统计出每种数字出现的位置列表，然后计算当最终子数组中只留下这种数字时可以得到的最长子数组的长度是多少。

我在这里采用的是第二种做法。首先使用一个哈希pos_dict统计每种数字出现的位置列表，接下来遍历每种数组v，那么对于pos_dict[v]，再使用变长滑动窗口找出其中每个左边界left对应的最大右边界right，要求满足(pos_dict[v][right - 1] - pos_dict[v][left] + 1) - (right - left) \<\= k，这里面的两个括号分别是子数组中数字的个数以及子数组中v的个数，那么二者相减就是需要删除的元素数量，这个值必须小于等于k。另一方面，随着left的向后移动，right也必然跟着向后移动，因此这里找right的复杂度实际上是均摊O(1)的。对于每个left找到right后，使用right - left更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def longestEqualSubarray(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        pos_dict = {}
        for index, v in enumerate(nums):
            if v not in pos_dict:
                pos_dict[v] = []
            pos_dict[v].append(index)
        
        res = 0
        for v in pos_dict:
            pos_list = pos_dict[v]
            left = 0
            right = 0
            while left < len(pos_list):
                if right < left:
                    right = left
                
                while right < len(pos_list) and pos_list[right] - pos_list[left] + 1 - (right - left + 1) <= k:
                    right += 1
                
                res = max(res, right - left)
                left += 1
        
        return res
```
