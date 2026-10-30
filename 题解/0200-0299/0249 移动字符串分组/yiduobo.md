---
title: "249. 移动字符串分组"
aliases: ["yiduobo的每日leetcode 249.移动字符串分组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/592448096"
zhihu_id: "592448096"
zhihu_title: "yiduobo的每日leetcode 249.移动字符串分组"
question_id: "249"
question: "移动字符串分组"
problem_url: "https://leetcode.cn/problems/group-shifted-strings/"
created: "2022-12-17T04:46:51+08:00"
updated: "2022-12-17T04:46:51+08:00"
upvotes: 0
comments: 0
---

# 249. 移动字符串分组

> **[yiduobo的每日leetcode 249.移动字符串分组](https://zhuanlan.zhihu.com/p/592448096) · 知乎 · 2022-12-17 · 赞同 0**
> 力扣：[249. 移动字符串分组](https://leetcode.cn/problems/group-shifted-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

249.移动字符串分组

[力扣](https://leetcode.cn/problems/group-shifted-strings/)

首先根据题目的意思，所有长度为1的字符串都可以归位同一组。接下来对于长度大于等于2的字符串，如果两个字符串可以分为同一组，那么就意味着其中一个字符串中的所有字符移动若干次之后可以变为另一个字符串。不妨设这两个字符串分别为s和t，那么就可以认为s[0] + k \= t[0]、s[1] + k \= t[1]、...、s[-1] + k \= t[-1]。

根据上面的式子，如果将相邻的位置相减，那么就有t[i] - t[i - 1] \= (s[i] + k) - (s[i - 1] + k) \= s[i] - s[i - 1]，也就是说如果两个字符串可以分到同一组，那么相邻位置相减得到的差值数组必然是完全相同的。于是可以用这个差值数组作为key，使用一个哈希表记录每个组中的字符串。接下来只需一趟遍历，计算每个长度大于等于2的字符串的差值数组并将其分到对应的组中，然后再与长度为1的字符串那一组合并后返回。

最后附上python代码：

```python
class Solution(object):
    def groupStrings(self, strings):
        """
        :type strings: List[str]
        :rtype: List[List[str]]
        """

        single_list = []
        h = {}
        for s in strings:
            if len(s) == 1:
                single_list.append(s)
            else:
                diff_list = [(ord(s[index]) - ord(s[index - 1]) + 26) % 26 for index in range(1, len(s))]
                key = tuple(diff_list)
                if key not in h:
                    h[key] = []
                h[key].append(s)
        
        res = h.values()
        if single_list:
            res.append(single_list)
        return res
```
