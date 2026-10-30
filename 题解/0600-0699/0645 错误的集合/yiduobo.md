---
title: "645. 错误的集合"
aliases: ["yiduobo的每日leetcode 645.错误的集合"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/273747853"
zhihu_id: "273747853"
zhihu_title: "yiduobo的每日leetcode 645.错误的集合"
question_id: "645"
question: "错误的集合"
problem_url: "https://leetcode.cn/problems/set-mismatch/"
created: "2020-11-04T22:38:42+08:00"
updated: "2020-11-04T22:38:42+08:00"
upvotes: 0
comments: 0
---

# 645. 错误的集合

> **[yiduobo的每日leetcode 645.错误的集合](https://zhuanlan.zhihu.com/p/273747853) · 知乎 · 2020-11-04 · 赞同 0**
> 力扣：[645. 错误的集合](https://leetcode.cn/problems/set-mismatch/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

645.错误的集合

[力扣](https://leetcode-cn.com/problems/set-mismatch/)

比较基础的题目，一趟扫描，用哈希表判断哪个数字出现了两次，然后1到n这些数字之和减去不重复的所有数字之和就是缺失的数字。

最后附上python代码：

```python
class Solution(object):
    def findErrorNums(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        num_set = set()
        s = 0
        for num in nums:
            if num in num_set:
                repeat = num
            else:
                num_set.add(num)
                s += num
            
        return [repeat, len(nums) * (len(nums) + 1) / 2 - s]
```
