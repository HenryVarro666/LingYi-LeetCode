---
title: "26. 删除排序数组中的重复项"
aliases: ["yiduobo的每日leetcode 26.删除排序数组中的重复项"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "leetcode/api", "题单/滑动窗口与双指针", "题单/面试经典-150-题", "题单/滑动窗口与双指针/三-单序列双指针", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/116901219"
zhihu_id: "116901219"
zhihu_title: "yiduobo的每日leetcode 26.删除排序数组中的重复项"
question_id: "26"
question: "删除有序数组中的重复项"
problem_url: "https://leetcode.cn/problems/remove-duplicates-from-sorted-array/"
difficulty: "Easy"
created: "2020-03-25T22:54:26+08:00"
updated: "2020-03-26T22:57:21+08:00"
upvotes: 0
comments: 0
---

# 26. 删除排序数组中的重复项

> **[yiduobo的每日leetcode 26.删除排序数组中的重复项](https://zhuanlan.zhihu.com/p/116901219) · 知乎 · 2020-03-25 · 赞同 0**
> 力扣：[26. 删除有序数组中的重复项](https://leetcode.cn/problems/remove-duplicates-from-sorted-array/) · Easy · 灵茶山艾府：[跟着我过一遍示例 2，你就明白怎么做了（附库函数写法）Python/Java/C++/C/Go/JS/Rust](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

26.删除排序数组中的重复项<https://leetcode-cn.com/problems/remove-duplicates-from-sorted-array/>

不知道怎么形容的题目。

首先可以确定的是，答案的第一个数一定是nums[0]。接下来处理nums[1]到nums[n - 1]。

假如题目表示可以另起一个数组res，那么依次判断现在的nums[index]是否等于res[-1]，如果不等于则将其加入res即可。

实际上，len(res)一定是小于index + 1的。因为当我们处理到index时，即使nums[0]到nums[index - 1]都是不一样的数，此时的res中也只有index个数，而当前是nums中的第index + 1个数，因此满足len(res) \< index + 1。换言之，当我们操作到nums[index]时，nums[0]到nums[index - 1]即使都改动了也不会产生什么影响。因此我们直接用nums来表示res。维护res的长度now，每次判断nums[index]是否等于nums[now]，如果不等于则将其加入到res即可。

最后附上python代码：

```python
class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        if not nums:
            return 0

        now = 0
        for index in range(1, len(nums)):
            if nums[now] != nums[index]:
                now += 1
                nums[now] = nums[index]

        return now + 1
```
