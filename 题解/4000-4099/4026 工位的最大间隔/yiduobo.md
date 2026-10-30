---
title: "4026. 工位的最大间隔"
aliases: ["yiduobo的每日leetcode 4026.工位的最大间隔"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/四-双序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2073913902983799739"
zhihu_id: "2073913902983799739"
zhihu_title: "yiduobo的每日leetcode 4026.工位的最大间隔"
question_id: "4026"
question: "工位的最大间隔"
problem_url: "https://leetcode.cn/problems/maximum-gap-between-stations/"
difficulty: "Medium"
rating: 1675
created: "2026-08-20T23:37:43+08:00"
updated: "2026-08-20T23:37:43+08:00"
upvotes: 1
comments: 0
---

# 4026. 工位的最大间隔

> **[yiduobo的每日leetcode 4026.工位的最大间隔](https://zhuanlan.zhihu.com/p/2073913902983799739) · 知乎 · 2026-08-20 · 赞同 1**
> 力扣：[4026. 工位的最大间隔](https://leetcode.cn/problems/maximum-gap-between-stations/) · Medium · 灵茶山艾府：[前后缀分解（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4026.工位的最大间隔

<https://leetcode.cn/problems/maximum-gap-between-stations/description/>

题目给出两个长度分别为n和m的字符串skill和station，分别表示工人的技能，以及工位所支持的技能。

现在要求将每一名工人分配到一个互不相同的工位，要求工位所支持的技能恰好等于工人的技能，同时分配给工人的工位必须按照工人的顺序严格递增。

分配方案的间隔，指的是分配给两名相邻工人的工位下标间的最大差，若只存在一名工人，则间隔为0。

问所有有效分配方案中可能得到的最大间隔。保证至少存在一种有效的分配方案。

题目实际上就是要从station中找出一个与skill完全相同的子序列，同时这个子序列中，某两个位置的间隔最大。

首先，若只有一名工人，则直接返回0。接下来，若工人的数量大于1名，那么不妨其对应的下标子序列中，间隔最大的两个位置在skill中对应的下标为p - 1和p，那么在这里的目标就是将skill[:p]尽量靠前压紧，即在station中找出最靠前的可以匹配skill[:p]的子序列；同样的，对于skill[p:]则应该尽量靠后压紧，即在station中找出最靠后的可以匹配skill[p:]的子序列。这样一来，skill[p - 1]与skill[p]的间隔才能最大。

基于上面的结论，就可以正反两趟遍历，找出station中能匹配skill的每个前缀的最短前缀的结束为止left，以及能匹配skill的每个后缀的最短后缀的起始位置right，接下来只需遍历这个分割点p，就使用right[index] - left[index - 1]更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maximumGap(self, skill, station):
        """
        :type skill: str
        :type station: str
        :rtype: int
        """
        
        if len(skill) == 1:
            return 0
        
        left = []
        p = 0
        for s in skill:
            while station[p] != s:
                p += 1
            left.append(p)
            p += 1
        
        right = []
        p = len(station) - 1
        for s in skill[::-1]:
            while station[p] != s:
                p -= 1
            right.append(p)
            p -= 1
        right.reverse()

        res = 0
        for index in range(1, len(skill)):
            res = max(res, right[index] - left[index - 1])
        
        return res
```
