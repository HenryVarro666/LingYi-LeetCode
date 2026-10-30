---
title: "2905. 找出满足差值条件的下标II"
aliases: ["yiduobo的每日leetcode 2905.找出满足差值条件的下标II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/two-pointers", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/663896108"
zhihu_id: "663896108"
zhihu_title: "yiduobo的每日leetcode 2905.找出满足差值条件的下标II"
question_id: "2905"
question: "找出满足差值条件的下标 II"
problem_url: "https://leetcode.cn/problems/find-indices-with-index-and-value-difference-ii/"
difficulty: "Medium"
rating: 1764
created: "2023-10-29T00:10:10+08:00"
updated: "2023-10-29T00:10:10+08:00"
upvotes: 0
comments: 0
---

# 2905. 找出满足差值条件的下标II

> **[yiduobo的每日leetcode 2905.找出满足差值条件的下标II](https://zhuanlan.zhihu.com/p/663896108) · 知乎 · 2023-10-29 · 赞同 0**
> 力扣：[2905. 找出满足差值条件的下标 II](https://leetcode.cn/problems/find-indices-with-index-and-value-difference-ii/) · Medium · 灵茶山艾府：[O(n) 做法：双指针+维护最大最小（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2905.找出满足差值条件的下标II

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/find-indices-with-index-and-value-difference-ii/)

之前2903题的加强版，由于数据规模的增大，在这里不能再使用O(n^2)的暴力算法，必须想办法优化。

观察题目的两个条件，可以发现实际上就是对于数组中的每个下标j，是否存在下标在0到j - indexDifference之间的i满足abs(nums[i] - nums[j]) >\= valueDifference。对于后面这个绝对值之差，则只需检测两种情况，即0到j - indexDifference中的最大值减去nums[j]，以及nums[j]减去0到indexDifference中的最小值。

换言之，在这里只需从indexDifference开始向后遍历下标j，同时使用两个变量ma和mi分别记录前缀0到j - indexDifference中的最大值和最小值下标。接下来对于当前遍历到的j，通过nums[j - indexDifference]与nums[ma]以及nums[mi]的大小关系更新ma和mi，若此时的nums[ma] - nums[j]或者nums[j] - nums[mi]大于等于valueDifference，说明[ma, j]或者[mi, j]即为一组可行解。

若遍历完数组任然没找到可行的解，那么返回[-1, -1]作为答案。

最后附上python代码：

```python
class Solution(object):
    def findIndices(self, nums, indexDifference, valueDifference):
        """
        :type nums: List[int]
        :type indexDifference: int
        :type valueDifference: int
        :rtype: List[int]
        """

        ma = mi = None
        for index, v in enumerate(nums[indexDifference:]):
            if ma is None or nums[ma] < nums[index]:
                ma = index
            if mi is None or nums[mi] > nums[index]:
                mi = index
            
            if nums[ma] - v >= valueDifference:
                return [ma, index + indexDifference]
            if v - nums[mi] >= valueDifference:
                return [mi, index + indexDifference]
        
        return [-1, -1]
```
