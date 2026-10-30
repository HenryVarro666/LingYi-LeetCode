---
title: "394. 字符串编码"
aliases: ["yiduobo的每日leetcode 394.字符串编码"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/recursion", "题单/常用数据结构", "题单/LeetCode-热题-100", "题单/常用数据结构/三-栈", "题单/LeetCode-热题-100/栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/176976606"
zhihu_id: "176976606"
zhihu_title: "yiduobo的每日leetcode 394.字符串编码"
question_id: "394"
question: "字符串解码"
problem_url: "https://leetcode.cn/problems/decode-string/"
difficulty: "Medium"
created: "2020-08-09T21:10:30+08:00"
updated: "2020-08-09T21:10:30+08:00"
upvotes: 0
comments: 0
---

# 394. 字符串编码

> **[yiduobo的每日leetcode 394.字符串编码](https://zhuanlan.zhihu.com/p/176976606) · 知乎 · 2020-08-09 · 赞同 0**
> 力扣：[394. 字符串解码](https://leetcode.cn/problems/decode-string/) · Medium · 灵茶山艾府：[递归 / 用栈模拟递归（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

394.字符串编码<https://leetcode-cn.com/problems/decode-string/>

又是典型的栈操作的题目，从左往右一趟扫描，对于当前字符有四种情况：

1、当前字符为数字：

此时只需要更新倍数multi即可

2、当前字符为字母：

此时只需要更新当前的字符串res即可

3、当前字符为左括号：

此时需要将res以及multi都压入栈中，并将res以及multi重置，具体为multi\=0，res\=''

4、当前字符为右括号时：

此时需要将栈顶弹出，并更新当前的统计结果。需要注意的是，栈顶的multi是用来修饰当前res的，因此最终的字符串res应该为res \= prev_res + prev_multi \* res

最后附上python代码：

```python
class Solution(object):
    def decodeString(self, s):
        """
        :type s: str
        :rtype: str
        """

        stack = []
        res = ''
        multi = 0
        for char in s:
            if ord(char) >= 48 and ord(char) <= 57:
                multi = multi * 10 + int(char)
            elif char == '[':
                stack.append([res, multi])
                res = ''
                multi = 0
            elif char == ']':
                prev_res, prev_multi = stack.pop()
                res = prev_res + res * prev_multi
            else:
                res += char

        return res
```
