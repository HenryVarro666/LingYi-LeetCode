---
title: "2574. 左右元素和的差值"
aliases: ["yiduobo的每日leetcode 2574.左右元素和的差值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/641762946"
zhihu_id: "641762946"
zhihu_title: "yiduobo的每日leetcode 2574.左右元素和的差值"
question_id: "2574"
question: "左右元素和的差值"
problem_url: "https://leetcode.cn/problems/left-and-right-sum-differences/"
difficulty: "Easy"
rating: 1206
created: "2023-07-06T01:23:12+08:00"
updated: "2023-07-06T01:23:12+08:00"
upvotes: 0
comments: 0
---

# 2574. 左右元素和的差值

> **[yiduobo的每日leetcode 2574.左右元素和的差值](https://zhuanlan.zhihu.com/p/641762946) · 知乎 · 2023-07-06 · 赞同 0**
> 力扣：[2574. 左右元素和的差值](https://leetcode.cn/problems/left-and-right-sum-differences/) · Easy · 灵茶山艾府：[两次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2574.左右元素和的差值

[力扣](https://leetcode.cn/problems/left-and-right-sum-differences/)

对于数组中的某个位置p而言，题目中的左右元素和的差值可以认为是到位置p - 1的前缀和与从p + 1开始的后缀和之差的绝对值，而这个后缀和也可以通过总和减去前缀和以及p对应的值得到，那么就可以先计算出数组的总和s，接下来一趟遍历，同时使用一个变量now表示前缀和。

对于当前遍历到的数v，其左侧元素和就是当前的前缀和now，而其右侧元素和则可以通过s - now - v得到，因此v对应的左右元素和差值就是abs(s - now - v - now)，将其加入到答案数组后，再将v累加到now中然后继续向后遍历即可。

最后附上python代码：

```python
class Solution(object):
    def leftRightDifference(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        s = sum(nums)
        res = []
        now = 0
        for v in nums:
            res.append(abs(s - now - v - now))
            now += v
        
        return res
```
