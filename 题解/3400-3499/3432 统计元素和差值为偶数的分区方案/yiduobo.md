---
title: "3432. 统计元素和差值为偶数的分区方案"
aliases: ["yiduobo的每日leetcode 3432.统计元素和差值为偶数的分区方案"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1890561475019514725"
zhihu_id: "1890561475019514725"
zhihu_title: "yiduobo的每日leetcode 3432.统计元素和差值为偶数的分区方案"
question_id: "3432"
question: "统计元素和差值为偶数的分区方案"
problem_url: "https://leetcode.cn/problems/count-partitions-with-even-sum-difference/"
difficulty: "Easy"
rating: 1200
created: "2025-04-02T00:37:32+08:00"
updated: "2025-04-02T00:37:32+08:00"
upvotes: 0
comments: 0
---

# 3432. 统计元素和差值为偶数的分区方案

> **[yiduobo的每日leetcode 3432.统计元素和差值为偶数的分区方案](https://zhuanlan.zhihu.com/p/1890561475019514725) · 知乎 · 2025-04-02 · 赞同 0**
> 力扣：[3432. 统计元素和差值为偶数的分区方案](https://leetcode.cn/problems/count-partitions-with-even-sum-difference/) · Easy · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3432.统计元素和差值为偶数的分区方案

[3432. 统计元素和差值为偶数的分区方案 - 力扣（LeetCode）](https://leetcode.cn/problems/count-partitions-with-even-sum-difference/description/)

题目给出一个长度为n的整数数组nums，现在可以从0到n - 2之间任意选择下标index，将nums划分为nums[:index + 1]以及nums[index + 1:]这两个子数组。

问划分后两个子数组之差为偶数的划分方案数。

对于两个整数x和y而言，若x - y为偶数，那么x + y也必然为偶数。那么对于本题中的两个子数组，若二者之差为偶数，那么二者之和，也就是nums之和也必然为偶数。

反过来，若nums之和s为偶数，那么从中分离出一个和为x的子数组，剩下的子数组之和为s - x，二者之差为2 \* x - s，其奇偶性也只依赖于s的奇偶性。

也就是说若nums之和s为偶数，那么任意的index都是可行的，一共有n - 1种划分方案。反之若s为奇数，则得不到可行的划分，答案为0。

最后附上python代码：

```python
class Solution(object):
    def countPartitions(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        if sum(nums) % 2 == 0:
            return len(nums) - 1
        return 0
```
