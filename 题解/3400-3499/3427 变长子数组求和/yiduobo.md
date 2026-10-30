---
title: "3427. 变长子数组求和"
aliases: ["yiduobo的每日leetcode 3427.变长子数组求和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/prefix-sum", "leetcode/bao-li", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1889802409091514541"
zhihu_id: "1889802409091514541"
zhihu_title: "yiduobo的每日leetcode 3427.变长子数组求和"
question_id: "3427"
question: "变长子数组求和"
problem_url: "https://leetcode.cn/problems/sum-of-variable-length-subarrays/"
difficulty: "Easy"
created: "2025-03-30T22:16:54+08:00"
updated: "2025-03-30T22:16:54+08:00"
upvotes: 0
comments: 0
---

# 3427. 变长子数组求和

> **[yiduobo的每日leetcode 3427.变长子数组求和](https://zhuanlan.zhihu.com/p/1889802409091514541) · 知乎 · 2025-03-30 · 赞同 0**
> 力扣：[3427. 变长子数组求和](https://leetcode.cn/problems/sum-of-variable-length-subarrays/) · Easy · 灵茶山艾府：[三种方法：暴力 / 前缀和 / 差分数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3427.变长子数组求和

[3427. 变长子数组求和 - 力扣（LeetCode）](https://leetcode.cn/problems/sum-of-variable-length-subarrays/description/)

题目给出一个长度为n的整数数组nums。对于每个在0到n - 1之间的下标index，定义对应的子数组为nums[start: index + 1]，其中start \= max(0, index - nums[index])。

现在要求返回每个下标对应子数组的元素之和。

根据题目的描述，对于每个下标index，可以先计算出对应的start，那么问题就转化成了求数组区间和的问题。于是只需先一趟遍历，预处理出数组的前缀和，然后就可以很方便的得到对应的区间和了。

最后附上python代码：

```python
class Solution(object):
    def subarraySum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        s = [nums[0]]
        for v in nums[1:]:
            s.append(s[-1] + v)
        
        res = 0
        for index, v in enumerate(nums):
            start = max(0, index - v)
            res += s[index]
            if start > 0:
                res -= s[start - 1]
        
        return res
```
