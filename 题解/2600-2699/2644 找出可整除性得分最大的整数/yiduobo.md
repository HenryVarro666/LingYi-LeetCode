---
title: "2644. 找出可整除性得分最大的整数"
aliases: ["yiduobo的每日leetcode 2644.找出可整除性得分最大的整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/enumeration", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/646932878"
zhihu_id: "646932878"
zhihu_title: "yiduobo的每日leetcode 2644.找出可整除性得分最大的整数"
question_id: "2644"
question: "找出可整除性得分最大的整数"
problem_url: "https://leetcode.cn/problems/find-the-maximum-divisibility-score/"
difficulty: "Easy"
created: "2023-07-31T03:07:01+08:00"
updated: "2023-07-31T03:07:01+08:00"
upvotes: 0
comments: 0
---

# 2644. 找出可整除性得分最大的整数

> **[yiduobo的每日leetcode 2644.找出可整除性得分最大的整数](https://zhuanlan.zhihu.com/p/646932878) · 知乎 · 2023-07-31 · 赞同 0**
> 力扣：[2644. 找出可整除性得分最大的整数](https://leetcode.cn/problems/find-the-maximum-divisibility-score/) · Easy · 灵茶山艾府：[暴力枚举+排序优化（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2644.找出可整除性得分最大的整数

[力扣](https://leetcode.cn/problems/find-the-maximum-divisibility-score/)

直接遍历divisors中的所有整数，对于当前遍历到的整数d，遍历nums，计算nums中可以整除d的个数cnt，然后按照题目要求使用cnt和d更新最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxDivScore(self, nums, divisors):
        """
        :type nums: List[int]
        :type divisors: List[int]
        :rtype: int
        """

        ma = 0
        res = 10 ** 9 + 1
        for d in divisors:
            cnt = 0
            for v in nums:
                if v % d == 0:
                    cnt += 1
            
            if ma < cnt or (ma == cnt and d < res):
                ma = cnt
                res = d
        
        return res
```
