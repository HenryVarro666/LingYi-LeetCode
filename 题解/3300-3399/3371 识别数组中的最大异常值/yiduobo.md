---
title: "3371. 识别数组中的最大异常值"
aliases: ["yiduobo的每日leetcode 3371.识别数组中的最大异常值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/enumeration", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/28496666492"
zhihu_id: "28496666492"
zhihu_title: "yiduobo的每日leetcode 3371.识别数组中的最大异常值"
question_id: "3371"
question: "识别数组中的最大异常值"
problem_url: "https://leetcode.cn/problems/identify-the-largest-outlier-in-an-array/"
difficulty: "Medium"
rating: 1644
created: "2025-03-07T01:22:26+08:00"
updated: "2025-03-07T01:22:26+08:00"
upvotes: 0
comments: 0
---

# 3371. 识别数组中的最大异常值

> **[yiduobo的每日leetcode 3371.识别数组中的最大异常值](https://zhuanlan.zhihu.com/p/28496666492) · 知乎 · 2025-03-07 · 赞同 0**
> 力扣：[3371. 识别数组中的最大异常值](https://leetcode.cn/problems/identify-the-largest-outlier-in-an-array/) · Medium · 灵茶山艾府：[本质是两数之和：枚举异常值/枚举元素和（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3371.识别数组中的最大异常值

[3371. 识别数组中的最大异常值 - 力扣（LeetCode）](https://leetcode.cn/problems/identify-the-largest-outlier-in-an-array/description/)

题目给出一个整数数组nums，其中包含n个元素。这n个元素中有n - 2个元素是特殊数字，另外两个元素中，一个是所有特殊数字之和，另一个是异常值。现在要求找出nums中可能的最大异常值是多少。

再去除掉异常值之后，数组中元素之和就应该是两倍的特殊数字之和，那么在这里使用一个变量s记录nums中所有元素之和，另外使用一个哈希表freq记录每种数字出现的次数。接下来一趟遍历，检测当前遍历到的数字v能否作为异常值，若可以，则更新答案。

具体来说，若v是异常值，那么剩下元素之和就是s - v，这个值是特殊数字之和的两倍，因此s - v必须是偶数，且(s - v) // 2必须在freq中出现过。另外需要特别注意的是，若当前的v恰好等于(s - v) // 2，那么(s - v) // 2在freq中的出现次数必须大于等于两次，因为去除掉v这一次之外特殊数字之和也必须出现一次；反之若v不等于(s - v) // 2，那么(s - v) // 2只需在freq中出现大于等于一次就行了。

最后附上python代码：

```python
from collections import Counter

class Solution(object):
    def getLargestOutlier(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        s = sum(nums)
        freq = Counter(nums)
        res = None
        for v in nums:
            if (s - v) % 2 == 0 and (freq[(s - v) // 2] > 1 or (freq[(s - v) // 2] == 1 and (s - v) // 2 != v)):
                if res is None or res < v:
                    res = v
        return res
```
