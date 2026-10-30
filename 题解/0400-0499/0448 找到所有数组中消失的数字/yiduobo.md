---
title: "448. 找到所有数组中消失的数字"
aliases: ["yiduobo的每日leetcode 448.找到所有数组中消失的数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/209039368"
zhihu_id: "209039368"
zhihu_title: "yiduobo的每日leetcode 448.找到所有数组中消失的数字"
question_id: "448"
question: "找到所有数组中消失的数字"
problem_url: "https://leetcode.cn/problems/find-all-numbers-disappeared-in-an-array/"
created: "2020-08-31T22:00:24+08:00"
updated: "2020-08-31T22:00:24+08:00"
upvotes: 0
comments: 0
---

# 448. 找到所有数组中消失的数字

> **[yiduobo的每日leetcode 448.找到所有数组中消失的数字](https://zhuanlan.zhihu.com/p/209039368) · 知乎 · 2020-08-31 · 赞同 0**
> 力扣：[448. 找到所有数组中消失的数字](https://leetcode.cn/problems/find-all-numbers-disappeared-in-an-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

448.找到所有数组中消失的数字<https://leetcode-cn.com/problems/find-all-numbers-disappeared-in-an-array/>

这题与442题一样（[yiduobo：yiduobo的每日leetcode 442.数组中重复的数据](https://zhuanlan.zhihu.com/p/205550018)），只不过442题找的是出现两次的数字，而这一题需要找到出现0次的数字，于是可以先按同样的做法调换位置，然后一趟扫描，对于第index个数，如果其不等于index + 1，那么index + 1就缺失了。

最后附上python代码：

```python
class Solution(object):
    def findDisappearedNumbers(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        for index in range(len(nums)):
            while nums[nums[index] - 1] != nums[index]:
                nums[nums[index] - 1], nums[index] = nums[index], nums[nums[index] - 1]
                
        res = []
        for index in range(len(nums)):
            if nums[index] != index + 1:
                res.append(index + 1)

        return res
```
