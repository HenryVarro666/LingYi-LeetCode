---
title: "LCP 66. 最小展台数量"
aliases: ["yiduobo的每日leetcode LCP66.最小展台数量"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/579890408"
zhihu_id: "579890408"
zhihu_title: "yiduobo的每日leetcode LCP66.最小展台数量"
question_id: "LCP 66"
question: "最小展台数量"
problem_url: "https://leetcode.cn/problems/600YaG/"
difficulty: "Easy"
created: "2022-11-03T01:05:41+08:00"
updated: "2022-11-03T01:05:41+08:00"
upvotes: 0
comments: 0
---

# LCP 66. 最小展台数量

> **[yiduobo的每日leetcode LCP66.最小展台数量](https://zhuanlan.zhihu.com/p/579890408) · 知乎 · 2022-11-03 · 赞同 0**
> 力扣：[LCP 66. 最小展台数量](https://leetcode.cn/problems/600YaG/) · Easy · 灵茶山艾府：[Python 一行](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP66.最小展台数量

[力扣](https://leetcode.cn/problems/600YaG/description/)

由于不同天之间，展台可以重复利用，那么只需一趟遍历，找出每种展台在同一天中最多需要几个，然后将每种展台单天最多需要的数量累加起来即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minNumBooths(self, demand):
        """
        :type demand: List[str]
        :rtype: int
        """

        max_cnt = {}
        for d in demand:
            char_cnt = {}
            for char in d:
                char_cnt[char] = char_cnt.get(char, 0) + 1
            
            for char in char_cnt:
                if char_cnt[char] > max_cnt.get(char, 0):
                    max_cnt[char] = char_cnt[char]
        
        return sum(max_cnt.values())
```
