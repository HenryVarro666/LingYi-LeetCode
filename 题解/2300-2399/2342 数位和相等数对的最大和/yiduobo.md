---
title: "2342. 数位和相等数对的最大和"
aliases: ["yiduobo的每日leetcode 2342.数位和相等数对的最大和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/560028326"
zhihu_id: "560028326"
zhihu_title: "yiduobo的每日leetcode 2342.数位和相等数对的最大和"
question_id: "2342"
question: "数位和相等数对的最大和"
problem_url: "https://leetcode.cn/problems/max-sum-of-a-pair-with-equal-sum-of-digits/"
difficulty: "Medium"
rating: 1309
created: "2022-09-01T00:09:40+08:00"
updated: "2022-09-01T00:09:40+08:00"
upvotes: 0
comments: 0
---

# 2342. 数位和相等数对的最大和

> **[yiduobo的每日leetcode 2342.数位和相等数对的最大和](https://zhuanlan.zhihu.com/p/560028326) · 知乎 · 2022-09-01 · 赞同 0**
> 力扣：[2342. 数位和相等数对的最大和](https://leetcode.cn/problems/max-sum-of-a-pair-with-equal-sum-of-digits/) · Medium · 灵茶山艾府：[枚举右，维护左（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2342.数位和相等数对的最大和

[力扣](https://leetcode.cn/problems/max-sum-of-a-pair-with-equal-sum-of-digits/)

由于题目要找到的是两个数位和相等的数的和的最大值，那么一个自然的想法就是按照数位和将所有数分好类，然后对于每一类，找出其中最大的两个数并使用这两个数的和来更新最终答案。

由于这里只需要知道每种数位和中最大的两个数，那么也可以从左向右一趟遍历，只记录下当前遍历过的数中每种数位和的最大值。对于当前遍历到的数num，设其数位和为digit_s。

若当前的digit_s已经在max_num中出现过，那么就是用max_num[digit_s]与num之和更新答案。

另一方面，若digit_s没有在max_num中出现过，或者num大于max_num[digit_s]，那么就还需要使用num更新max_num[digit_s]。

最后附上python代码：

```python
class Solution(object):
    def maximumSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = -1
        max_num = {}
        for num in nums:
            digit_s = 0
            tmp = num
            while tmp:
                digit_s += tmp % 10
                tmp /= 10

            if digit_s not in max_num:
                max_num[digit_s] = num
            else:
                res = max(res, max_num[digit_s] + num)
                if num > max_num[digit_s]:
                    max_num[digit_s] = num
        
        return res
```
