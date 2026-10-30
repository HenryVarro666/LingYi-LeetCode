---
title: "280. 摆动排序"
aliases: ["yiduobo的每日leetcode 280.摆动排序"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/594296327"
zhihu_id: "594296327"
zhihu_title: "yiduobo的每日leetcode 280.摆动排序"
question_id: "280"
question: "摆动排序"
problem_url: "https://leetcode.cn/problems/wiggle-sort/"
created: "2022-12-26T01:39:50+08:00"
updated: "2022-12-26T01:39:50+08:00"
upvotes: 0
comments: 0
---

# 280. 摆动排序

> **[yiduobo的每日leetcode 280.摆动排序](https://zhuanlan.zhihu.com/p/594296327) · 知乎 · 2022-12-26 · 赞同 0**
> 力扣：[280. 摆动排序](https://leetcode.cn/problems/wiggle-sort/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

280.摆动排序

[力扣](https://leetcode.cn/problems/wiggle-sort/)

最直观的做法自然是将数组排序，然后将将较大的一半填充到奇数下标内，将较小的一半填充到偶数下标内，不过还存在更好的做法。

当前的nums[index]以及nums[index - 1]，如果这二者不符合题目的要求，那么将二者交换位置就能符合题目要求了，因此nums[index - 1]与nums[index - 2]的大小关系和nums[index - 1]与nums[index]的大小关系是完全一致的，当交换发生时，新的nums[index - 1]并不会破坏之前nums[index - 1]与nums[index - 2]的大小关系。更严谨的证明可以采用数学归纳法，在这里就不展开了。

根据这个结论，就可以一趟遍历，使用一个标记变量flag记录当前数组末尾元素的大小关系。每一轮都根据当前的flag以及已有的大小关系选择是否进行交换，并将flag置反。

最后附上python代码：

```python
class Solution(object):
    def wiggleSort(self, nums):
        """
        :type nums: List[int]
        :rtype: None Do not return anything, modify nums in-place instead.
        """

        flag = True
        for index in range(1, len(nums)):
            if flag:
                if nums[index] < nums[index - 1]:
                    nums[index], nums[index - 1] = nums[index - 1], nums[index]
            else:
                if nums[index] > nums[index - 1]:
                    nums[index], nums[index - 1] = nums[index - 1], nums[index]
            
            flag = not flag
```
