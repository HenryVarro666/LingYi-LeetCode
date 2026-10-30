---
title: "2215. 找出两数组的不同"
aliases: ["yiduobo的每日leetcode 2215.找出两数组的不同"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/541227738"
zhihu_id: "541227738"
zhihu_title: "yiduobo的每日leetcode 2215.找出两数组的不同"
question_id: "2215"
question: "找出两数组的不同"
problem_url: "https://leetcode.cn/problems/find-the-difference-of-two-arrays/"
difficulty: "Easy"
created: "2022-07-13T18:39:50+08:00"
updated: "2022-07-13T18:39:50+08:00"
upvotes: 0
comments: 0
---

# 2215. 找出两数组的不同

> **[yiduobo的每日leetcode 2215.找出两数组的不同](https://zhuanlan.zhihu.com/p/541227738) · 知乎 · 2022-07-13 · 赞同 0**
> 力扣：[2215. 找出两数组的不同](https://leetcode.cn/problems/find-the-difference-of-two-arrays/) · Easy · 灵茶山艾府：[O(n) 模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2215.找出两数组的不同

[力扣](https://leetcode.cn/problems/find-the-difference-of-two-arrays/)

将两个数组的数分别放入两个集合中，然后分别枚举两个集合中的每个数字，检测其是否在另一个集合中出现过并根据出现情况更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def findDifference(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[List[int]]
        """

        set1 = set(nums1)
        set2 = set(nums2)
        res = [[], []]
        for num in set1:
            if num not in set2:
                res[0].append(num)
        
        for num in set2:
            if num not in set1:
                res[1].append(num)
        
        return res
```
