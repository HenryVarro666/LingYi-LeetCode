---
title: "3174. 清除数字"
aliases: ["yiduobo的每日leetcode 3174.清除数字"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/stack", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/705432428"
zhihu_id: "705432428"
zhihu_title: "yiduobo的每日leetcode 3174.清除数字"
question_id: "3174"
question: "清除数字"
problem_url: "https://leetcode.cn/problems/clear-digits/"
difficulty: "Easy"
created: "2024-06-26T00:06:08+08:00"
updated: "2024-06-26T00:06:08+08:00"
upvotes: 2
comments: 0
---

# 3174. 清除数字

> **[yiduobo的每日leetcode 3174.清除数字](https://zhuanlan.zhihu.com/p/705432428) · 知乎 · 2024-06-26 · 赞同 2**
> 力扣：[3174. 清除数字](https://leetcode.cn/problems/clear-digits/) · Easy · 灵茶山艾府：[O(n) 用栈维护（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3174.清除数字

[. - 力扣（LeetCode）](https://leetcode.cn/problems/clear-digits/description/)

题目给出一个字符串s，其中可能包含小写字符与数字。现在要求不断将s中最左侧的数字以及该数字左侧最近的一个字符删掉，问删除所有数字后剩下的字符串是什么。

对于每一轮操作，题目要求删除的是最左侧的数字以及其左侧最近的字符，那么为了适配最左侧的数字，就可以考虑正序遍历，逐个处理遍历到的数字。对于当前数字，其左侧最近的字符就是已经遍历过的s中还未被删除的最后一个遍历到的字符，是先进后出的场景，因此可以使用栈来储存遍历过的字符，当碰到数字时就将栈顶元素删去。遍历完成后，栈中剩余的字符就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def clearDigits(self, s):
        """
        :type s: str
        :rtype: str
        """

        stack = []
        for char in s:
            if '0' <= char <= '9':
                if stack:
                    stack.pop()
            else:
                stack.append(char)

        return ''.join(stack)
```
