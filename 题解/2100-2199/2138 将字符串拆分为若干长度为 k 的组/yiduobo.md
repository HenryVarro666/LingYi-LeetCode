---
title: "2138. 将字符串拆分成若干长度为k的组"
aliases: ["yiduobo的每日leetcode 2138.将字符串拆分成若干长度为k的组"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/528385839"
zhihu_id: "528385839"
zhihu_title: "yiduobo的每日leetcode 2138.将字符串拆分成若干长度为k的组"
question_id: "2138"
question: "将字符串拆分为若干长度为 k 的组"
problem_url: "https://leetcode.cn/problems/divide-a-string-into-groups-of-size-k/"
difficulty: "Easy"
created: "2022-06-13T22:54:28+08:00"
updated: "2022-06-13T22:54:28+08:00"
upvotes: 0
comments: 0
---

# 2138. 将字符串拆分成若干长度为k的组

> **[yiduobo的每日leetcode 2138.将字符串拆分成若干长度为k的组](https://zhuanlan.zhihu.com/p/528385839) · 知乎 · 2022-06-13 · 赞同 0**
> 力扣：[2138. 将字符串拆分为若干长度为 k 的组](https://leetcode.cn/problems/divide-a-string-into-groups-of-size-k/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2138.将字符串拆分成若干长度为k的组

[力扣](https://leetcode.cn/problems/divide-a-string-into-groups-of-size-k/)

比较基础的题目，直接一趟遍历，每k个字符一组添加到答案中，然后对最后一组用fill补足到长度k即可。需要注意字符串长度恰好为k的情况。

当然，在这里也可以运用语言特性，直接截取字符串中的子串。

最后附上python代码：

```python
class Solution(object):
    def divideString(self, s, k, fill):
        """
        :type s: str
        :type k: int
        :type fill: str
        :rtype: List[str]
        """

        res = [[]]
        for char in s:
            res[-1].append(char)
            if len(res[-1]) == k:
                res.append([])
        
        if len(res[-1]) == 0:
            res.pop()

        if len(res[-1]) < k:
            res[-1].extend([fill] * (k - len(res[-1])))
        
        return [''.join(part) for part in res]
```
