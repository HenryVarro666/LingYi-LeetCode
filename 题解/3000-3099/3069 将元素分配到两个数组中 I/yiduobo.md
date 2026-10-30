---
title: "3069. 将元素分配到两个数组中I"
aliases: ["yiduobo的每日leetcode 3069.将元素分配到两个数组中I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/697272737"
zhihu_id: "697272737"
zhihu_title: "yiduobo的每日leetcode 3069.将元素分配到两个数组中I"
question_id: "3069"
question: "将元素分配到两个数组中 I"
problem_url: "https://leetcode.cn/problems/distribute-elements-into-two-arrays-i/"
difficulty: "Easy"
created: "2024-05-12T05:10:38+08:00"
updated: "2024-05-12T05:10:38+08:00"
upvotes: 0
comments: 0
---

# 3069. 将元素分配到两个数组中I

> **[yiduobo的每日leetcode 3069.将元素分配到两个数组中I](https://zhuanlan.zhihu.com/p/697272737) · 知乎 · 2024-05-12 · 赞同 0**
> 力扣：[3069. 将元素分配到两个数组中 I](https://leetcode.cn/problems/distribute-elements-into-two-arrays-i/) · Easy · 灵茶山艾府：[模拟（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3069.将元素分配到两个数组中I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/distribute-elements-into-two-arrays-i/description/)

题目给出的分配方案简单且固定，只需按照题目要求模拟即可。先分别初始化arr1和arr2中的元素为nums[0]和nums[1]，接下来从nums[2]开始向后遍历，每一轮对比arr1和arr2中最后这个元素的大小并将当前元素加入到对应的数组中即可。

最后附上python代码：

```python
class Solution(object):
    def resultArray(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        arr1 = [nums[0]]
        arr2 = [nums[1]]
        for v in nums[2:]:
            if arr1[-1] > arr2[-1]:
                arr1.append(v)
            else:
                arr2.append(v)
        
        return arr1 + arr2
```
