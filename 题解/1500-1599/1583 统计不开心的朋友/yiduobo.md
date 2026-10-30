---
title: "1583. 统计不开心的朋友"
aliases: ["yiduobo的每日leetcode 1583.统计不开心的朋友"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/430432544"
zhihu_id: "430432544"
zhihu_title: "yiduobo的每日leetcode 1583.统计不开心的朋友"
question_id: "1583"
question: "统计不开心的朋友"
problem_url: "https://leetcode.cn/problems/count-unhappy-friends/"
created: "2021-11-07T14:51:32+08:00"
updated: "2021-11-07T14:51:32+08:00"
upvotes: 0
comments: 0
---

# 1583. 统计不开心的朋友

> **[yiduobo的每日leetcode 1583.统计不开心的朋友](https://zhuanlan.zhihu.com/p/430432544) · 知乎 · 2021-11-07 · 赞同 0**
> 力扣：[1583. 统计不开心的朋友](https://leetcode.cn/problems/count-unhappy-friends/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1583.统计不开心的朋友

[力扣](https://leetcode-cn.com/problems/count-unhappy-friends/)

由于这里n的规模很小，因此可以直接逐个进行判断。

对于x而言，不妨设其配对的朋友为pair[x]，那么此时可以枚举所有亲密度大于pair[x]的朋友y。若对于y而言，x的亲密度大于其配对的朋友pair[y]的亲密度，那么x就是不开心的，此时应该将答案加上1。

具体实现上，由于preferences已经按从高到低的亲密度排列好了，因此枚举y可以从preferences[x]从前向后进行枚举，直到枚举到pair[x]停止。而对于y而言，则可以使用一个dict来储存其他所有人的亲密度排位，即dict[y][x]表示x在y这里的亲密度排位。这个dict也可以通过preferences预处理得到。

最后附上python代码：

```python
class Solution(object):
    def unhappyFriends(self, n, preferences, pairs):
        """
        :type n: int
        :type preferences: List[List[int]]
        :type pairs: List[List[int]]
        :rtype: int
        """

        prefer_dict = {}
        for x, prefer in enumerate(preferences):
            prefer_dict[x] = {}
            for level, y in enumerate(prefer):
                prefer_dict[x][y] = level
        
        pair_dict = {}
        for x, y in pairs:
            pair_dict[x] = y
            pair_dict[y] = x

        res = 0
        for x in pair_dict:
            for y in preferences[x]:
                if y == pair_dict[x]:
                    break
                if prefer_dict[y][x] < prefer_dict[y][pair_dict[y]]:
                    res += 1
                    break
        
        return res
```
