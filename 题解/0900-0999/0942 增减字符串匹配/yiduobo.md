---
title: "942. 增减字符串匹配"
aliases: ["yiduobo的每日leetcode 942.增减字符串匹配"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/358640803"
zhihu_id: "358640803"
zhihu_title: "yiduobo的每日leetcode 942.增减字符串匹配"
question_id: "942"
question: "增减字符串匹配"
problem_url: "https://leetcode.cn/problems/di-string-match/"
created: "2021-03-20T20:47:11+08:00"
updated: "2021-03-20T20:47:11+08:00"
upvotes: 1
comments: 0
---

# 942. 增减字符串匹配

> **[yiduobo的每日leetcode 942.增减字符串匹配](https://zhuanlan.zhihu.com/p/358640803) · 知乎 · 2021-03-20 · 赞同 1**
> 力扣：[942. 增减字符串匹配](https://leetcode.cn/problems/di-string-match/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

942.增减字符串匹配

[力扣](https://leetcode-cn.com/problems/di-string-match/)

看到I和D联想到之前某一题，本题似乎是某种低配版本？具体做法也比较简单，从头开始扫描S，若当前字符为I，那么就将当前剩下的最小值加入答案，否则将当前剩下的最大值加入答案即可。

最后附上python代码：

```python
class Solution(object):
    def diStringMatch(self, S):
        """
        :type S: str
        :rtype: List[int]
        """

        res = []
        l = 0
        r = len(S)

        for char in S:
            if char == 'I':
                res.append(l)
                l += 1
            else:
                res.append(r)
                r -= 1

        res.append(l)
        return res
```
