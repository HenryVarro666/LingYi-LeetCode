---
title: "3452. 好数字之和"
aliases: ["yiduobo的每日leetcode 3452.好数字之和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1893414455909540401"
zhihu_id: "1893414455909540401"
zhihu_title: "yiduobo的每日leetcode 3452.好数字之和"
question_id: "3452"
question: "好数字之和"
problem_url: "https://leetcode.cn/problems/sum-of-good-numbers/"
difficulty: "Easy"
created: "2025-04-09T21:32:23+08:00"
updated: "2025-04-09T21:32:23+08:00"
upvotes: 1
comments: 0
---

# 3452. 好数字之和

> **[yiduobo的每日leetcode 3452.好数字之和](https://zhuanlan.zhihu.com/p/1893414455909540401) · 知乎 · 2025-04-09 · 赞同 1**
> 力扣：[3452. 好数字之和](https://leetcode.cn/problems/sum-of-good-numbers/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3452.好数字之和

[3452. 好数字之和 - 力扣（LeetCode）](https://leetcode.cn/problems/sum-of-good-numbers/description/)

题目给出一个整数数组nums以及一个整数k，对于其中的某个元素nums[index]，若index - k不存在，或者nums[index]严格大于下标nums[index - k]，同时index + k不存在，或者nums[index]严格大于nums[index + k]处的元素，那么就认为nums[index]是好的。问nums中所有好元素之和。

直接对nums进行一趟遍历，对于nums[index]，按照题目描述中关于好元素的定义，检测index - k是否不存在，或者nums[index]严格大于nums[index - k]，同时检测index + k是否不存在，或者nums[index]严格大于nums[index + k]。若两边都满足，那么就将nums[index]累加到答案中。

最后附上python代码：

```python
class Solution(object):
    def sumOfGoodNumbers(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        res = 0
        for index, v in enumerate(nums):
            if (index - k < 0 or nums[index - k] < v) and (index + k >= len(nums) or nums[index + k] < v):
                res += v
        
        return res
```
