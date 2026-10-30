---
title: "3253. 最小代价构造字符串（简单）"
aliases: ["yiduobo的每日leetcode 3253.最小代价构造字符串（简单）"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/721707612"
zhihu_id: "721707612"
zhihu_title: "yiduobo的每日leetcode 3253.最小代价构造字符串（简单）"
question_id: "3253"
question: "最小代价构造字符串（简单）"
problem_url: "https://leetcode.cn/problems/construct-string-with-minimum-cost-easy/"
created: "2024-09-23T23:29:41+08:00"
updated: "2024-09-23T23:29:41+08:00"
upvotes: 0
comments: 0
---

# 3253. 最小代价构造字符串（简单）

> **[yiduobo的每日leetcode 3253.最小代价构造字符串（简单）](https://zhuanlan.zhihu.com/p/721707612) · 知乎 · 2024-09-23 · 赞同 0**
> 力扣：[3253. 最小代价构造字符串（简单）](https://leetcode.cn/problems/construct-string-with-minimum-cost-easy/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3253.最小代价构造字符串(简单)

[. - 力扣（LeetCode）](https://leetcode.cn/problems/construct-string-with-minimum-cost-easy/description/)

题目给出一个字符串target，以及一个字符串数组words和一个整数数组costs，这两个数组的长度相同。现在要求使用words中的字符串构造出target，问构造的最小代价是多少。

经典的动态规划问题，因为过于经典且数据规模较小，还特意在标题里补充了一个简单。

令f[index]表示构造target的前index个字符的最小代价，边界情况有f[0] \= 0。接下来对于所有的f[index]，枚举所有长度小于等于index的单词w，设其需要的代价为c，若target[index - len(w) : index]与w相同，那么就有f[index] \= min(f[index], f[index - len(w)] + c)，当然前提是f[index - len(w)]本身是可达的状态。

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, target, words, costs):
        """
        :type target: str
        :type words: List[str]
        :type costs: List[int]
        :rtype: int
        """

        n = len(target)
        f = [-1] * (n + 1)
        f[0] = 0

        for index in range(1, n + 1):
            for w, c in zip(words, costs):
                if index >= len(w) and f[index - len(w)] != -1 and target[index - len(w) : index] == w:
                    if f[index] == -1 or f[index] > f[index - len(w)] + c:
                        f[index] = f[index - len(w)] + c
        
        return f[-1]
```
