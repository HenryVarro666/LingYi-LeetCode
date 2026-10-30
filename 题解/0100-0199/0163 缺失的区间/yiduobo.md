---
title: "163. 缺失的区间"
aliases: ["yiduobo的每日leetcode 163.缺失的区间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/591083400"
zhihu_id: "591083400"
zhihu_title: "yiduobo的每日leetcode 163.缺失的区间"
question_id: "163"
question: "缺失的区间"
problem_url: "https://leetcode.cn/problems/missing-ranges/"
created: "2022-12-12T00:28:43+08:00"
updated: "2022-12-12T00:28:43+08:00"
upvotes: 0
comments: 0
---

# 163. 缺失的区间

> **[yiduobo的每日leetcode 163.缺失的区间](https://zhuanlan.zhihu.com/p/591083400) · 知乎 · 2022-12-12 · 赞同 0**
> 力扣：[163. 缺失的区间](https://leetcode.cn/problems/missing-ranges/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

163.缺失的区间

[力扣](https://leetcode.cn/problems/missing-ranges/)

注意到题目中对于长度为1的区间输出的格式与其他区间不同，所以我在这里采用的是先将区间信息收集起来，然后再统一格式化输出。

首先是特殊情况，若nums数组为空，那么最终答案就是区间[lower, upper]。

接下来是nums不为空的情况。

首先需要考虑边界，若nums[0] > lower，那么lower到nums[0] - 1这一段区间是缺失的。同样的，若nums[-1] \< upper，那么nums[-1] + 1到upper同样是缺失的，不过为了保证顺序的正确，这一步需要放在最后处理。

对于nums数组中产生的缺失，则可以从下标1开始遍历nums中的数。若nums[index - 1] + 1 \< nuns[index]，那么说明区间nums[index - 1] + 1到nums[index] - 1之间是缺失的。

收集好区间信息之后，只需根据区间左右边界是否相同来决定最终的输出格式即可。

最后附上python代码：

```python
class Solution(object):
    def findMissingRanges(self, nums, lower, upper):
        """
        :type nums: List[int]
        :type lower: int
        :type upper: int
        :rtype: List[str]
        """

        if not nums:
            intervals = [[lower, upper]]
        else:      
            intervals = []
            if nums[0] > lower:
                intervals.append([lower, nums[0] - 1])
        
            for index in range(1, len(nums)):
                if nums[index] > nums[index - 1] + 1:
                    intervals.append([nums[index - 1] + 1, nums[index] - 1])
        
            if nums[-1] < upper:
                intervals.append([nums[-1] + 1, upper])

        res = []
        for x, y in intervals:
            if x == y:
                res.append(str(x))
            else:
                res.append(str(x) + '->' + str(y))
        
        return res
```
