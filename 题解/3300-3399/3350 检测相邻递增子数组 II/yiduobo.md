---
title: "3349. 检测相邻递增子数组I & 3350. 检测相邻递增子数组II"
aliases: ["yiduobo的每日leetcode 3349.检测相邻递增子数组I && 3350.检测相邻递增子数组II", "3349. 检测相邻递增子数组I", "3350. 检测相邻递增子数组II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li", "leetcode/medium", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/26113097834"
zhihu_id: "26113097834"
zhihu_title: "yiduobo的每日leetcode 3349.检测相邻递增子数组I && 3350.检测相邻递增子数组II"
question_id: ["3349", "3350"]
question: ["检测相邻递增子数组 I", "检测相邻递增子数组 II"]
problem_url: ["https://leetcode.cn/problems/adjacent-increasing-subarrays-detection-i/", "https://leetcode.cn/problems/adjacent-increasing-subarrays-detection-ii/"]
difficulty: ["Easy", "Medium"]
rating: 1600
created: "2025-02-24T22:47:49+08:00"
updated: "2025-02-24T22:47:49+08:00"
upvotes: 1
comments: 0
---

# 3349. 检测相邻递增子数组I & 3350. 检测相邻递增子数组II

> **[yiduobo的每日leetcode 3349.检测相邻递增子数组I && 3350.检测相邻递增子数组II](https://zhuanlan.zhihu.com/p/26113097834) · 知乎 · 2025-02-24 · 赞同 1**
> 力扣：[3349. 检测相邻递增子数组 I](https://leetcode.cn/problems/adjacent-increasing-subarrays-detection-i/) · Easy · 灵茶山艾府：[O(n) 一次遍历（Python/Java/C++/C/Go/JS/Rust）](../3349%20检测相邻递增子数组%20I/灵茶山艾府.md)
> 力扣：[3350. 检测相邻递增子数组 II](https://leetcode.cn/problems/adjacent-increasing-subarrays-detection-ii/) · Medium · 灵茶山艾府：[O(n) 一次遍历，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3349.检测相邻递增子数组I

[3349. 检测相邻递增子数组 I - 力扣（LeetCode）](https://leetcode.cn/problems/adjacent-increasing-subarrays-detection-i/description/)

3350.检测相邻递增子数组II

[3350. 检测相邻递增子数组 II - 力扣（LeetCode）](https://leetcode.cn/problems/adjacent-increasing-subarrays-detection-ii/description/)

题目给出一个数组nums，另外定义相邻递增子数组为两个相邻且长度都为k的子数组，其中nums[a]到nums[a + k - 1]和nums[b]到nums[b + k - 1]都是严格递增的，且b \= a + k。

3349题问的是给出指定的k，问nums中是否存在这样的子数组。3350题则是问最大可能的k是多少。

实际上只需要知道3350题中最大可能的k是多少，对比3349题中指定的k就可以得到3349题的答案，因此在这里先将问题统一成最大可能的k是多少。

可以明确的是，相邻严格递增子数组可以分为两种情况，分别是：

1、样例1中类似[7, 8, 9, 2, 3, 4]这样，前半段的最后一个元素大于等于后半段的第一个元素，即这个相邻递增子数组是由左侧的递增子数组的后缀，以及右侧的递增子数组的前缀构成

2、样例2中类似[1, 2, 3, 4]这样，前半段的最后一个元素小于后半段的第一个元素，即这个相邻递增子数组是由一个递增子数组从中间劈开得到的

于是可以一趟遍历，将数组分离成若干个尽量长的递增子数组，而最大的k要么是两个相邻的递增子数组中长度的较小值，要么是某个递增子数组长度的一半。

最后附上3350题的python代码：

```python
class Solution(object):
    def maxIncreasingSubarrays(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = 0
        pre_len = 0
        pre = nums[0]
        now_len = 1
        for v in nums[1:]:
            if v > pre:
                now_len += 1
            else:
                res = max(res, now_len // 2, min(pre_len, now_len))
                pre_len = now_len
                now_len = 1
            
            pre = v
        
        res = max(res, now_len // 2, min(pre_len, now_len))
        return res
```
