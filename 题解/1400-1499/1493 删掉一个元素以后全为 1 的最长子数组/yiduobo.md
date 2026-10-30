---
title: "1493. 删掉一个元素后全为1的最长子数组"
aliases: ["yiduobo的每日leetcode 1493.删掉一个元素后全为1的最长子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/动态规划", "题单/滑动窗口与双指针/二-不定长滑动窗口", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/416791963"
zhihu_id: "416791963"
zhihu_title: "yiduobo的每日leetcode 1493.删掉一个元素后全为1的最长子数组"
question_id: "1493"
question: "删掉一个元素以后全为 1 的最长子数组"
problem_url: "https://leetcode.cn/problems/longest-subarray-of-1s-after-deleting-one-element/"
difficulty: "Medium"
rating: 1423
created: "2021-10-04T09:06:54+08:00"
updated: "2021-10-04T09:06:54+08:00"
upvotes: 0
comments: 0
---

# 1493. 删掉一个元素后全为1的最长子数组

> **[yiduobo的每日leetcode 1493.删掉一个元素后全为1的最长子数组](https://zhuanlan.zhihu.com/p/416791963) · 知乎 · 2021-10-04 · 赞同 0**
> 力扣：[1493. 删掉一个元素以后全为 1 的最长子数组](https://leetcode.cn/problems/longest-subarray-of-1s-after-deleting-one-element/) · Medium · 灵茶山艾府：[滑动窗口（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1493.删掉一个元素后全为1的最长子数组

[力扣](https://leetcode-cn.com/problems/longest-subarray-of-1s-after-deleting-one-element/)

题目要求找出删除一个元素后全为1的最长子数组。

先考察特殊情况。当数组中全都是1时，那么删去任意元素，答案都是数组长度减1。

接下来考虑一般情况。此时数组中至少有一个0，而为了使得答案尽量长，显然应该删去一个0，而删去这个0会使得0前后两段连续的1被合并为一段，因此可以一趟扫描，使用now_l表示当前这一段连续1的长度，last_l表示翻过一个0之后上一段连续1的长度。那么对于元素num：

1、若num等于1，那么将当前连续1的长度now_l加上1

2、若num等于0，说明当前这一段连续1已经结束，应该使用now_l加上last_l来更新答案。此时的now_l就变成了last_l，而now_l则应该被置为0

由于数组可能由1结尾，因此在扫描结束后，还需要使用最后的now_l加上last_l来更新答案。

最后附上python代码：

```python
class Solution(object):
    def longestSubarray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        last_l = 0
        zero_flag = False
        now_l = 0
        res = 0
        for num in nums:
            if num == 1:
                now_l += 1
            else:
                zero_flag = True
                res = max(res, now_l + last_l)
                last_l = now_l
                now_l = 0

        res = max(res, now_l + last_l)
        if not zero_flag:
            res -= 1
        
        return res
```
