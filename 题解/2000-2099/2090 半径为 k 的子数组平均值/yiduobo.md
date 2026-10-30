---
title: "2090. 半径为k的子数组平均值"
aliases: ["yiduobo的每日leetcode 2090.半径为k的子数组平均值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/519394750"
zhihu_id: "519394750"
zhihu_title: "yiduobo的每日leetcode 2090.半径为k的子数组平均值"
question_id: "2090"
question: "半径为 k 的子数组平均值"
problem_url: "https://leetcode.cn/problems/k-radius-subarray-averages/"
difficulty: "Medium"
rating: 1358
created: "2022-05-24T21:23:02+08:00"
updated: "2022-05-24T21:23:02+08:00"
upvotes: 0
comments: 0
---

# 2090. 半径为k的子数组平均值

> **[yiduobo的每日leetcode 2090.半径为k的子数组平均值](https://zhuanlan.zhihu.com/p/519394750) · 知乎 · 2022-05-24 · 赞同 0**
> 力扣：[2090. 半径为 k 的子数组平均值](https://leetcode.cn/problems/k-radius-subarray-averages/) · Medium · 灵茶山艾府：[O(n) 定长滑动窗口（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2090.半径为k的子数组平均值

[力扣](https://leetcode.cn/problems/k-radius-subarray-averages/)

非常标准的定长滑动窗口问题，在这里可以记录窗口的首尾位置，也可以通过窗口的中心位置来计算首尾位置。

我在这里采用的是记录窗口中心位置的做法。需要注意的是，题目不需要长度不足的窗口，因此在枚举窗口中心时的左右边界应该是k和n - k - 1。这里有一种特殊情况是原数组的长度不足k + k + 1，这样的话就得不到一个完整的窗口，此时全部返回-1即可。

接下来考虑一般情况。首先需要初始化窗口内元素和为sum(nums[:k + k + 1])，接下来从k + 1开始向后枚举窗口中心。当窗口中心从index - 1移动到index时，右侧元素nums[index + k]将被纳入到窗口中，而左侧元素nums[index - k - 1]则将被移出窗口，因此需要使用这两个值来更新窗口内元素和，同时更新窗口中心为index时对应的答案。

最后附上python代码：

```python
class Solution(object):
    def getAverages(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """

        n = len(nums)
        res = [-1] * n
        if k + k + 1 > n:
            return res
        
        now = sum(nums[:k + k + 1])
        res[k] = now / (k + k + 1)
        for index in range(k + 1, n - k):
            now += nums[index + k] - nums[index - k - 1]
            res[index] = now / (k + k + 1)
        
        return res
```
