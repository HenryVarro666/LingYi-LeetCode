---
title: "2789. 合并后数组中的最大元素"
aliases: ["yiduobo的每日leetcode 2789.合并后数组中的最大元素"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bian-li", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/656715132"
zhihu_id: "656715132"
zhihu_title: "yiduobo的每日leetcode 2789.合并后数组中的最大元素"
question_id: "2789"
question: "合并后数组中的最大元素"
problem_url: "https://leetcode.cn/problems/largest-element-in-an-array-after-merge-operations/"
difficulty: "Medium"
rating: 1485
created: "2023-09-17T05:15:46+08:00"
updated: "2023-09-17T05:15:46+08:00"
upvotes: 0
comments: 0
---

# 2789. 合并后数组中的最大元素

> **[yiduobo的每日leetcode 2789.合并后数组中的最大元素](https://zhuanlan.zhihu.com/p/656715132) · 知乎 · 2023-09-17 · 赞同 0**
> 力扣：[2789. 合并后数组中的最大元素](https://leetcode.cn/problems/largest-element-in-an-array-after-merge-operations/) · Medium · 灵茶山艾府：[从暴力枚举到一次遍历（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2789.合并后数组中的最大元素

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/largest-element-in-an-array-after-merge-operations/)

对于每次合并操作，当nums[i + 1]被合并成nums[i] + nums[i + 1]之后，其数值必然会变大，从而导致nums[i + 2]想要合并nums[i + 1]就更加困难。

正向合并会有这样的影响，那么不妨反过来思考。当nums[i + 1]合并了nums[i]后，其再往前合并nums[i - 1]是更容易的，也就是说如果反向合并就能越合并越容易继续合并。基于这一点，就只需倒序遍历数组，如果能合并就尽量合并。

另外，当出现无法合并的状况时，由于前一个数的值大于后面的合并结果，因此后面的合并结果就不可能是最终答案，此时只需从前一个值继续向前合并即可，因此可以使用一个变量now来储存合并结果，而不需要真正对数组进行操作。当无法合并时，将now置为前一个数就行了。在遍历完成后，now就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxArrayValue(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        now = nums[-1]
        n = len(nums)
        for index in range(n - 2, -1, -1):
            if now >= nums[index]:
                now += nums[index]
            else:
                now = nums[index]
        
        return now
```
