---
title: "3300. 替换为数位和以后的最小元素"
aliases: ["yiduobo的每日leetcode 3300.替换为数位和以后的最小元素"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/978394390"
zhihu_id: "978394390"
zhihu_title: "yiduobo的每日leetcode 3300.替换为数位和以后的最小元素"
question_id: "3300"
question: "替换为数位和以后的最小元素"
problem_url: "https://leetcode.cn/problems/minimum-element-after-replacement-with-digit-sum/"
difficulty: "Easy"
created: "2024-10-13T02:00:00+08:00"
updated: "2024-10-13T02:00:00+08:00"
upvotes: 0
comments: 0
---

# 3300. 替换为数位和以后的最小元素

> **[yiduobo的每日leetcode 3300.替换为数位和以后的最小元素](https://zhuanlan.zhihu.com/p/978394390) · 知乎 · 2024-10-13 · 赞同 0**
> 力扣：[3300. 替换为数位和以后的最小元素](https://leetcode.cn/problems/minimum-element-after-replacement-with-digit-sum/) · Easy · 灵茶山艾府：[不用字符串的写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3300.替换为数位和以后的最小元素

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-element-after-replacement-with-digit-sum/)

题目给出一个整数数组nums，要求将其中每个元素都替换为它的各个数位之和，问替换后的元素的最小值。

按照题目要求来做就行了。一趟遍历，对于每个元素先逐位分离并计算数位之和，然后取其中的最小值作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def minElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = None
        for v in nums:
            s = 0
            while v:
                s += v % 10
                v //= 10
            
            if res is None or res > s:
                res = s
                
        return res
```
