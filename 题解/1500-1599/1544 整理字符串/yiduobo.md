---
title: "1544. 整理字符串"
aliases: ["yiduobo的每日leetcode 1544.整理字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/424979597"
zhihu_id: "424979597"
zhihu_title: "yiduobo的每日leetcode 1544.整理字符串"
question_id: "1544"
question: "整理字符串"
problem_url: "https://leetcode.cn/problems/make-the-string-great/"
created: "2021-10-23T22:14:51+08:00"
updated: "2021-10-23T22:14:51+08:00"
upvotes: 0
comments: 0
---

# 1544. 整理字符串

> **[yiduobo的每日leetcode 1544.整理字符串](https://zhuanlan.zhihu.com/p/424979597) · 知乎 · 2021-10-23 · 赞同 0**
> 力扣：[1544. 整理字符串](https://leetcode.cn/problems/make-the-string-great/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1544.整理字符串

[力扣](https://leetcode-cn.com/problems/make-the-string-great/)

题目要求将相邻的特定字符对消去，可以视为某种特殊的括号匹配问题，那么可以一趟扫描，使用一个栈来维护当前剩下的字符。若当前字符与栈顶字符形成配对，那么将栈顶弹出，否则将当前字符压入栈中。遍历完成后，栈中剩下的字符即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def makeGood(self, s):
        """
        :type s: str
        :rtype: str
        """

        stack = []
        for char in s:
            if stack and abs(ord(stack[-1]) - ord(char)) == 32:
                stack.pop()
            else:
                stack.append(char)
        
        return ''.join(stack)
```
