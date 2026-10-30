---
title: "3438. 找到字符串中合法的相邻数字"
aliases: ["yiduobo的每日leetcode 3438.找到字符串中合法的相邻数字"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1891292584124588506"
zhihu_id: "1891292584124588506"
zhihu_title: "yiduobo的每日leetcode 3438.找到字符串中合法的相邻数字"
question_id: "3438"
question: "找到字符串中合法的相邻数字"
problem_url: "https://leetcode.cn/problems/find-valid-pair-of-adjacent-digits-in-string/"
difficulty: "Easy"
created: "2025-04-04T00:59:32+08:00"
updated: "2025-04-04T00:59:32+08:00"
upvotes: 1
comments: 0
---

# 3438. 找到字符串中合法的相邻数字

> **[yiduobo的每日leetcode 3438.找到字符串中合法的相邻数字](https://zhuanlan.zhihu.com/p/1891292584124588506) · 知乎 · 2025-04-04 · 赞同 1**
> 力扣：[3438. 找到字符串中合法的相邻数字](https://leetcode.cn/problems/find-valid-pair-of-adjacent-digits-in-string/) · Easy · 灵茶山艾府：[计数+遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3438.找到字符串中合法的相邻数字

[3438. 找到字符串中合法的相邻数字 - 力扣（LeetCode）](https://leetcode.cn/problems/find-valid-pair-of-adjacent-digits-in-string/description/)

题目给出一个只包含数字的字符串s，若s中两个相邻的数字s[index - 1]以及s[index]满足s[index - 1]不等于s[index]，且s中s[index - 1]出现的次数恰好就是s[index - 1]次，s[index]出现的次数恰好就是s[index]次，那么就称这两个相邻数字是合法的。

现在要求找出s中首次出现的合法相邻数字，如果不存在，返回空字符串。

按照题目要求模拟。由于需要判断某个数出现的次数是否恰好就等于其自身的数值，那么就需要先进行一趟遍历，统计每种数字出现的次数。接下来再从下标1开始进行一趟遍历，判断当前的s[index - 1]以及s[index]是否符合题目给出的条件就行了。

最后附上python代码：

```python
class Solution(object):
    def findValidPair(self, s):
        """
        :type s: str
        :rtype: str
        """
        
        cnt = [0] * 10
        for digit in s:
            cnt[int(digit)] += 1
        
        for index in range(1, len(s)):
            if s[index] != s[index - 1] and cnt[int(s[index - 1])] == int(s[index - 1]) and cnt[int(s[index])] == int(s[index]):
                return s[index - 1: index + 1]
        
        return ""
```
