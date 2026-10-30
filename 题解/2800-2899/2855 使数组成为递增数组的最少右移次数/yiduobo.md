---
title: "2855. 使数组成为递增数组的最少右移次数"
aliases: ["yiduobo的每日leetcode 2855.使数组成为递增数组的最少右移次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/661022577"
zhihu_id: "661022577"
zhihu_title: "yiduobo的每日leetcode 2855.使数组成为递增数组的最少右移次数"
question_id: "2855"
question: "使数组成为递增数组的最少右移次数"
problem_url: "https://leetcode.cn/problems/minimum-right-shifts-to-sort-the-array/"
difficulty: "Easy"
created: "2023-10-13T00:24:52+08:00"
updated: "2023-10-13T00:24:52+08:00"
upvotes: 0
comments: 0
---

# 2855. 使数组成为递增数组的最少右移次数

> **[yiduobo的每日leetcode 2855.使数组成为递增数组的最少右移次数](https://zhuanlan.zhihu.com/p/661022577) · 知乎 · 2023-10-13 · 赞同 0**
> 力扣：[2855. 使数组成为递增数组的最少右移次数](https://leetcode.cn/problems/minimum-right-shifts-to-sort-the-array/) · Easy · 灵茶山艾府：[从 O(n^2) 到 O(n)：至多两段递增子数组](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2855.使数组成为递增数组的最少右移次数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-right-shifts-to-sort-the-array/description/)

题目要求在循环右移操作之后使得数组变为单调递增，那么只有两种可能。

第一种就是原数组本来就是单调递增的，此时无需进行任何操作，对应的答案为0。

另一种则是原数组由两个单调递增的数组拼成，同时原数组的最左侧的元素要大于最右侧的元素。理由是对于经历过右移的k个元素，其在原数组中和移动后的数组中的顺序是一致的，那么要让移动后的数组单调递增，这个部分在原数组中也必须要单调递增。同样的，未经过移动的部分保持原来的顺序不变，因此这个部分也必须要单调递增。最后，由于右侧移动的部分会放在未移动部分的左侧，因此需要满足右侧部分的最后一个元素，也就是原数组中的最右侧元素必须小于未移动部分的第一个元素，也就是原数组中最左侧的元素。

根据上面的结论，就可以先一趟遍历，找出数组中第一个满足nums[p] \< nums[p - 1]的下标p。若不存在这样的p，说明原数组单调递增，此时直接返回0。否则的话就只有从nums[p]到nums[n - 1]也单调递增，同时nums[0] > nums[n - 1]才能使得移动后的数组单调递增。若满足，此时需要移动的元素个数就是nums[p]到nums[n - 1]的元素个数，也就是n - p，否则的话说明无法得到单调递增的数组，此时返回-1。

最后附上python代码：

```python
class Solution(object):
    def minimumRightShifts(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        p = -1
        n = len(nums)
        for i in range(1, n):
            if nums[i] < nums[i - 1]:
                p = i
                break
        
        if p == -1:
            return 0
        
        for i in range(p + 1, n):
            if nums[i] < nums[i - 1]:
                return -1
        
        if nums[0] > nums[-1]:
            return n - p
        
        return -1
```
