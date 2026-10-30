---
title: "485. 最大连续1的个数"
aliases: ["yiduobo的每日leetcode 485.最大连续1的个数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/250943914"
zhihu_id: "250943914"
zhihu_title: "yiduobo的每日leetcode 485.最大连续1的个数"
question_id: "485"
question: "最大连续 1 的个数"
problem_url: "https://leetcode.cn/problems/max-consecutive-ones/"
difficulty: "Easy"
created: "2020-09-17T20:44:11+08:00"
updated: "2020-09-17T20:44:11+08:00"
upvotes: 0
comments: 0
---

# 485. 最大连续1的个数

> **[yiduobo的每日leetcode 485.最大连续1的个数](https://zhuanlan.zhihu.com/p/250943914) · 知乎 · 2020-09-17 · 赞同 0**
> 力扣：[485. 最大连续 1 的个数](https://leetcode.cn/problems/max-consecutive-ones/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

485.最大连续1的个数<https://leetcode-cn.com/problems/max-consecutive-ones/>

比较基础的题目，一趟扫描统计1连续出现的次数即可。

最后附上python代码：

```python
class Solution(object):
    def findMaxConsecutiveOnes(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        now = 0
        for num in nums:
            if num == 1:
                now += 1
            else:
                res = max(now, res)
                now = 0
        return max(now, res)
```
