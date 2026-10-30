---
title: "4083. 使相邻元素按位异或非零的最少删除次数"
aliases: ["yiduobo的每日leetcode 4083.使相邻元素按位异或非零的最少删除次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2095186543912673645"
zhihu_id: "2095186543912673645"
zhihu_title: "yiduobo的每日leetcode 4083.使相邻元素按位异或非零的最少删除次数"
question_id: "4083"
question: "使相邻元素按位异或非零的最少删除次数"
problem_url: "https://leetcode.cn/problems/minimum-deletions-to-make-array-sharp/"
created: "2026-10-18T16:20:30+08:00"
updated: "2026-10-18T16:20:30+08:00"
upvotes: 0
comments: 0
---

# 4083. 使相邻元素按位异或非零的最少删除次数

> **[yiduobo的每日leetcode 4083.使相邻元素按位异或非零的最少删除次数](https://zhuanlan.zhihu.com/p/2095186543912673645) · 知乎 · 2026-10-18 · 赞同 0**
> 力扣：[4083. 使相邻元素按位异或非零的最少删除次数](https://leetcode.cn/problems/minimum-deletions-to-make-array-sharp/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4803.使相邻元素按位异或非零的最少删除次数

<https://leetcode.cn/problems/minimum-deletions-to-make-array-sharp/description/>

题目给出一个整数数组nums。

现在可以从nums中删除任意数量的元素，剩下的元素将保持原有的相对顺序。

若数组中每一对相邻元素的按位异或结果都不为0，则称这个数组为相邻异或非零数组。问至少需要多少次删除操作，才能使得nums变为相邻异或非零数组。

两个元素异或值为零，意味着这两个元素相同，因此本题实际上就是要将nums变为一个相邻元素互不相同的数组，于是只需从下标1开始一趟遍历，检测每个元素是否和前一个剩下的元素相同，若相同，则删除当前元素并更新答案，否则保留当前元素。

最后附上python代码：

```python
class Solution(object):
    def minDeletions(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        pre = nums[0]
        res = 0
        for v in nums[1:]:
            if pre == v:
                res += 1
            else:
                pre = v
        
        return res
```
