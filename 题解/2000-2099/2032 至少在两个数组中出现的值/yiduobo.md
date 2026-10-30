---
title: "2032. 至少在两个数组中出现的值"
aliases: ["yiduobo的每日leetcode 2032.至少在两个数组中出现的值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/hash-table", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/508485173"
zhihu_id: "508485173"
zhihu_title: "yiduobo的每日leetcode 2032.至少在两个数组中出现的值"
question_id: "2032"
question: "至少在两个数组中出现的值"
problem_url: "https://leetcode.cn/problems/two-out-of-three/"
difficulty: "Easy"
created: "2022-05-02T18:08:35+08:00"
updated: "2022-05-02T18:08:35+08:00"
upvotes: 0
comments: 0
---

# 2032. 至少在两个数组中出现的值

> **[yiduobo的每日leetcode 2032.至少在两个数组中出现的值](https://zhuanlan.zhihu.com/p/508485173) · 知乎 · 2022-05-02 · 赞同 0**
> 力扣：[2032. 至少在两个数组中出现的值](https://leetcode.cn/problems/two-out-of-three/) · Easy · 灵茶山艾府：[位运算写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2032.至少在两个数组中出现的值

[力扣](https://leetcode-cn.com/problems/two-out-of-three/)

比较基础的题目，不过题目描述有点问题。这里的不同指的是答案数组中的每个数不同，而不是指的要与原始的3个数组不同。

由于题目中数值的范围在1到100以内，那么可以直接从1到100开始进行枚举，判断当前这个数是否出现在至少两个数组内，如果满足就将其加入到答案中。

最后附上python代码：

```python
class Solution(object):
    def twoOutOfThree(self, nums1, nums2, nums3):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type nums3: List[int]
        :rtype: List[int]
        """

        set1 = set(nums1)
        set2 = set(nums2)
        set3 = set(nums3)

        res = []
        for num in range(1, 101):
            score = 0
            if num in set1:
                score += 1
            if num in set2:
                score += 1
            if num in set3:
                score += 1
            
            if score >= 2:
                res.append(num)

        return res
```
