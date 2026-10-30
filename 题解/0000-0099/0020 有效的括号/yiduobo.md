---
title: "20. 有效的括号"
aliases: ["yiduobo的每日leetcode 20.有效的括号"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/stack", "leetcode/string", "题单/常用数据结构", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/常用数据结构/三-栈", "题单/LeetCode-热题-100/栈", "题单/面试经典-150-题/栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/115365029"
zhihu_id: "115365029"
zhihu_title: "yiduobo的每日leetcode 20.有效的括号"
question_id: "20"
question: "有效的括号"
problem_url: "https://leetcode.cn/problems/valid-parentheses/"
difficulty: "Easy"
created: "2020-03-22T23:52:58+08:00"
updated: "2020-03-22T23:52:58+08:00"
upvotes: 0
comments: 0
---

# 20. 有效的括号

> **[yiduobo的每日leetcode 20.有效的括号](https://zhuanlan.zhihu.com/p/115365029) · 知乎 · 2020-03-22 · 赞同 0**
> 力扣：[20. 有效的括号](https://leetcode.cn/problems/valid-parentheses/) · Easy · 灵茶山艾府：[括号消消乐：三种利用栈的写法，附题单！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

20.有效的括号<https://leetcode-cn.com/problems/valid-parentheses/>

括号匹配是经典的栈的题目，简单来说就是对于一个左括号，直接压入栈顶，而对于一个右括号，如果当前栈为空或者栈顶不是左括号，那么就不合法，否则弹出栈顶的左括号来和这个右括号配对。

这里有三种类型的括号，所以碰到右括号时需要判断是否是同类别的左括号，例如 ( [ ) ] 这种情况，扫描到第一个小括号虽然栈顶是左括号，但是这是个左中括号，依然不合法。

最后需要注意的是，当字符串扫描结束之后，如果栈中还有元素，说明存在依然单身的左括号，这个情况同样是不合法的。

最后附上python代码：

```python
class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        stack = []
        for char in s:
            if char in ['(', '[', '{']:
                stack.append(char)
            elif not stack:
                return False
            elif char == ')' and stack.pop() != '(':
                return False
            elif char == ']' and stack.pop() != '[':
                return False
            elif char == '}' and stack.pop() != '{':
                return False
        
        return not stack
```
