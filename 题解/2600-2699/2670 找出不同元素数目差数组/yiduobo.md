---
title: "2670. 找出不同元素数目差数组"
aliases: ["yiduobo的每日leetcode 2670.找出不同元素数目差数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/648847596"
zhihu_id: "648847596"
zhihu_title: "yiduobo的每日leetcode 2670.找出不同元素数目差数组"
question_id: "2670"
question: "找出不同元素数目差数组"
problem_url: "https://leetcode.cn/problems/find-the-distinct-difference-array/"
difficulty: "Easy"
created: "2023-08-09T01:32:46+08:00"
updated: "2023-08-09T01:32:46+08:00"
upvotes: 0
comments: 1
---

# 2670. 找出不同元素数目差数组

> **[yiduobo的每日leetcode 2670.找出不同元素数目差数组](https://zhuanlan.zhihu.com/p/648847596) · 知乎 · 2023-08-09 · 赞同 0**
> 力扣：[2670. 找出不同元素数目差数组](https://leetcode.cn/problems/find-the-distinct-difference-array/) · Easy · 灵茶山艾府：[O(n) 前后缀分解（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2670.找出不同元素数目差数组

[力扣](https://leetcode.cn/problems/find-the-distinct-difference-array/description/)

题目要去对于数组中的每个位置，都计算以当前位置为结尾的前缀中不同元素的数目与以当前位置下一个位置为开头的后缀中不同元素的数目，那么在这里不妨将其拆分开来，分别计算然后相减。

首先正向一趟遍历，使用哈希表计算当前前缀中不同元素的数目，并将其累加到答案数组的对应下标。

接下来反向一趟遍历，同样是使用哈希表计算当前后缀中不同元素的数目，不过这里有些微不同，需要使用答案数组的上一位减去当前不同元素的数目。

最后附上python代码：

```python
class Solution(object):
    def distinctDifferenceArray(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        n = len(nums)
        res = [0] * n
        
        num_set = set()
        for index in range(n):
            num_set.add(nums[index])
            res[index] = len(num_set)
        
        num_set = set()
        for index in range(n - 1, 0, -1):
            num_set.add(nums[index])
            res[index - 1] -= len(num_set)
        
        return res
```
