---
title: "1974. 使用特殊打字机键入单词的最少时间"
aliases: ["yiduobo的每日leetcode 1974.使用特殊打字机键入单词的最少时间"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/496284419"
zhihu_id: "496284419"
zhihu_title: "yiduobo的每日leetcode 1974.使用特殊打字机键入单词的最少时间"
question_id: "1974"
question: "使用特殊打字机键入单词的最少时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-type-word-using-special-typewriter/"
difficulty: "Easy"
created: "2022-04-11T00:02:35+08:00"
updated: "2022-04-11T00:02:36+08:00"
upvotes: 0
comments: 0
---

# 1974. 使用特殊打字机键入单词的最少时间

> **[yiduobo的每日leetcode 1974.使用特殊打字机键入单词的最少时间](https://zhuanlan.zhihu.com/p/496284419) · 知乎 · 2022-04-11 · 赞同 0**
> 力扣：[1974. 使用特殊打字机键入单词的最少时间](https://leetcode.cn/problems/minimum-time-to-type-word-using-special-typewriter/) · Easy · 灵茶山艾府：[Go 贪心](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1974.使用特殊打字机键入单词的最少时间

[力扣](https://leetcode-cn.com/problems/minimum-time-to-type-word-using-special-typewriter/)

题目实际上需要计算各个字符之间移动的距离，由于这是一个圆盘，因此可以按照顺时针或者逆时针的顺序来进行移动。当顺时针移动时，移动的距离就是较大字符的ascii码减去较小字符的ascii码，而逆时针移动的距离，则可以使用26减去顺时针移动的距离来得到。

一趟遍历，计算相邻字符间的距离累加起来即可。需要注意一开始是从字符'a'开始的，且每次移动完后需要再加上一步键入的操作。

最后附上python代码：

```python
class Solution(object):
    def minTimeToType(self, word):
        """
        :type word: str
        :rtype: int
        """

        res = 0
        now = 'a'
        for char in word:
            delta = abs(ord(char) - ord(now))
            res += min(delta, 26 - delta) + 1
            now = char
        
        return res
```
