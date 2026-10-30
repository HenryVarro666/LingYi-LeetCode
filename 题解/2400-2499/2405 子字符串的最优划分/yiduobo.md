---
title: "2405. 子字符串的最优划分"
aliases: ["yiduobo的每日leetcode 2405.子字符串的最优划分"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bit-manipulation", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/567888470"
zhihu_id: "567888470"
zhihu_title: "yiduobo的每日leetcode 2405.子字符串的最优划分"
question_id: "2405"
question: "子字符串的最优划分"
problem_url: "https://leetcode.cn/problems/optimal-partition-of-string/"
difficulty: "Medium"
rating: 1355
created: "2022-09-25T02:16:16+08:00"
updated: "2022-09-25T02:16:16+08:00"
upvotes: 0
comments: 0
---

# 2405. 子字符串的最优划分

> **[yiduobo的每日leetcode 2405.子字符串的最优划分](https://zhuanlan.zhihu.com/p/567888470) · 知乎 · 2022-09-25 · 赞同 0**
> 力扣：[2405. 子字符串的最优划分](https://leetcode.cn/problems/optimal-partition-of-string/) · Medium · 灵茶山艾府：[贪心 + 位运算 O(1) 空间](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2405.子字符串的最优划分

[力扣](https://leetcode.cn/problems/optimal-partition-of-string/)

贪心法的题目。首先，对于一个字符串和该字符串的某个后缀字符串而言，后缀字符串的最优划分得到的字符串数目显然比原字符串的最优化分得到的字符串数目要少，也就是说对于划分出去的第一个字符串而言，应该尽可能地划分得长一些，这样一来后面剩余的字符串就可能有更好的划分方案。

为了使得划分出去的第一个字符串尽量的长，那么就可以一趟遍历，尽量将字符加入到第一个字符串中，直到某个字符出现了重复。那么可以使用一个set记录当前划分中已经出现的字符，若当前字符在set中，那么当前的划分就到此为止了，此时应该将set情况并更新答案。最后，还需要将当前字符加入到set中，然后继续向后遍历。

遍历完成后，由于最后一个划分出去的字符串没有被记录到答案中，因此还需要将最终答案加上1。

最后附上python代码：

```python
class Solution(object):
    def partitionString(self, s):
        """
        :type s: str
        :rtype: int
        """

        used = set()
        res = 0
        for char in s:
            if char in used:
                res += 1
                used = set()
            used.add(char)
        
        return res + 1
```
