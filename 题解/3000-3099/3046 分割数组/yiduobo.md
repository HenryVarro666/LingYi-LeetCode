---
title: "3046. 分割数组"
aliases: ["yiduobo的每日leetcode 3046.分割数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/696266487"
zhihu_id: "696266487"
zhihu_title: "yiduobo的每日leetcode 3046.分割数组"
question_id: "3046"
question: "分割数组"
problem_url: "https://leetcode.cn/problems/split-the-array/"
difficulty: "Easy"
created: "2024-05-07T01:56:21+08:00"
updated: "2024-05-07T01:56:21+08:00"
upvotes: 1
comments: 0
---

# 3046. 分割数组

> **[yiduobo的每日leetcode 3046.分割数组](https://zhuanlan.zhihu.com/p/696266487) · 知乎 · 2024-05-07 · 赞同 1**
> 力扣：[3046. 分割数组](https://leetcode.cn/problems/split-the-array/) · Easy · 灵茶山艾府：[简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3046.分割数组

[. - 力扣（LeetCode）](https://leetcode.cn/problems/split-the-array/description/)

如果数组中存在某个数v出现了大于等于三次，那么无论怎么分割，必然有至少两个v被分到同一个数组中，不符合题目要求，必然不能分割。反之，则可以先将出现次数为两次的数分摊给num1和num2，接下来将只出现一次的数分给当前长度较小的数组。于是只需一趟遍历，统计每种数字出现的次数，若其中的最大值不超过2，那么返回true，否则返回false。

最后附上python代码：

```python
class Solution(object):
    def isPossibleToSplit(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        freq = Counter(nums)
        return max(freq.values()) <= 2
```
