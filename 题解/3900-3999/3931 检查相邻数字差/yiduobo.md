---
title: "3931. 检查相邻数字差"
aliases: ["yiduobo的每日leetcode 3931.检查相邻数字差"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2042061502711059766"
zhihu_id: "2042061502711059766"
zhihu_title: "yiduobo的每日leetcode 3931.检查相邻数字差"
question_id: "3931"
question: "检查相邻数字差"
problem_url: "https://leetcode.cn/problems/check-adjacent-digit-differences/"
difficulty: "Easy"
created: "2026-05-25T21:26:16+08:00"
updated: "2026-05-25T21:26:19+08:00"
upvotes: 1
comments: 0
---

# 3931. 检查相邻数字差

> **[yiduobo的每日leetcode 3931.检查相邻数字差](https://zhuanlan.zhihu.com/p/2042061502711059766) · 知乎 · 2026-05-25 · 赞同 1**
> 力扣：[3931. 检查相邻数字差](https://leetcode.cn/problems/check-adjacent-digit-differences/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3931.检查相邻数字差

<https://leetcode.cn/problems/check-adjacent-digit-differences/>

题目给出一个由数字组成的字符串s。

如果每一对相邻数字之间的绝对差都至多为2，那么返回true，否则返回false。

按照题目要求直接模拟检测即可。

从下标1开始向后遍历。对于当前遍历到的下标index，若nums[index]与nums[index - 1]差的绝对值大于2，则返回false。若顺利遍历完成，则返回true。

最后附上python代码：

```python
class Solution(object):
    def isAdjacentDiffAtMostTwo(self, s):
        """
        :type s: str
        :rtype: bool
        """
        
        for index in range(1, len(s)):
            if abs(int(s[index]) - int(s[index - 1])) > 2:
                return False

        return True
```
