---
title: "3168. 候诊室中的最少椅子数"
aliases: ["yiduobo的每日leetcode 3168.候诊室中的最少椅子数"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/704999837"
zhihu_id: "704999837"
zhihu_title: "yiduobo的每日leetcode 3168.候诊室中的最少椅子数"
question_id: "3168"
question: "候诊室中的最少椅子数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-chairs-in-a-waiting-room/"
difficulty: "Easy"
created: "2024-06-23T22:36:54+08:00"
updated: "2024-06-23T22:36:54+08:00"
upvotes: 1
comments: 0
---

# 3168. 候诊室中的最少椅子数

> **[yiduobo的每日leetcode 3168.候诊室中的最少椅子数](https://zhuanlan.zhihu.com/p/704999837) · 知乎 · 2024-06-23 · 赞同 1**
> 力扣：[3168. 候诊室中的最少椅子数](https://leetcode.cn/problems/minimum-number-of-chairs-in-a-waiting-room/) · Easy · 灵茶山艾府：[转换成上下车更好理解（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3168.候诊室中的最少椅子数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-chairs-in-a-waiting-room/description/)

题目给出一个字符串s，模拟每秒钟的时间i。当s[i]为'E'时，表示来了一位顾客并占用了一把椅子，当s[i]为'L'时，则表示有一位顾客走了并空出一把椅子。问至少要准备多少椅子才能让每位顾客都有椅子坐。

题目实际上要求的是同时到达的顾客数量，于是只需使用一个变量now统计当前的顾客人数，然后一趟遍历，对于当前遍历到的s[i]，若s[i]为'E'，那么就将now加上1，并使用now来更新答案；若s[i]为'L'，则将now减去1。

最后附上python代码：

```python
class Solution(object):
    def minimumChairs(self, s):
        """
        :type s: str
        :rtype: int
        """

        now = 0
        res = 0
        for char in s:
            if char == 'E':
                now += 1
                res = max(res, now)
            else:
                now -= 1
            
        return res
```
