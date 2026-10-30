---
title: "2248. 多个数组求交集"
aliases: ["yiduobo的每日leetcode 2248.多个数组求交集"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/hash-table", "leetcode/enumeration", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/546521933"
zhihu_id: "546521933"
zhihu_title: "yiduobo的每日leetcode 2248.多个数组求交集"
question_id: "2248"
question: "多个数组求交集"
problem_url: "https://leetcode.cn/problems/intersection-of-multiple-arrays/"
difficulty: "Easy"
created: "2022-07-26T23:45:06+08:00"
updated: "2022-07-26T23:45:06+08:00"
upvotes: 0
comments: 0
---

# 2248. 多个数组求交集

> **[yiduobo的每日leetcode 2248.多个数组求交集](https://zhuanlan.zhihu.com/p/546521933) · 知乎 · 2022-07-26 · 赞同 0**
> 力扣：[2248. 多个数组求交集](https://leetcode.cn/problems/intersection-of-multiple-arrays/) · Easy · 灵茶山艾府：[统计每个元素的出现次数](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2248.多个数组求交集

[力扣](https://leetcode.cn/problems/intersection-of-multiple-arrays/)

由于所有数的范围到在1到1000之内，同时最终答案要求从小到大进行排序，因此可以从小到大枚举1到1000内的所有数，判断这个数是否在每个数组中都出现过。当然，在这之前应该先将每个数组转化成集合或哈希表，这样才能高效地判断某个数是否出现过。

最后附上python代码：

```python
class Solution(object):
    def intersection(self, nums):
        """
        :type nums: List[List[int]]
        :rtype: List[int]
        """

        num_set_list = []
        for num_list in nums:
            num_set_list.append(set(num_list))
        
        res = []
        for num in range(1, 1001):
            flag = True
            for num_set in num_set_list:
                if num not in num_set:
                    flag = False
                    break
            
            if flag:
                res.append(num)
        
        return res
```
