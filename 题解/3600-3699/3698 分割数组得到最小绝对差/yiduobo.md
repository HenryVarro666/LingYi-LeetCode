---
title: "3698. 分割数组得到最小绝对差"
aliases: ["yiduobo的每日leetcode 3698.分割数组得到最小绝对差"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bian-li", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1956343968083214743"
zhihu_id: "1956343968083214743"
zhihu_title: "yiduobo的每日leetcode 3698.分割数组得到最小绝对差"
question_id: "3698"
question: "分割数组得到最小绝对差"
problem_url: "https://leetcode.cn/problems/split-array-with-minimum-difference/"
difficulty: "Medium"
rating: 1649
created: "2025-10-04T20:34:56+08:00"
updated: "2025-10-04T20:34:56+08:00"
upvotes: 1
comments: 0
---

# 3698. 分割数组得到最小绝对差

> **[yiduobo的每日leetcode 3698.分割数组得到最小绝对差](https://zhuanlan.zhihu.com/p/1956343968083214743) · 知乎 · 2025-10-04 · 赞同 1**
> 力扣：[3698. 分割数组得到最小绝对差](https://leetcode.cn/problems/split-array-with-minimum-difference/) · Medium · 灵茶山艾府：[一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3698.分割数组得到最小绝对差

[3698. 分割数组得到最小绝对差 - 力扣（LeetCode）](https://leetcode.cn/problems/split-array-with-minimum-difference/)

题目给出一个整数数组nums。现在要求将nums分割成两个非空子数组left和right，其中left必须严格递增，right必须严格递减。

问left与right的元素和之间差的绝对值的最小可能是多少。若不存在合法的分割方案，则返回-1。

对于左侧的上升子数组和右侧的下降子数组，这二者相邻的地方可能有两种情况。

第一种情况是上升子数组的最后一个元素恰好就等于下降子数组的第一个元素，对于这种情况，子数组的划分是唯一的，只需分别计算两个子数组的元素之和，相减后取绝对值即为最终答案。

第二种情况则是nums中仅存在一个唯一的最大值，这个最大值左侧是上升子数组，右侧是下降子数组，那么这个最大值应该划分到哪一边，就应该根据左右两侧之差来决定。

无论是上面哪种情况，在一开始都应该先想办法定位到这个最大值的下标。于是可以从数组头部开始向后遍历，使用一个变量p扫过所有递增的部分。如果存在合法的划分，那么nums[p]就是nums的最大值，或者两个最大值其中一个。另外，为了方便计算两个子数组差的绝对值，在这里可以使用一个变量s记录两个子数组之差，那么在上面寻找p的过程中，可以将前缀中扫过的元素都累加到s中。

接下来，则可以分为两种情况：

1、若p + 1没有越界，且nums[p]与nums[p + 1]相等，那么就遇到了上面提到的第一种情况。对于这种情况，只需要从p + 2开始向后扫，检测剩下的子数组是否递减即可。若不递减，则返回-1，否则只需在上面的过程中让s减去扫过的元素就行了，最后返回s的绝对值。

2、否则就是最大值唯一的情况。此时则需要从p + 1开始，先检测剩下的子数组是否递减。若不满足，则返回-1，否则同样是让s减去扫过的元素。

遍历完成后，还需要决定nums[p]的归属，不过需要特别注意的是，此时还有两种特殊情况，也就是nums[p]是nums的第一个元素，或者最后一个元素。

对于前面这种情况，整个nums是递减的，因此只能将第一个元素单独划做递增的子数组，将剩下的元素当做递减的子数组，也就是说这种情况下需要将nums[p]累加到s中。

后面这种情况则完全对称，此时需要将最后这个元素单独划做递减的子数组，剩下的元素当做递增的子数组，此时需要将nums[p]从s中减去。

除了这两种情况之外，nums[p]都可以加入到任意一边，此时取s + nums[p]的绝对值以及s - nums[p]的绝对值中较小的那一个即可。

最后附上python代码：

```python
class Solution(object):
    def splitArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        s = nums[0]
        p = 0
        while p + 1 < len(nums) and nums[p + 1] > nums[p]:
            p += 1
            s += nums[p]

        if p + 1 < len(nums) and nums[p + 1] == nums[p]:
            s -= nums[p + 1]
            p += 2
            while p < len(nums) and nums[p] < nums[p - 1]:
                s -= nums[p]
                p += 1
            
            if p != len(nums):
                return -1
            
            return abs(s)
        
        ma_p = p
        s -= nums[p]
        while p + 1 < len(nums) and nums[p + 1] < nums[p]:
            p += 1
            s -= nums[p]

        if p != len(nums) - 1:
            return -1
        
        if ma_p == 0:
            return abs(s + nums[ma_p])
        elif ma_p == len(nums) - 1:
            return abs(s - nums[ma_p])
        else:
            return min(abs(s + nums[ma_p]), abs(s - nums[ma_p]))
```
