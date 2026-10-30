---
title: "80. 删除排序数组中的重复项II"
aliases: ["yiduobo的每日leetcode 80.删除排序数组中的重复项II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/面试经典-150-题", "题单/滑动窗口与双指针/三-单序列双指针", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/134168297"
zhihu_id: "134168297"
zhihu_title: "yiduobo的每日leetcode 80.删除排序数组中的重复项II"
question_id: "80"
question: "删除有序数组中的重复项 II"
problem_url: "https://leetcode.cn/problems/remove-duplicates-from-sorted-array-ii/"
difficulty: "Medium"
created: "2020-04-21T23:14:18+08:00"
updated: "2020-04-21T23:14:18+08:00"
upvotes: 1
comments: 0
---

# 80. 删除排序数组中的重复项II

> **[yiduobo的每日leetcode 80.删除排序数组中的重复项II](https://zhuanlan.zhihu.com/p/134168297) · 知乎 · 2020-04-21 · 赞同 1**
> 力扣：[80. 删除有序数组中的重复项 II](https://leetcode.cn/problems/remove-duplicates-from-sorted-array-ii/) · Medium · 灵茶山艾府：[用栈思考，原地实现（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

80.删除排序数组中的重复项II <https://leetcode-cn.com/problems/remove-duplicates-from-sorted-array-ii/>

比较基础的题目。由于题目要求每个数最多保留两次，那么我们从左往右扫描，当遇到nums[k] \=\= ans[-1]时，判断ans中是否已经有两个nums[k]了。如果有，那么就跳过nums[k]，否则将nums[k]加入到ans中，需要注意此时ans[-1]与ans[-2]的值都是nums[k]，因此nums[k + 1]以及之后值等于nums[k]的数都不能再加入ans了，我在这里设置了一个second_flag标记来表示这个状态。

另外，题目要求原地修改，答案数组的长度一定是严格小于等于nums的，因此可以直接将答案数组从头部开始覆盖到nums上，但是需要注意这里就需要维护一个pos，表示ans的长度，而不能用ans[-1]与作比较了。

最后附上python代码：

```python
class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        second_flag = False
        pos = 0
        for index in range(1, len(nums)):
            if nums[index] == nums[pos]:
                if second_flag:
                    continue
                second_flag = True
            else:
                second_flag = False
            
            pos += 1
            nums[pos] = nums[index]

        return pos + 1
```
