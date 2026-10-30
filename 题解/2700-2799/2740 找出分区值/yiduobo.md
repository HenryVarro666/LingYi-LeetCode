---
title: "2740. 找出分区值"
aliases: ["yiduobo的每日leetcode 2740.找出分区值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/八-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/653175569"
zhihu_id: "653175569"
zhihu_title: "yiduobo的每日leetcode 2740.找出分区值"
question_id: "2740"
question: "找出分区值"
problem_url: "https://leetcode.cn/problems/find-the-value-of-the-partition/"
difficulty: "Medium"
rating: 1302
created: "2023-08-30T02:37:06+08:00"
updated: "2023-08-30T02:37:06+08:00"
upvotes: 0
comments: 0
---

# 2740. 找出分区值

> **[yiduobo的每日leetcode 2740.找出分区值](https://zhuanlan.zhihu.com/p/653175569) · 知乎 · 2023-08-30 · 赞同 0**
> 力扣：[2740. 找出分区值](https://leetcode.cn/problems/find-the-value-of-the-partition/) · Medium · 灵茶山艾府：[贪心（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2740.找出分区值

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/find-the-value-of-the-partition/description/)

首先可以明确的是，最终答案中的max(nums1)和min(nums2)之间必然是不存在其他数的。

对于max(nums1) \< min(nums2)这种情况，若原数组中存在某个整数v满足max(nums1) \< v \< min(nums2)，那么v如果属于nums1，此时的max(nums1)就应该是v而不是小于v，同样的v也不能属于nums2。

反过来，若max(nums1) > min(nums2)，若原数组中存在某个整数满足max(nums1) > v > min(nums2)，那么就可以将num1中所有大于v的数都移动到num2中，然后将v移动到num1中，此时的max(nums1)就是v，而min(nums2)不变，此时的分区值显然是更优的。

综合上面两种情况，就得到了结论，最终用来计算分区值的两个数的大小在原数组中必然是相邻的，那么在这里就得到了一种很方便的构造方法。将原数组排序，然后一趟遍历，将数组划分成左右两个部分并计算当前分区值然后更新答案就行了。

最后附上python代码：

```python
class Solution(object):
    def findValueOfPartition(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        nums.sort()
        res = None
        for index in range(1, len(nums)):
            if res is None or res > nums[index] - nums[index - 1]:
                res = nums[index] - nums[index - 1]
        
        return res
```
