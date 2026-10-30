---
title: "1150. 检查一个数是否在数组中占绝大多数"
aliases: ["yiduobo的每日leetcode 1150.检查一个数是否在数组中占绝大多数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/610879741"
zhihu_id: "610879741"
zhihu_title: "yiduobo的每日leetcode 1150.检查一个数是否在数组中占绝大多数"
question_id: "1150"
question: "检查一个数是否在数组中占绝大多数"
problem_url: "https://leetcode.cn/problems/check-if-a-number-is-majority-element-in-a-sorted-array/"
created: "2023-03-02T23:12:44+08:00"
updated: "2023-03-02T23:12:44+08:00"
upvotes: 0
comments: 0
---

# 1150. 检查一个数是否在数组中占绝大多数

> **[yiduobo的每日leetcode 1150.检查一个数是否在数组中占绝大多数](https://zhuanlan.zhihu.com/p/610879741) · 知乎 · 2023-03-02 · 赞同 0**
> 力扣：[1150. 检查一个数是否在数组中占绝大多数](https://leetcode.cn/problems/check-if-a-number-is-majority-element-in-a-sorted-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1150.检查一个数是否在数组中占绝大多数

[力扣](https://leetcode.cn/problems/check-if-a-number-is-majority-element-in-a-sorted-array/)

最直观的做法自然是一趟遍历，统计数组中target中出现的次数并判断其是否超过数组长度的一半，不过还存在更好的做法。注意到数组已经排好了序，那么就可以使用二分法定位到target在数组中第一次和最后一次出现的下标位置，只需通过这两个下标之差就可以得出数组中target的数量。更进一步的，在这里都不需要找出target最后一次出现的下标，只需找出其首次出现的下标left，然后判断从left往后数数组长度一半加1的下标是否依然是target就行了。

在具体实现上，由于数组中可能不存在target，那么需要将问题转化为找出数组中最小的大于等于target的数的下标。找到对应的下标left后，先判断nums[left]是否等于target，再判断nums[left + n / 2]是否也等于target。

```python
class Solution(object):
    def isMajorityElement(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: bool
        """

        if target < nums[0]:
            return False
        
        n = len(nums)
        left = 0
        right = n - 1
        while left < right:
            mid = (left + right) / 2
            if nums[mid] >= target:
                right = mid
            else:
                left = mid + 1
        
        if nums[left] != target:
            return False
        
        if left + n / 2 < len(nums) and nums[left + n / 2] == target:
            return True
        
        return False
```
