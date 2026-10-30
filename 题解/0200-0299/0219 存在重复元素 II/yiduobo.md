---
title: "219. 存在重复元素II"
aliases: ["yiduobo的每日leetcode 219.存在重复元素II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/sliding-window", "题单/常用数据结构", "题单/面试经典-150-题", "题单/常用数据结构/零-常用枚举技巧", "题单/面试经典-150-题/哈希表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/148545497"
zhihu_id: "148545497"
zhihu_title: "yiduobo的每日leetcode 219.存在重复元素II"
question_id: "219"
question: "存在重复元素 II"
problem_url: "https://leetcode.cn/problems/contains-duplicate-ii/"
difficulty: "Easy"
created: "2020-06-15T21:48:41+08:00"
updated: "2020-06-15T21:48:41+08:00"
upvotes: 0
comments: 0
---

# 219. 存在重复元素II

> **[yiduobo的每日leetcode 219.存在重复元素II](https://zhuanlan.zhihu.com/p/148545497) · 知乎 · 2020-06-15 · 赞同 0**
> 力扣：[219. 存在重复元素 II](https://leetcode.cn/problems/contains-duplicate-ii/) · Easy · 灵茶山艾府：[两种方法：枚举右维护左/定长滑动窗口（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

219.存在重复元素II <https://leetcode-cn.com/problems/contains-duplicate-ii/>

比较基础的题目。

用一个dict维护每个数最晚一次出现的位置，然后从左往右开始扫描nums。若当前的nums\[index\]在dict中，那么就比较index与dict\[nums\[index\]\]的差值是否小于等于k即可。每扫描一个数都需要把dict\[nums\[index\]\]更新为index。

最后附上python代码：

```python
class Solution(object):
    def containsNearbyDuplicate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: bool
        """

        pos_dict = {}
        for index, num in enumerate(nums):
            if num in pos_dict and index - pos_dict[num] <= k:
                return True

            pos_dict[num] = index

        return False
```
