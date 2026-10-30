---
title: "2206. 将数组划分成相等数对"
aliases: ["yiduobo的每日leetcode 2206.将数组划分成相等数对"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/539717784"
zhihu_id: "539717784"
zhihu_title: "yiduobo的每日leetcode 2206.将数组划分成相等数对"
question_id: "2206"
question: "将数组划分成相等数对"
problem_url: "https://leetcode.cn/problems/divide-array-into-equal-pairs/"
difficulty: "Easy"
created: "2022-07-09T23:19:40+08:00"
updated: "2022-07-09T23:19:40+08:00"
upvotes: 0
comments: 0
---

# 2206. 将数组划分成相等数对

> **[yiduobo的每日leetcode 2206.将数组划分成相等数对](https://zhuanlan.zhihu.com/p/539717784) · 知乎 · 2022-07-09 · 赞同 0**
> 力扣：[2206. 将数组划分成相等数对](https://leetcode.cn/problems/divide-array-into-equal-pairs/) · Easy · 灵茶山艾府：[O(n) 一次遍历](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2206.将数组划分成相等数对

[力扣](https://leetcode.cn/problems/divide-array-into-equal-pairs/)

题目要求划分出的数对中两个数相等，因此当每种数出现的次数都为偶数次时，就可以完成划分，否则就不能。于是可以一趟遍历，统计每种数出现的次数，然后判断这些次数是否都为偶数。

最后附上python代码：

```python
class Solution(object):
    def divideArray(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        num_dict = {}
        for num in nums:
            num_dict[num] = num_dict.get(num, 0) + 1
        
        for cnt in num_dict.values():
            if cnt % 2 == 1:
                return False

        return True
```
