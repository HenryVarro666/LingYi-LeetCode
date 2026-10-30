---
title: "2367. 算术三元组的数目"
aliases: ["yiduobo的每日leetcode 2367.算术三元组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/two-pointers", "leetcode/shi-pin", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/五-三指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/563197551"
zhihu_id: "563197551"
zhihu_title: "yiduobo的每日leetcode 2367.算术三元组的数目"
question_id: "2367"
question: "等差三元组的数目"
problem_url: "https://leetcode.cn/problems/number-of-arithmetic-triplets/"
difficulty: "Easy"
created: "2022-09-10T16:42:36+08:00"
updated: "2022-09-10T16:42:36+08:00"
upvotes: 0
comments: 0
---

# 2367. 算术三元组的数目

> **[yiduobo的每日leetcode 2367.算术三元组的数目](https://zhuanlan.zhihu.com/p/563197551) · 知乎 · 2022-09-10 · 赞同 0**
> 力扣：[2367. 等差三元组的数目](https://leetcode.cn/problems/number-of-arithmetic-triplets/) · Easy · 灵茶山艾府：[两种 O(n) 做法：哈希表 / 三指针](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2367.算术三元组的数目

[力扣](https://leetcode.cn/problems/number-of-arithmetic-triplets/)

一趟遍历，使用集合记录已经遍历过的数，接下来对于当前遍历到的数num，若num - diff以及num - diff - diff都出现在集合中，说明这三个数就是一组合法的算术三元组。无论是否存在有效的算术三元组，最后都需要将num也加入到集合中，然后继续向后遍历。

最后附上python代码：

```python
class Solution(object):
    def arithmeticTriplets(self, nums, diff):
        """
        :type nums: List[int]
        :type diff: int
        :rtype: int
        """

        num_set = set()
        res = 0
        for num in nums:
            if num - diff in num_set and num - diff - diff in num_set:
                res += 1
            num_set.add(num)
        
        return res
```
