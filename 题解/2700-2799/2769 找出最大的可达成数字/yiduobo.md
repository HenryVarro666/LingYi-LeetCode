---
title: "2769. 找出最大的可达成数字"
aliases: ["yiduobo的每日leetcode 2769.找出最大的可达成数字"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/655331954"
zhihu_id: "655331954"
zhihu_title: "yiduobo的每日leetcode 2769.找出最大的可达成数字"
question_id: "2769"
question: "找出最大的可达成数字"
problem_url: "https://leetcode.cn/problems/find-the-maximum-achievable-number/"
difficulty: "Easy"
created: "2023-09-09T23:52:30+08:00"
updated: "2023-09-09T23:52:30+08:00"
upvotes: 0
comments: 0
---

# 2769. 找出最大的可达成数字

> **[yiduobo的每日leetcode 2769.找出最大的可达成数字](https://zhuanlan.zhihu.com/p/655331954) · 知乎 · 2023-09-09 · 赞同 0**
> 力扣：[2769. 找出最大的可达成数字](https://leetcode.cn/problems/find-the-maximum-achievable-number/) · Easy · 灵茶山艾府：[阅读理解（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2769.找出最大的可达成数字

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/find-the-maximum-achievable-number/)

为了使得答案最大，那么每一步都应该是让答案减去1，然后让num加上1，最终使得二者相等，而对应的答案就应该是num + t + t。

最后附上python代码：

```python
class Solution(object):
    def theMaximumAchievableX(self, num, t):
        """
        :type num: int
        :type t: int
        :rtype: int
        """

        return num + t + t
```
