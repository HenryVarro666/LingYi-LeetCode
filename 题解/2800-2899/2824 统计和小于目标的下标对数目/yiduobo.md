---
title: "2824. 统计和小于目标的下标对数目"
aliases: ["yiduobo的每日leetcode 2824.统计和小于目标的下标对数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659004820"
zhihu_id: "659004820"
zhihu_title: "yiduobo的每日leetcode 2824.统计和小于目标的下标对数目"
question_id: "2824"
question: "统计和小于目标的下标对数目"
problem_url: "https://leetcode.cn/problems/count-pairs-whose-sum-is-less-than-target/"
difficulty: "Easy"
created: "2023-09-29T01:18:47+08:00"
updated: "2023-09-29T01:18:47+08:00"
upvotes: 0
comments: 0
---

# 2824. 统计和小于目标的下标对数目

> **[yiduobo的每日leetcode 2824.统计和小于目标的下标对数目](https://zhuanlan.zhihu.com/p/659004820) · 知乎 · 2023-09-29 · 赞同 0**
> 力扣：[2824. 统计和小于目标的下标对数目](https://leetcode.cn/problems/count-pairs-whose-sum-is-less-than-target/) · Easy · 灵茶山艾府：[O(nlogn) 排序+相向双指针（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2824.统计和小于目标的下标对数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-pairs-whose-sum-is-less-than-target/description/)

本题与站内第一题类似，也同样可以排序后利用双指针来解决。不过由于数据规模非常小，我在这里直接使用的暴力法，两两枚举下标对然后判断。

最后附上python代码：

```python
class Solution(object):
    def countPairs(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """

        n = len(nums)
        res = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                if nums[i] + nums[j] < target:
                    res += 1
        
        return res
```
