---
title: "2390. 从字符串中移除星号"
aliases: ["yiduobo的每日leetcode 2390.从字符串中移除星号"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/565767599"
zhihu_id: "565767599"
zhihu_title: "yiduobo的每日leetcode 2390.从字符串中移除星号"
question_id: "2390"
question: "从字符串中移除星号"
problem_url: "https://leetcode.cn/problems/removing-stars-from-a-string/"
difficulty: "Medium"
rating: 1348
created: "2022-09-19T00:50:17+08:00"
updated: "2022-09-19T00:50:17+08:00"
upvotes: 0
comments: 0
---

# 2390. 从字符串中移除星号

> **[yiduobo的每日leetcode 2390.从字符串中移除星号](https://zhuanlan.zhihu.com/p/565767599) · 知乎 · 2022-09-19 · 赞同 0**
> 力扣：[2390. 从字符串中移除星号](https://leetcode.cn/problems/removing-stars-from-a-string/) · Medium · 灵茶山艾府：[O(n) 用栈维护（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2390.从字符串中移除星号

[力扣](https://leetcode.cn/problems/removing-stars-from-a-string/)

题目可能出现连续的星号，而每个星号则会消耗掉当前储存的最后一个字符，那么很自然联想到使用栈来储存字符。从头开始向后一趟遍历，若当前字符为星号，则将栈顶字符弹出，否则将当前字符加入到栈中。遍历完成后，栈中剩余的字符即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def removeStars(self, s):
        """
        :type s: str
        :rtype: str
        """

        stack = []
        for char in s:
            if char == '*':
                stack.pop()
            else:
                stack.append(char)
        
        return ''.join(stack)
```
