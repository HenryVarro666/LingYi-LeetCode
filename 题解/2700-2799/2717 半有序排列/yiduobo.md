---
title: "2717. 半有序排列"
aliases: ["yiduobo的每日leetcode 2717.半有序排列"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/651726636"
zhihu_id: "651726636"
zhihu_title: "yiduobo的每日leetcode 2717.半有序排列"
question_id: "2717"
question: "半有序排列"
problem_url: "https://leetcode.cn/problems/semi-ordered-permutation/"
difficulty: "Easy"
created: "2023-08-23T03:09:52+08:00"
updated: "2023-08-23T03:09:52+08:00"
upvotes: 0
comments: 0
---

# 2717. 半有序排列

> **[yiduobo的每日leetcode 2717.半有序排列](https://zhuanlan.zhihu.com/p/651726636) · 知乎 · 2023-08-23 · 赞同 0**
> 力扣：[2717. 半有序排列](https://leetcode.cn/problems/semi-ordered-permutation/) · Easy · 灵茶山艾府：[分类讨论+简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2717.半有序排列

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/semi-ordered-permutation/)

题目要将数组中的1交换到数组的头部，将数组中的n交换到数组的尾部。不妨设1的初始下标为p1，n的初始下标为p2，那么将1交换到头部所需的交换次数就是p1，而将n交换到尾部所需的交换次数就是n - p2 - 1，因此直观来看最终答案就是p1 + n - p2 - 1。

不过需要特别注意的是，如果p1大于p2，那么1和n之间就必然会产生一次交换，而这次交换同时被计算在了p1和n - p2 - 1当中，因此对于这种情况，最终答案还需要减去1。

最后附上python代码：

```python
class Solution(object):
    def semiOrderedPermutation(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        p1 = p2 = None
        for index in range(len(nums)):
            if nums[index] == 1:
                p1 = index
            if nums[index] == len(nums):
                p2 = index
        
        res = p1 + len(nums) - p2 - 1
        if p1 > p2:
            res -= 1
        return res
```
